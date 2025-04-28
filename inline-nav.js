document.addEventListener('DOMContentLoaded', () => {
  // Smooth scrolling for navigation links
  document.querySelectorAll('.inline-nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const targetId = link.getAttribute('href');
      const targetSection = document.querySelector(targetId);
      
      window.scrollTo({
        top: targetSection.offsetTop - 100,
        behavior: 'smooth'
      });
    });
  });

  // Update active section on scroll
  const sections = document.querySelectorAll('.content-section');
  const navLinks = document.querySelectorAll('.inline-nav-link');

  function updateActiveSection() {
    let currentSection = '';
    
    sections.forEach(section => {
      const sectionTop = section.offsetTop - 150;
      const sectionHeight = section.clientHeight;
      
      if (window.scrollY >= sectionTop && window.scrollY < sectionTop + sectionHeight) {
        currentSection = section.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === `#${currentSection}`) {
        link.classList.add('active');
      }
    });
  }

  // Tilt card effect
  const tiltCard = document.querySelector('.tilt-card');
  if (tiltCard) {
    tiltCard.addEventListener('mousemove', (e) => {
      const rect = tiltCard.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      
      const rotateX = (y - centerY) / 10;
      const rotateY = (centerX - x) / 10;
      
      tiltCard.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
    });

    tiltCard.addEventListener('mouseleave', () => {
      tiltCard.style.transform = 'perspective(1000px) rotateX(0) rotateY(0)';
    });
  }

  // Mouse tracking effect
  const mouseTrackCard = document.querySelector('.mouse-track-card');
  const mouseTrackDot = document.querySelector('.mouse-track-dot');
  const mouseXDisplay = document.getElementById('mouseX');
  const mouseYDisplay = document.getElementById('mouseY');

  if (mouseTrackCard && mouseTrackDot) {
    mouseTrackCard.addEventListener('mousemove', (e) => {
      const rect = mouseTrackCard.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      // Update dot position
      mouseTrackDot.style.left = `${x}px`;
      mouseTrackDot.style.top = `${y}px`;
      
      // Update coordinates display
      mouseXDisplay.textContent = Math.round(x);
      mouseYDisplay.textContent = Math.round(y);
      
      // Add parallax effect to content
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      const moveX = (x - centerX) / 20;
      const moveY = (y - centerY) / 20;
      
      mouseTrackCard.style.transform = `perspective(1000px) rotateX(${-moveY}deg) rotateY(${moveX}deg)`;
    });

    mouseTrackCard.addEventListener('mouseleave', () => {
      mouseTrackCard.style.transform = 'perspective(1000px) rotateX(0) rotateY(0)';
    });
  }

  window.addEventListener('scroll', updateActiveSection);
  updateActiveSection(); // Initial check
}); 