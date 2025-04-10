document.addEventListener('DOMContentLoaded', () => {
  const carousel = document.getElementById('carousel');
  const items = document.querySelectorAll('.carousel-item');
  const prevBtn = document.getElementById('prev');
  const nextBtn = document.getElementById('next');

  let index = 0;

  function updateCarousel() {
    if (!items.length) return;

    const itemWidth = items[0].offsetWidth + 20; // largura + gap
    const offset = (carousel.offsetWidth - itemWidth) / 2;
    carousel.style.transform = `translateX(${-index * itemWidth + offset}px)`;

    items.forEach((item, i) => {
      item.classList.toggle('active', i === index);
    });
  }

  prevBtn?.addEventListener('click', () => {
    index = (index - 1 + items.length) % items.length;
    updateCarousel();
  });

  nextBtn?.addEventListener('click', () => {
    index = (index + 1) % items.length;
    updateCarousel();
  });

  window.addEventListener('resize', updateCarousel);
  updateCarousel();
});
