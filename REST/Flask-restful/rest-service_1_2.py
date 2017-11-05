from flask import Flask, request
from flask_restful import Resource, Api
import MySQLdb

app = Flask(__name__)
api = Api(app)

# config = {
#     'user': 'spp',
#     'password': 'spp',
#     'database': 'spp',
#     'host': 'localhost',
#     'charset': 'utf8'
# }
# db = MySQLdb


class WorkResource(Resource):
    config = {
        'user': 'spp',
        'password': 'spp',
        'database': 'spp',
        'host': 'localhost',
        'charset': 'utf8'
    }
    db = MySQLdb

    @classmethod
    def __init__(cls):
        cls.conn = cls.db.connect(**cls.config)
        cls.cursor = cls.conn.cursor()


class Dictionary(WorkResource):
    table = 'some_table'

    @classmethod
    def get(cls, _id=None, _name=None):
        # cls.__init__()
        conn = cls.conn
        cursor = cls.cursor
        table = cls.table
        if _id:
            cursor.execute(
                "select Name from `{}` where ID='{}'".format(table, _id)
            )
        elif _name:
            cursor.execute(
                "select ID from `{}` where Name='{}'".format(table, _name)
            )
        else:
            cursor.execute("select Name from `{}`".format(table))
        result = cursor.fetchall()
        conn.close()
        return [i[0] for i in result]

    @classmethod
    def put(cls, _name=None, person_id=None):
        # cls.__init__()
        conn = cls.conn
        cursor = cls.cursor
        table = cls.table
        if person_id:
            cursor.execute(
                "insert into `{}` (Name, PersonID) values ('{}', '{}')"
                .format(table, _name, person_id))
        else:
            cursor.execute(
                "insert into `{}` (Name) values ('{}')"
                .format(table, _name))
        conn.commit()
        cursor.execute("select ID from `{}` where Name='{}'".format(table, _name))
        result = cursor.fetchone()[0]
        conn.close()
        return result

    @classmethod
    def post(cls, _id=None, _name=None, person_id=None):
        # cls.__init__()
        conn = cls.conn
        cursor = cls.cursor
        table = cls.table
        if person_id:
            cursor.execute(
                "update `{}` set Name='{}', PersonID='{}' where ID='{}'"
                .format(table, _name, person_id, _id)
            )
        else:
            cursor.execute(
                "update `{}` set Name='{}' where ID='{}'".format(table, _name, _id)
            )
        conn.commit()
        conn.close()

    @classmethod
    def delete(cls, _id=None):
        # cls.__init__()
        conn = cls.conn
        cursor = cls.cursor
        table = cls.table
        if _id:
            cursor.execute("delete from `{}` where ID='{}'".format(table, _id))
        else:
            cursor.execute("delete from `{}`".format(table))
        conn.commit()
        conn.close()


class Persons(Dictionary):
    table = 'persons'


class Keywords(Dictionary):
    table = 'keywords'

    def get(self, _id=None, _name=None, person_id=None, person_name=None):
        # self.__init__()
        conn = self.conn
        cursor = self.cursor
        table = self.table
        if _id is None and _name is None:
            cursor.execute(
                """select t2.Name, t1.Name from `{}` t1
                    join persons t2 on t1.PersonID=t2.ID
                """.format(table)
            )
            result = {}
            for item in cursor.fetchall():
                result.setdefault(item[0], []).append(item[1])
        else:
            if person_id:
                cursor.execute(
                    "select Name from `{}` where PersonID='{}'".format(table, person_id)
                )
            elif person_name:
                cursor.execute(
                    """select t1.Name from `{}` t1
                        join persons t2 on t1.PersonID=t2.ID
                        where t2.Name='{}'""".format(table, person_name)
                )
            elif _id:
                cursor.execute(
                    "select Name from `{}` where ID='{}'".format(table, _id)
                )
            elif _name:
                cursor.execute(
                    """select t2.Name from `{}` t1
                        join persons t2 on t1.PersonID=t2.ID
                        where t1.Name='{}'""".format(table, _name)
                )
            result = [i[0] for i in cursor.fetchall()]
        conn.close()
        return result


class Sites(Dictionary):
    table = 'sites'


class PersonPageRank(WorkResource):
    table = 'personpagerank'

    def get(self, person_id=None, site_id=None, start_date=None, end_date=None):
        # self.__init__()
        conn = self.conn
        cursor = self.cursor
        table = self.table
        sql_str = """select t1.Rank from `{0}` t1
                        join pages t2 on t1.PageID=t2.ID
                        join persons t3 on t1.PersonID=t3.ID
                        {{}}
                        where t3.ID='{1}'{{}}""".format(table, person_id)
        if site_id:
            sql_str = sql_str.format(
                "join sites t4 on t2.SiteID=t4.ID",
                " and t4.ID='{}'{{}}".format(site_id)
            )
            if start_date:
                if end_date is None:
                    sql_str = sql_str.format(
                        " and t2.FoundDateTime='{}'".format(start_date)
                    )
                    cursor.execute(sql_str)
                else:
                    sql_str = sql_str.format(
                        " and t2.FoundDateTime>='{}' and t2.FoundDateTime<='{}'"
                        .format(start_date, end_date)
                    )
                    cursor.execute(sql_str)
            else:
                cursor.execute(sql_str.format(''))
        else:
            cursor.execute(sql_str.format('', ''))
        result = sum(map(lambda x: x[0], cursor.fetchall()))
        conn.close()
        return result


api.add_resource(
    Keywords,
    '/keywords',
    '/keywords/<int:_id>',
    '/keywords/<string:_name>',
    '/keywords/<int:person_id>/<string:_name>',
    '/keywords/<int:_id>/<int:person_id>/<string:_name>',
    '/keywords/person/<int:person_id>',
    '/keywords/person/<string:person_name>',
)
api.add_resource(
    Persons,
    '/persons',
    '/persons/<int:_id>',
    '/persons/<string:_name>',
    '/persons/<int:_id>/<string:_name>',
)
api.add_resource(
    Sites,
    '/sites',
    '/sites/<int:_id>',
    '/sites/<string:_name>',
    '/sites/<int:_id>/<string:_name>',
)
api.add_resource(
    PersonPageRank,
    '/rank/<int:person_id>',
    '/rank/<int:person_id>/<int:site_id>',
    '/rank/<int:person_id>/<int:site_id>/<string:start_date>',
    '/rank/<int:person_id>/<int:site_id>/<string:start_date>&<string:end_date>'
)

if __name__ == '__main__':
    app.run()