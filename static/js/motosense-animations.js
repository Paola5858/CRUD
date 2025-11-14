// Animar elementos quando entram na tela
const observeElements = () => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('fade-in');
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.1
  });

  document.querySelectorAll('.animate-on-scroll').forEach(el => {
    observer.observe(el);
  });
};

// Animar números (contador crescente)
const animateValue = (element, start, end, duration) => {
  const range = end - start;
  const increment = range / (duration / 16);
  let current = start;

  const timer = setInterval(() => {
    current += increment;
    if (current >= end) {
      current = end;
      clearInterval(timer);
    }
    element.textContent = Math.floor(current);
  }, 16);
};

// Animar KPI cards ao carregar
document.addEventListener('DOMContentLoaded', () => {
  observeElements();

  // Animar números dos KPIs
  document.querySelectorAll('.kpi-value').forEach(el => {
    const finalValue = parseInt(el.textContent);
    animateValue(el, 0, finalValue, 1000);
  });

  // Adicionar classe de animação com delay
  document.querySelectorAll('.kpi-card').forEach((card, index) => {
    setTimeout(() => {
      card.classList.add('slide-in-right');
    }, index * 100);
  });
});

// Smooth scroll para âncoras
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});

// Feedback visual em botões
document.querySelectorAll('.btn').forEach(btn => {
  btn.addEventListener('click', function(e) {
    const ripple = document.createElement('span');
    ripple.classList.add('ripple');
    this.appendChild(ripple);

    setTimeout(() => ripple.remove(), 600);
  });
});