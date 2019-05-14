$(function () {


    // mobile menu
    $('.menu').click(function () {
        $('.menu-list').toggleClass('open');
    });
    // mark
    $('.mark').click(function () {
        $('.mark-text').toggleClass('open');
    });
    // clear on resize
    $(window).resize(function () {
        $('.menu-list , .mark-text').removeClass('open');
    });


});



