
/* completar_perfil.js */
// Mantener la función original de previsualización de imagen
function previewImage(event) {
    const reader = new FileReader();
    reader.onload = function() {
        const preview = document.getElementById('header-preview');
        preview.style.opacity = 0;
        preview.src = reader.result;
        preview.onload = () => {
            preview.style.transition = 'opacity 0.5s';
            preview.style.opacity = 1;
        };
    };
    reader.readAsDataURL(event.target.files[0]);
}

// Funciones mejoradas para el manejo del formulario
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('profile-form');
    const inputs = form.querySelectorAll('input[type="text"], textarea');
    const descripcion = document.getElementById('descripcion');
    const counterElement = document.querySelector('.character-counter');
    const maxLength = 500;

    // Actualizar contador de caracteres
    function updateCharacterCount() {
        const currentLength = descripcion.value.length;
        counterElement.textContent = `${currentLength}/${maxLength}`;
        
        if (currentLength >= maxLength) {
            counterElement.style.color = 'var(--error-color)';
        } else {
            counterElement.style.color = '#6b7280';
        }
    }

    // Validar campo individual
    function validateField(input) {
        const feedback = input.nextElementSibling;
        
        if (input.value.trim() === '') {
            input.classList.add('error');
            feedback.textContent = 'Este campo es requerido';
            feedback.style.color = 'var(--error-color)';
            return false;
        } else {
            input.classList.remove('error');
            feedback.textContent = '';
            return true;
        }
    }

    // Actualizar barra de progreso
    function updateProgress() {
        const totalFields = inputs.length;
        let completedFields = 0;

        inputs.forEach(input => {
            if (input.value.trim() !== '') {
                completedFields++;
            }
        });

        const progress = (completedFields / totalFields) * 100;
        document.querySelector('.progress-fill').style.width = `${progress}%`;
    }

    // Event Listeners
    inputs.forEach(input => {
        input.addEventListener('blur', () => {
            validateField(input);
            updateProgress();
        });

        input.addEventListener('input', updateProgress);
    });

    descripcion.addEventListener('input', updateCharacterCount);

    // Manejo del envío del formulario
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        let isValid = true;
        inputs.forEach(input => {
            if (!validateField(input)) {
                isValid = false;
            }
        });

        if (isValid) {
            // Aquí iría tu lógica original de envío
            const notification = document.getElementById('notification');
            notification.classList.add('show');
            
            setTimeout(() => {
                notification.classList.remove('show');
            }, 3000);

            // Simular envío del formulario (reemplazar con tu lógica real)
            setTimeout(() => {
                form.submit();
            }, 500);
        }
    });

    // Inicialización
    updateCharacterCount();
    updateProgress();
});