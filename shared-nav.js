// Navigation functionality
document.addEventListener('DOMContentLoaded', () => {
  const navbar = document.querySelector('.navbar');
  const menuButton = document.querySelector('.menu-button');
  const navLinks = document.querySelector('.nav-links');
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';

  // Set active link
  document.querySelectorAll('.nav-link').forEach(link => {
    if (link.getAttribute('href') === currentPage) {
      link.classList.add('active');
    }
  });

  // Mobile menu toggle
  menuButton.addEventListener('click', () => {
    navLinks.classList.toggle('active');
    menuButton.classList.toggle('active');
  });

  // Close mobile menu when clicking outside
  document.addEventListener('click', (e) => {
    if (!navLinks.contains(e.target) && !menuButton.contains(e.target)) {
      navLinks.classList.remove('active');
      menuButton.classList.remove('active');
    }
  });

  // Scroll behavior
  let lastScroll = 0;
  window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    // Add/remove scrolled class
    if (currentScroll > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }

    // Hide/show navbar on scroll
    if (currentScroll > lastScroll && currentScroll > 100) {
      navbar.style.transform = 'translateY(-100%)';
    } else {
      navbar.style.transform = 'translateY(0)';
    }
    lastScroll = currentScroll;
  });

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
        // Close mobile menu after clicking
        navLinks.classList.remove('active');
        menuButton.classList.remove('active');
      }
    });
  });
}); 