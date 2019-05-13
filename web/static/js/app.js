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


// choose visit date&time
var overlay = $('#overlay');
var modal = $('.modal-div');
var openModalBtn = $('.open-modal');
var closeModal = $('.modal-close, #overlay');

openModalBtn.click(function (e) {
    e.preventDefault();

    var div = $(this).attr('href');
    overlay
        .fadeIn(400,
            function () {
                $(div).css('display', 'block').animate({opacity: 1, top: '475px'}, 200);
            });
});

closeModal.click(function () {
    modal
        .animate({opacity: 0, top: '45%'}, 200,
            function () {
                $(this).css('display', 'none');
                overlay.fadeOut(400);
            }
        );
});


