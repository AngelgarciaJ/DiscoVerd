document.addEventListener('DOMContentLoaded', function() {
  // Animación para las secciones del perfil
  const profileSections = document.querySelectorAll('.profile-section');
  profileSections.forEach((section, index) => {
      section.style.opacity = '0';
      section.style.transform = 'translateY(20px)';
      setTimeout(() => {
          section.style.transition = 'all 0.5s ease';
          section.style.opacity = '1';
          section.style.transform = 'translateY(0)';
      }, index * 100);
  });

  // Efecto hover para badges
  const badges = document.querySelectorAll('.badge');
  badges.forEach(badge => {
      badge.addEventListener('mouseenter', function() {
          this.style.transform = 'scale(1.1)';
      });
      badge.addEventListener('mouseleave', function() {
          this.style.transform = 'scale(1)';
      });
  });

  // Botón de editar perfil
  const editButton = document.querySelector('.edit-button');
  if (editButton) {
      editButton.addEventListener('click', function() {
          const currentLocation = this.getAttribute('href');
          this.classList.add('clicked');
          setTimeout(() => {
              window.location.href = currentLocation;
          }, 300);
      });
  }
});