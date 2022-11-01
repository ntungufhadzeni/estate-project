$('.navToggle').on('click', function (e) {
  e.preventDefault();
  $('body').toggleClass('navToggleActive');
});

$(window).scroll(function(){
  if ($(this).scrollTop() > 10) {
    $('body').addClass('fixedHeader');
  } else {
    $('body').removeClass('fixedHeader');
  }
});


var swiper = new Swiper(".testimonialSwiper", {
  navigation: {
    nextEl: ".test-swiper-button-next",
    prevEl: ".test-swiper-button-prev",
  },
});


var swiper = new Swiper(".certificatesSlider", {
  slidesPerView: 1,
  spaceBetween: 16,
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
  navigation: {
    nextEl: ".cert-swiper-button-next",
    prevEl: ".cert-swiper-button-prev",
  },
  breakpoints: {
    640: {
      slidesPerView: 2,
      spaceBetween: 16,
    },
    768: {
      slidesPerView: 2,
      spaceBetween: 16,
    },
    1024: {
      slidesPerView: 2,
      spaceBetween: 16,
    },
  },
});

function ShowHideDiv() {
        let chkYes1 = document.getElementById("Yes 0");
        let specify1 = document.getElementById("dv 0");
        specify1.style.display = chkYes1.checked ? "block" : "none";

        let chkYes2 = document.getElementById("Yes 1");
        let specify2 = document.getElementById("dv 1");
        specify2.style.display = chkYes2.checked ? "block" : "none";

        let chkYes3 = document.getElementById("Yes 2");
        let specify3 = document.getElementById("dv 2");
        specify3.style.display = chkYes3.checked ? "block" : "none";

        let chkYes4 = document.getElementById("Yes 3");
        let specify4 = document.getElementById("dv 3");
        specify4.style.display = chkYes4.checked ? "block" : "none";

        let chkYes5 = document.getElementById("Yes 4");
        let specify5 = document.getElementById("dv 4");
        specify5.style.display = chkYes5.checked ? "block" : "none";

        let chkYes6 = document.getElementById("Yes 5");
        let specify6 = document.getElementById("dv 5");
        specify6.style.display = chkYes6.checked ? "block" : "none";

        let chkYes7 = document.getElementById("Yes 6");
        let specify7 = document.getElementById("dv 6");
        specify7.style.display = chkYes7.checked ? "block" : "none";
    }