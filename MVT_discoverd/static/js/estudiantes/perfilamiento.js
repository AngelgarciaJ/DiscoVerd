// perfilamiento.js
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('perfilamientoForm');
    const progressBar = document.querySelector('.progress-fill');
    const formSections = document.querySelectorAll('.form-section');
    
    // Función para actualizar la barra de progreso
    function updateProgress() {
        const newLocal = formSections.length;
        const totalSections = newLocal;
        let completedSections = 0;
        
        formSections.forEach(section => {
            const inputs = section.querySelectorAll('input, select, textarea');
            let sectionComplete = false;
            
            inputs.forEach(input => {
                if ((input.type === 'checkbox' || input.type === 'radio') && input.checked) {
                    sectionComplete = true;
                } else if (input.value && input.value.trim() !== '') {
                    sectionComplete = true;
                }
            });
            
            if (sectionComplete) completedSections++;
        });
        
        const progress = (completedSections / totalSections) * 100;
        progressBar.style.width = `${progress}%`;
    }

    // Event listeners para intereses
    const interestItems = document.querySelectorAll('.interest-item');
    interestItems.forEach(item => {
        item.addEventListener('click', function() {
            const checkbox = this.querySelector('input[type="checkbox"]');
            checkbox.checked = !checkbox.checked;
            this.classList.toggle('selected', checkbox.checked);
            updateProgress();
        });
    });

    // Event listeners para opciones de participación
    const participationOptions = document.querySelectorAll('.participation-option');
    participationOptions.forEach(option => {
        option.addEventListener('click', function() {
            const radio = this.querySelector('input[type="radio"]');
            participationOptions.forEach(opt => {
                opt.classList.remove('active');
                opt.querySelector('input[type="radio"]').checked = false;
            });
            this.classList.add('active');
            radio.checked = true;
            updateProgress();
        });
    });

    // Event listeners para todos los inputs
    form.addEventListener('input', function(e) {
        updateProgress();
    });

    // Validación del formulario
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Verificar intereses seleccionados
        const interesesSeleccionados = document.querySelectorAll('input[name="intereses"]:checked');
        if (interesesSeleccionados.length === 0) {
            alert('Por favor selecciona al menos un interés');
            return;
        }

        // Verificar disponibilidad
        const disponibilidadSeleccionada = document.querySelectorAll('input[name="disponibilidad"]:checked');
        if (disponibilidadSeleccionada.length === 0) {
            alert('Por favor selecciona al menos un horario de disponibilidad');
            return;
        }

        // Verificar modo de participación
        const modoParticipacion = document.querySelector('input[name="modo_participacion"]:checked');
        if (!modoParticipacion) {
            alert('Por favor selecciona un modo de participación');
            return;
        }

        // Verificar objetivos
        const objetivos = document.querySelector('textarea[name="objetivos"]');
        if (!objetivos.value.trim()) {
            alert('Por favor describe tus objetivos');
            return;
        }

        // Verificar ubicación
        const ubicacion = document.querySelector('input[name="ubicacion"]');
        if (!ubicacion.value.trim()) {
            alert('Por favor ingresa tu ubicación');
            return;
        }

        try {
            // Deshabilitar el botón y mostrar estado de carga
            const submitButton = form.querySelector('button[type="submit"]');
            submitButton.disabled = true;
            submitButton.textContent = 'Guardando...';

            // Enviar el formulario
            form.submit();
        } catch (error) {
            console.error('Error:', error);
            alert('Hubo un error al guardar tu perfil. Por favor intenta nuevamente.');
            
            // Restaurar el botón
            submitButton.disabled = false;
            submitButton.textContent = 'Continuar';
        }
    });

    // Inicializar la barra de progreso
    updateProgress();
});




