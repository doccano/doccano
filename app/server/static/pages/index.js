import Swiper from 'swiper';

new Swiper('.swiper-container', {
  // Optional parameters
  loop: true,
  autoplay: {
    delay: 5000,
  },
  // Navigation arrows
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },
});
