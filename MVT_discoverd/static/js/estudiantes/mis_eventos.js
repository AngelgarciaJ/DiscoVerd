// eventos.js
function inscribirEvento(eventoId) {
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
            mostrarNotificacion('Te has inscrito exitosamente', 'success');
            actualizarBotonInscripcion(eventoId);
        } else {
            mostrarNotificacion('Error al inscribirse', 'error');
        }
    });
}

function filtrarEventos() {
    const categoria = document.getElementById('categoria-filter').value;
    const fecha = document.getElementById('fecha-filter').value;
    
    document.querySelectorAll('.event-card').forEach(card => {
        let mostrar = true;
        
        if (categoria && card.dataset.categoria !== categoria) {
            mostrar = false;
        }
        
        if (mostrar) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// Inicializar filtros
document.addEventListener('DOMContentLoaded', function() {
    const categoriaFilter = document.getElementById('categoria-filter');
    const fechaFilter = document.getElementById('fecha-filter');
    
    if (categoriaFilter) categoriaFilter.addEventListener('change', filtrarEventos);
    if (fechaFilter) fechaFilter.addEventListener('change', filtrarEventos);
});