
/* Открытие меню */

var main = function() { //главная функция

    $('.icon-menu').click(function() { /* выбираем класс icon-menu и
               добавляем метод click с функцией, вызываемой при клике */

        $('.menu').animate({ //выбираем класс menu и метод animate

            left: '0px' /* теперь при клике по иконке, меню, скрытое за
               левой границей на 285px, изменит свое положение на 0px и станет видимым */

        }, 200); //скорость движения меню в мс

         //скорость движения меню в мс
    });


/* Закрытие меню */

    $('.icon-close').click(function() { //выбираем класс icon-close и метод click

        $('.menu').animate({ //выбираем класс menu и метод animate

            left: '-285px' /* при клике на крестик меню вернется назад в свое
               положение и скроется */

        }, 200); //скорость движения меню в мс

     //скорость движения меню в мс
    });
};

$(document).ready(main);
