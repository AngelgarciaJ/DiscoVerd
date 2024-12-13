document.addEventListener('DOMContentLoaded', function() {
    // Inicializar filtros
    initializeFiltros();
    
    // Animaciones de entrada
    animateCards();
});

function initializeFiltros() {
    const categoriaFilter = document.getElementById('categoria-filter');
    const fechaFilter = document.getElementById('fecha-filter');
    
    if (categoriaFilter) {
        categoriaFilter.addEventListener('change', filtrarEventos);
    }
    
    if (fechaFilter) {
        fechaFilter.addEventListener('change', filtrarEventos);
    }
}

function filtrarEventos() {
    const categoria = document.getElementById('categoria-filter').value;
    const fecha = document.getElementById('fecha-filter').value;
    const tarjetas = document.querySelectorAll('.tarjeta-evento');
    
    tarjetas.forEach(tarjeta => {
        let mostrar = true;
        
        // Filtro por categoría
        if (categoria && tarjeta.dataset.categoria !== categoria) {
            mostrar = false;
        }
        
        // Filtro por fecha
        if (fecha) {
            const fechaEvento = tarjeta.dataset.fecha;
            if (fechaEvento !== fecha) {
                mostrar = false;
            }
        }
        
        // Aplicar animación de fade
        if (mostrar) {
            tarjeta.style.display = 'grid';
            setTimeout(() => {
                tarjeta.style.opacity = '1';
                tarjeta.style.transform = 'translateY(0)';
            }, 50);
        } else {
            tarjeta.style.opacity = '0';
            tarjeta.style.transform = 'translateY(20px)';
            setTimeout(() => {
                tarjeta.style.display = 'none';
            }, 300);
        }
    });
}

function inscribirEvento(eventoId) {
    // Mostrar indicador de carga
    const boton = event.target;
    boton.disabled = true;
    boton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Inscribiendo...';
    
    fetch(`/eventos/${eventoId}/inscribir/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            mostrarNotificacion('¡Te has inscrito exitosamente!', 'success');
            actualizarBotonInscripcion(eventoId);
        } else {
            mostrarNotificacion(data.message || 'Error al inscribirse', 'error');
            // Restaurar botón
            boton.disabled = false;
            boton.innerHTML = '<i class="fas fa-user-plus"></i> Inscribirse';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        mostrarNotificacion('Error al procesar la solicitud', 'error');
        // Restaurar botón
        boton.disabled = false;
        boton.innerHTML = '<i class="fas fa-user-plus"></i> Inscribirse';
    });
}

function animateCards() {
    const tarjetas = document.querySelectorAll('.tarjeta-evento');
    
    tarjetas.forEach((tarjeta, index) => {
        tarjeta.style.opacity = '0';
        tarjeta.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            tarjeta.style.transition = 'all 0.5s ease';
            tarjeta.style.opacity = '1';
            tarjeta.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

function mostrarNotificacion(mensaje, tipo) {
    const notificacion = document.createElement('div');
    notificacion.className = `notificacion ${tipo}`;
    notificacion.innerHTML = `
        <i class="fas ${tipo === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
        <span>${mensaje}</span>
    `;
    
    document.body.appendChild(notificacion);
    
    setTimeout(() => {
        notificacion.classList.add('mostrar');
    }, 100);
    
    setTimeout(() => {
        notificacion.classList.remove('mostrar');
        setTimeout(() => {
            notificacion.remove();
        }, 300);
    }, 3000);
}

// Función auxiliar para obtener el token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}