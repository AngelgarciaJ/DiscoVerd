document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('perfilamientoForm');
    const steps = document.querySelectorAll('.form-step');
    const progressSteps = document.querySelectorAll('.step');
    const nextBtn = document.getElementById('nextBtn');
    const prevBtn = document.getElementById('prevBtn');
    const submitBtn = document.getElementById('submitBtn');
    let currentStep = 0;


    // Agregar este objeto después de ubicacionesPeru
    const facultadesPorUniversidad = {
        'unmsm': [
            'Facultad de Ingeniería de Sistemas e Informática',
            'Facultad de Ingeniería Industrial',
            'Facultad de Ingeniería Electrónica y Eléctrica',
            'Facultad de Ciencias Matemáticas',
            'Facultad de Química e Ingeniería Química',
            'Facultad de Ingeniería Geológica, Minera, Metalúrgica y Geográfica',
            'Facultad de Medicina',
            'Facultad de Derecho y Ciencia Política',
            'Facultad de Letras y Ciencias Humanas',
            'Facultad de Farmacia y Bioquímica',
            'Facultad de Odontología',
            'Facultad de Educación',
            'Facultad de Química e Ingeniería Química',
            'Facultad de Medicina Veterinaria',
            'Facultad de Ciencias Administrativas',
            'Facultad de Ciencias Biológicas',
            'Facultad de Ciencias Contables',
            'Facultad de Ciencias Económicas',
            'Facultad de Ciencias Físicas',
            'Facultad de Ciencias Sociales',
            'Facultad de Psicología'
        ],
        'uni': [
            'Facultad de Arquitectura, Urbanismo y Artes',
            'Facultad de Ciencias',
            'Facultad de Ingeniería Ambiental',
            'Facultad de Ingeniería Civil',
            'Facultad de Ingeniería Económica, Estadística y Ciencias Sociales',
            'Facultad de Ingeniería Eléctrica y Electrónica',
            'Facultad de Ingeniería Geológica, Minera y Metalúrgica',
            'Facultad de Ingeniería Industrial y de Sistemas',
            'Facultad de Ingeniería Mecánica',
            'Facultad de Ingeniería de Petróleo, Gas Natural y Petroquímica',
            'Facultad de Ingeniería Química y Textil'
        ],
        'pucp': [
            'Facultad de Arquitectura y Urbanismo',
            'Facultad de Arte y Diseño',
            'Facultad de Artes Escénicas',
            'Facultad de Ciencias e Ingeniería',
            'Facultad de Ciencias Contables',
            'Facultad de Ciencias Sociales',
            'Facultad de Ciencias y Artes de la Comunicación',
            'Facultad de Derecho',
            'Facultad de Educación',
            'Facultad de Gestión y Alta Dirección',
            'Facultad de Letras y Ciencias Humanas',
            'Facultad de Psicología'
        ]
    };

    // Agregar después del event listener de departamento
    const universidadSelect = document.querySelector('select[name="universidad"]');
    const facultadSelect = document.querySelector('select[name="facultad"]');

    universidadSelect.addEventListener('change', function() {
        facultadSelect.disabled = false;
        facultadSelect.innerHTML = '<option value="">Selecciona tu facultad</option>';
        
        if (this.value && facultadesPorUniversidad[this.value]) {
            facultadesPorUniversidad[this.value].sort().forEach(facultad => {
                const option = document.createElement('option');
                option.value = facultad.toLowerCase().replace(/[^a-zA-Z0-9]+/g, '_');
                option.textContent = facultad;
                facultadSelect.appendChild(option);
            });
        } else {
            facultadSelect.disabled = true;
        }
    });
    // Objeto con las ubicaciones de Perú
    const ubicacionesPeru = {
        'lima': ['Lima', 'Ate', 'Barranco', 'Breña', 'Chorrillos', 'Comas', 'El Agustino', 'Independencia', 
                'Jesús María', 'La Molina', 'La Victoria', 'Lince', 'Los Olivos', 'Magdalena del Mar', 
                'Miraflores', 'Pueblo Libre', 'Puente Piedra', 'Rímac', 'San Borja', 'San Isidro', 
                'San Juan de Lurigancho', 'San Juan de Miraflores', 'San Luis', 'San Martin de Porres', 
                'San Miguel', 'Santa Anita', 'Santiago de Surco', 'Surquillo', 'Villa El Salvador', 
                'Villa María del Triunfo'],
        'arequipa': ['Cercado', 'Alto Selva Alegre', 'Cayma', 'Cerro Colorado', 'Characato', 'Jacobo Hunter',
                     'José Luis Bustamante y Rivero', 'La Joya', 'Mariano Melgar', 'Miraflores', 'Paucarpata',
                     'Sabandia', 'Sachaca', 'Socabaya', 'Tiabaya', 'Uchumayo', 'Yanahuara', 'Yura'],
        'cusco': ['Cusco', 'Ccorca', 'Poroy', 'San Jerónimo', 'San Sebastián', 'Santiago', 'Saylla', 'Wanchaq'],
        'trujillo': ['Trujillo', 'El Porvenir', 'Florencia de Mora', 'Huanchaco', 'La Esperanza', 
                     'Laredo', 'Moche', 'Poroto', 'Salaverry', 'Simbal', 'Victor Larco Herrera'],
        'chiclayo': ['Chiclayo', 'Jose Leonardo Ortiz', 'La Victoria', 'Pimentel', 'Pomalca', 'Monsefú', 
                     'Santa Rosa', 'Reque', 'Eten', 'San José']

    };

    // Función mejorada para validar el paso actual
    function validateStep(step) {
        const inputs = steps[step].querySelectorAll('input[required], select[required]');
        let isValid = true;
        
        // Limpiar mensajes de error previos
        steps[step].querySelectorAll('.is-invalid').forEach(el => {
            el.classList.remove('is-invalid');
        });
        
        inputs.forEach(input => {
            if (!input.value) {
                isValid = false;
                input.classList.add('is-invalid');
                
                // Mostrar mensaje de error específico
                const feedbackEl = input.nextElementSibling;
                if (feedbackEl && feedbackEl.classList.contains('invalid-feedback')) {
                    feedbackEl.style.display = 'block';
                }
            }
        });

        // Validaciones específicas por paso
        if (step === 0) {
            // Validar teléfono
            const telefono = document.querySelector('input[name="telefono"]');
            if (telefono.value && !/^\d{9}$/.test(telefono.value)) {
                isValid = false;
                telefono.classList.add('is-invalid');
            }

            // Validar que se haya seleccionado distrito si hay departamento seleccionado
            const departamento = document.querySelector('select[name="departamento"]');
            const distrito = document.querySelector('select[name="distrito"]');
            if (departamento.value && !distrito.value) {
                isValid = false;
                distrito.classList.add('is-invalid');
            }
        }

        if (step === 1) { // Paso académico
            const universidad = document.querySelector('select[name="universidad"]');
            const facultad = document.querySelector('select[name="facultad"]');
            
            if (universidad.value && !facultad.value) {
                isValid = false;
                facultad.classList.add('is-invalid');
            }
        }

        if (step === 2) {
            // Validar horarios
            const horarios = document.querySelectorAll('input[name="horarios[]"]:checked');
            const availabilityGrid = document.querySelector('.availability-grid');
            if (horarios.length === 0) {
                isValid = false;
                availabilityGrid.classList.add('is-invalid');
                const feedbackEl = availabilityGrid.nextElementSibling;
                if (feedbackEl) feedbackEl.style.display = 'block';
            } else {
                availabilityGrid.classList.remove('is-invalid');
            }



            // Validar modalidad
            const modalidad = document.querySelector('input[name="modalidad"]');
            const participationOptions = document.querySelector('.participation-options');
            if (!modalidad.value) {
                isValid = false;
                participationOptions.classList.add('is-invalid');
                const feedbackEl = participationOptions.nextElementSibling;
                if (feedbackEl) feedbackEl.style.display = 'block';
            } else {
                participationOptions.classList.remove('is-invalid');
            }
        }

        return isValid;
    }

    // Función para mostrar el paso actual y actualizar la barra de progreso
    function showStep(stepNumber) {
        steps.forEach((step, index) => {
            step.classList.remove('active');
            progressSteps[index].classList.remove('active', 'completed');
            if (index < stepNumber) {
                progressSteps[index].classList.add('completed');
            }
        });

        steps[stepNumber].classList.add('active');
        progressSteps[stepNumber].classList.add('active');

        // Actualizar barra de progreso
        const progress = (stepNumber / (steps.length - 1)) * 100;
        document.querySelector('.progress-bar').style.width = `${progress}%`;

        // Actualizar botones
        prevBtn.style.display = stepNumber === 0 ? 'none' : 'block';
        if (stepNumber === steps.length - 1) {
            nextBtn.style.display = 'none';
            submitBtn.style.display = 'block';
        } else {
            nextBtn.style.display = 'block';
            submitBtn.style.display = 'none';
        }
    }

    // Event listeners para navegación
    nextBtn.addEventListener('click', () => {
        if (validateStep(currentStep)) {
            currentStep++;
            showStep(currentStep);
        } else {
            // Mostrar mensaje de error más específico
            const errorMessages = steps[currentStep].querySelectorAll('.invalid-feedback');
            let message = 'Por favor completa los siguientes campos:\n';
            errorMessages.forEach(el => {
                if (el.style.display === 'block') {
                    message += `- ${el.textContent}\n`;
                }
            });
            alert(message);
        }
    });

    prevBtn.addEventListener('click', () => {
        currentStep--;
        showStep(currentStep);
    });

    // Manejar selección de modalidad con feedback visual mejorado
    const participationCards = document.querySelectorAll('.participation-card');
    participationCards.forEach(card => {
        card.addEventListener('click', () => {
            participationCards.forEach(c => c.classList.remove('selected'));
            card.classList.add('selected');
            const modalidadInput = document.querySelector('input[name="modalidad"]');
            modalidadInput.value = card.dataset.value;
            document.querySelector('.participation-options').classList.remove('is-invalid');
        });
    });

    // Manejar selección de departamento y distrito
    const departamentoSelect = document.querySelector('select[name="departamento"]');
    const distritoSelect = document.querySelector('select[name="distrito"]');

    departamentoSelect.addEventListener('change', function() {
        distritoSelect.disabled = false;
        distritoSelect.innerHTML = '<option value="">Selecciona tu distrito</option>';
        
        if (this.value && ubicacionesPeru[this.value]) {
            ubicacionesPeru[this.value].forEach(distrito => {
                const option = document.createElement('option');
                option.value = distrito.toLowerCase().replace(/ /g, '_');
                option.textContent = distrito;
                distritoSelect.appendChild(option);
            });
        }
    });

    // Validación final antes de enviar con mejor manejo de errores
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        if (validateStep(currentStep)) {
            const formData = new FormData(this);
            const submitButton = document.getElementById('submitBtn');
            submitButton.disabled = true;
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Guardando...';

            fetch(this.action, {
                method: 'POST',
                body: formData,
                credentials: 'same-origin'
            })
            .then(response => {
                if (response.ok) {
                    window.location.href = '/estudiantes/completar-perfil/';
                } else {
                    return response.json().then(data => {
                        throw new Error(data.message || 'Error al guardar el perfil');
                    });
                }
            })
            .catch(error => {
                alert('Hubo un error al guardar tu perfil: ' + error.message);
                submitButton.disabled = false;
                submitButton.innerHTML = '<i class="fas fa-check me-2"></i>Completar Perfil';
            });
        }
    });

    // Inicializar el formulario
    showStep(currentStep);
});