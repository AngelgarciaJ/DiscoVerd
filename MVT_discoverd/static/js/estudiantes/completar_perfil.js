<<<<<<< HEAD

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
=======
document.addEventListener('DOMContentLoaded', function() {
    // Variables principales
    const form = document.getElementById('profile-form');
    const imageUpload = document.getElementById('header-upload');
    const biografiaTextarea = document.getElementById('biografia');
    const charCounter = document.querySelector('.char-counter');
    const habilidadesInput = document.getElementById('habilidades');
    const skillsTagsContainer = document.querySelector('.skills-tags');
    const interestTags = document.querySelectorAll('.interest-tag');
    const interesesHidden = document.getElementById('intereses-hidden');
    const submitBtn = document.getElementById('submitBtn');

    // Función para mostrar notificaciones
    function showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
            <span>${message}</span>
        `;
        document.getElementById('notification-container').appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('fade-out');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    // Validación de imagen
    function validateImage(file) {
        const validTypes = ['image/jpeg', 'image/png', 'image/jpg', 'image/webp', 'image/gif'];
        const maxSize = 5 * 1024 * 1024; // 5MB

        if (!validTypes.includes(file.type)) {
            showNotification('Por favor, sube una imagen en formato válido (JPG, PNG, WEBP, GIF)', 'error');
            return false;
        }

        if (file.size > maxSize) {
            showNotification('La imagen no debe superar los 5MB', 'error');
            return false;
        }

        return true;
    }

    // Función unificada para previsualizar imagen
    function previewImage(event) {
        const file = event.target.files[0];
        if (!file) return;

        if (validateImage(file)) {
            const reader = new FileReader();
            
            reader.onload = function(e) {
                const preview = document.getElementById('header-preview');
                const img = new Image();
                
                img.onload = function() {
                    if (img.width < 200 || img.height < 200) {
                        showNotification('La imagen debe tener al menos 200x200 píxeles', 'error');
                        return;
                    }

                    preview.style.opacity = '0';
                    preview.src = e.target.result;
                    setTimeout(() => preview.style.opacity = '1', 50);
                    updateImageHelperText(file);
                };

                img.src = e.target.result;
            };

            reader.readAsDataURL(file);
        }
    }

    // Función para actualizar el texto de ayuda de la imagen
    function updateImageHelperText(file) {
        const helperText = document.querySelector('.upload-hint');
        const size = (file.size / (1024 * 1024)).toFixed(2);
        helperText.innerHTML = `
            <i class="fas fa-check-circle"></i> Imagen seleccionada: ${file.name} (${size}MB)
        `;
    }

    // Configuración del drag and drop
    function setupImageDragAndDrop() {
        const dropZone = document.querySelector('.profile-image-container');
        
        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        function handleDrop(e) {
            const file = e.dataTransfer.files[0];
            if (file) {
                imageUpload.files = e.dataTransfer.files;
                previewImage({ target: { files: [file] } });
            }
        }

        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(event => 
            dropZone.addEventListener(event, preventDefaults, false));

        dropZone.addEventListener('dragover', () => dropZone.classList.add('drag-over'));
        dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
        dropZone.addEventListener('drop', (e) => {
            dropZone.classList.remove('drag-over');
            handleDrop(e);
        });
        
        // Click para seleccionar archivo
        dropZone.addEventListener('click', () => imageUpload.click());
    }

    // Manejo de intereses académicos
    interestTags.forEach(tag => {
        tag.addEventListener('click', function() {
            this.classList.toggle('selected');
            updateIntereses();
        });
    });

    function updateIntereses() {
        const selectedInterests = Array.from(interestTags)
            .filter(tag => tag.classList.contains('selected'))
            .map(tag => tag.dataset.value);
        interesesHidden.value = selectedInterests.join(',');
    }

    // Manejo del contador de caracteres
    biografiaTextarea.addEventListener('input', function() {
        const maxLength = this.getAttribute('maxlength');
        const currentLength = this.value.length;
        charCounter.textContent = `${currentLength}/${maxLength} caracteres`;
        charCounter.style.color = currentLength >= maxLength ? 'var(--error-color)' : 'var(--text-light)';
    });

    // Manejo de habilidades
    let habilidades = new Set();

    function addHabilidadFromInput() {
        const valor = habilidadesInput.value.trim();
        if (valor && !habilidades.has(valor)) {
            addHabilidad(valor);
            habilidadesInput.value = '';
        }
    }

    function addHabilidad(valor) {
        habilidades.add(valor);
        updateHabilidadesDisplay();
    }

    function removeHabilidad(valor) {
        habilidades.delete(valor);
        updateHabilidadesDisplay();
    }

    function updateHabilidadesDisplay() {
        skillsTagsContainer.innerHTML = '';
        habilidades.forEach(habilidad => {
            const tag = document.createElement('div');
            tag.className = 'skill-tag';
            tag.innerHTML = `
                <span>${habilidad}</span>
                <i class="fas fa-times" onclick="removeHabilidad('${habilidad}')"></i>
            `;
            skillsTagsContainer.appendChild(tag);
        });
    }

    // Eventos de habilidades
    habilidadesInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            addHabilidadFromInput();
        }
    });

    document.querySelector('.add-skill-btn').addEventListener('click', addHabilidadFromInput);

    // Validación del formulario
    function validateForm() {
        let isValid = true;
        const errorMessages = [];

        if (!biografiaTextarea.value.trim()) {
            errorMessages.push('Por favor completa tu biografía académica');
            isValid = false;
        }

        if (!interesesHidden.value) {
            errorMessages.push('Por favor selecciona al menos un área de interés');
            isValid = false;
        }

        if (habilidades.size === 0) {
            errorMessages.push('Por favor agrega al menos una habilidad');
            isValid = false;
        }

        errorMessages.forEach(msg => showNotification(msg, 'error'));
        return isValid;
    }
>>>>>>> e2ce253692cd28d473d9b519ce02e488d98542bf

    // Manejo del envío del formulario
    form.addEventListener('submit', function(e) {
        e.preventDefault();
<<<<<<< HEAD
        
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
=======

        if (validateForm()) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Guardando...';

            const formData = new FormData(this);
            formData.append('habilidades', Array.from(habilidades).join(','));

            fetch(this.action, {
                method: 'POST',
                body: formData,
                credentials: 'same-origin'
            })
            .then(response => {
                if (response.ok) {
                    showNotification('¡Perfil completado exitosamente!', 'success');
                    setTimeout(() => {
                        window.location.href = '/pantalla_principal/';
                    }, 1500);
                } else {
                    throw new Error('Error al guardar el perfil');
                }
            })
            .catch(error => {
                showNotification('Error al guardar los cambios. Por favor intenta nuevamente.', 'error');
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="fas fa-check-circle"></i><span>Completar Perfil</span>';
            });
        }
    });

    // Configuración inicial
    imageUpload.addEventListener('change', previewImage);
    setupImageDragAndDrop();

    // Estilos para drag and drop
    const style = document.createElement('style');
    style.textContent = `
        .drag-over {
            border-color: var(--primary-color) !important;
            transform: scale(1.02);
        }

        .profile-image-container {
            transition: all 0.3s ease;
        }
    `;
    document.head.appendChild(style);
>>>>>>> e2ce253692cd28d473d9b519ce02e488d98542bf
});