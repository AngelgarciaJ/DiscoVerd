document.addEventListener('DOMContentLoaded', function() {
    // Validación de fechas y horas
    const fechaInput = document.getElementById('fecha');
    const horaInicioInput = document.getElementById('hora_inicio');
    const horaFinInput = document.getElementById('hora_fin');

    // Establecer fecha mínima como hoy
    const today = new Date().toISOString().split('T')[0];
    fechaInput.setAttribute('min', today);

    // Validar que la fecha no sea anterior a hoy
    fechaInput.addEventListener('change', function() {
        const selectedDate = new Date(this.value);
        const today = new Date();
        today.setHours(0, 0, 0, 0);

        if (selectedDate < today) {
            alert('La fecha no puede ser anterior a hoy');
            this.value = today.toISOString().split('T')[0];
        }
    });

    // Validar que hora fin sea posterior a hora inicio
    function validarHoras() {
        if (horaInicioInput.value && horaFinInput.value) {
            if (horaFinInput.value <= horaInicioInput.value) {
                alert('La hora de fin debe ser posterior a la hora de inicio');
                horaFinInput.value = '';
            }
        }
    }

    horaInicioInput.addEventListener('change', validarHoras);
    horaFinInput.addEventListener('change', validarHoras);

    // Validación de imagen
    const imagenInput = document.getElementById('imagen');
    imagenInput.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            // Validar tamaño (5MB máximo)
            if (file.size > 5 * 1024 * 1024) {
                alert('La imagen no debe superar los 5MB');
                this.value = '';
                return;
            }

            // Validar tipo
            if (!file.type.startsWith('image/')) {
                alert('Por favor, seleccione un archivo de imagen válido');
                this.value = '';
                return;
            }
        }
    });

    // Prevenir envío accidental del formulario
    document.querySelector('form').addEventListener('submit', function(e) {
        const requiredFields = this.querySelectorAll('[required]');
        let valid = true;

        requiredFields.forEach(field => {
            if (!field.value) {
                valid = false;
                field.classList.add('border-red-500');
            } else {
                field.classList.remove('border-red-500');
            }
        });

        if (!valid) {
            e.preventDefault();
            alert('Por favor, complete todos los campos requeridos');
        }
    });
});