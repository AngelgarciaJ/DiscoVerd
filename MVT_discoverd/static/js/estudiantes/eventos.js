// Funciones principales para manejo de eventos
document.addEventListener('DOMContentLoaded', function() {
    initializeEventHandlers();
});

function initializeEventHandlers() {
    // Manejadores para inscripción
    const inscriptionButtons = document.querySelectorAll('.btn-inscribirse');
    inscriptionButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const eventoId = e.target.dataset.eventoId;
            confirmarInscripcion(eventoId);
        });
    });

    // Manejadores para compartir
    setupShareButtons();
}

function confirmarInscripcion(eventoId) {
    try {
        fetch(`/eventos/${eventoId}/inscribir/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) throw new Error('Error en la respuesta del servidor');
            return response.json();
        })
        .then(data => {
            if (data.success) {
                mostrarNotificacion('Inscripción exitosa', 'success');
                location.reload();
            } else {
                mostrarNotificacion(data.message || 'Error al inscribirse', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            mostrarNotificacion('Error al procesar la solicitud', 'error');
        });
    } catch (error) {
        console.error('Error:', error);
        mostrarNotificacion('Error al procesar la solicitud', 'error');
    }
}

function cancelarInscripcion(eventoId) {
    if (confirm('¿Estás seguro que deseas cancelar tu inscripción?')) {
        fetch(`/eventos/${eventoId}/cancelar/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                mostrarNotificacion('Inscripción cancelada', 'success');
                location.reload();
            } else {
                mostrarNotificacion('Error al cancelar inscripción', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            mostrarNotificacion('Error al cancelar inscripción', 'error');
        });
    }
}

// Utilidades
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

function mostrarNotificacion(mensaje, tipo = 'info') {
    const notificacion = document.createElement('div');
    notificacion.className = `notificacion ${tipo}`;
    notificacion.textContent = mensaje;
    
    document.body.appendChild(notificacion);
    
    setTimeout(() => {
        notificacion.classList.add('fadeOut');
        setTimeout(() => {
            notificacion.remove();
        }, 300);
    }, 3000);
}

function setupShareButtons() {
    document.querySelectorAll('.share-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const platform = this.dataset.platform;
            const url = encodeURIComponent(window.location.href);
            const title = encodeURIComponent(document.title);
            
            let shareUrl;
            switch(platform) {
                case 'facebook':
                    shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${url}`;
                    break;
                case 'twitter':
                    shareUrl = `https://twitter.com/intent/tweet?url=${url}&text=${title}`;
                    break;
                case 'whatsapp':
                    shareUrl = `https://wa.me/?text=${title}%20${url}`;
                    break;
            }
            
            window.open(shareUrl, '_blank', 'width=600,height=400');
        });
    });
}

// Funciones de filtrado
function initializeFilters() {
    const categoriaFilter = document.getElementById('categoria-filter');
    const fechaFilter = document.getElementById('fecha-filter');
    
    if (categoriaFilter) {
        categoriaFilter.addEventListener('change', aplicarFiltros);
    }
    if (fechaFilter) {
        fechaFilter.addEventListener('change', aplicarFiltros);
    }
}

function aplicarFiltros() {
    const categoria = document.getElementById('categoria-filter').value;
    const fecha = document.getElementById('fecha-filter').value;
    
    const eventos = document.querySelectorAll('.event-card');
    eventos.forEach(evento => {
        const categoriaEvento = evento.dataset.categoria;
        const fechaEvento = evento.dataset.fecha;
        
        let mostrar = true;
        
        if (categoria && categoriaEvento !== categoria) {
            mostrar = false;
        }
        
        if (fecha && fechaEvento !== fecha) {
            mostrar = false;
        }
        
        evento.style.display = mostrar ? 'block' : 'none';
    });
}