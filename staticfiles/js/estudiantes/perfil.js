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
});