<<<<<<< HEAD
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
=======
ocument.addEventListener('DOMContentLoaded', function() {
    // Manejo de errores de imagen
    const profilePhoto = document.querySelector('.profile-photo');
    if (profilePhoto) {
        profilePhoto.addEventListener('error', function() {
            this.src = '/static/img/default-profile.jpg';
        });
    }

    // Función para animar elementos
    function animateElement(element, delay = 0) {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'all 0.5s ease';

        setTimeout(() => {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, delay);
    }

    // Elementos a animar
    const elementsToAnimate = [
        '.profile-photo-container',
        '.profile-title-info',
        '.info-card',
        '.main-card',
        '.buttons-container'
    ];

    elementsToAnimate.forEach((selector, index) => {
        const elements = document.querySelectorAll(selector);
        elements.forEach(element => {
            animateElement(element, 100 * index);
        });
    });

    // Efecto ripple para botones
    function createRipple(event) {
        const button = event.currentTarget;
        
        // Eliminar ripples anteriores
        const ripples = button.getElementsByClassName('ripple');
        Array.from(ripples).forEach(ripple => ripple.remove());

        const circle = document.createElement('span');
        const diameter = Math.max(button.clientWidth, button.clientHeight);
        const radius = diameter / 2;

        const rect = button.getBoundingClientRect();
        
        circle.style.width = circle.style.height = `${diameter}px`;
        circle.style.left = `${event.clientX - rect.left - radius}px`;
        circle.style.top = `${event.clientY - rect.top - radius}px`;
        circle.classList.add('ripple');

        button.appendChild(circle);
    }

    // Aplicar efecto ripple a todos los botones de acción
    document.querySelectorAll('.action-button').forEach(button => {
        button.addEventListener('click', createRipple);
    });

    // Confirmación antes de cerrar sesión
    document.querySelectorAll('.logout-button').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            if (confirm('¿Estás seguro que deseas cerrar sesión?')) {
                window.location.href = this.href;
            }
        });
    });
>>>>>>> e2ce253692cd28d473d9b519ce02e488d98542bf
});