$(function(){

	// slider
	$('.owl-carousel').owlCarousel({
	    loop: true,
	    margin: 10,
	    responsiveClass: true,
	    responsive:{
	        0:{
	            items:1,
	            nav:true
	        },
	        600:{
	            items:2,
	            nav:true
	        },
	        1000:{
	            items:4,
	            nav:true,
	            loop:false
	        }
	    }
	});
	// mobile menu
	$('.menu').click(function() {
		$('.menu-list').toggleClass('open');
	});
	// mark
	$('.mark').click(function() {
		$('.mark-text').toggleClass('open');
	});
	// clear on resize
	$(window).resize(function() {
		$('.menu-list , .mark-text').removeClass('open');
	});

});