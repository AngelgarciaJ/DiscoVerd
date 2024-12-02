function inscribirEvento(eventoId) {
    document.getElementById('confirmationModal').style.display = 'block';
    window.eventoIdTemp = eventoId;
}

function confirmarInscripcion() {
    const eventoId = window.eventoIdTemp;
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
            location.reload();
        } else {
            mostrarNotificacion('Error al inscribirse', 'error');
        }
    });
    cerrarModal();
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
                location.reload();
            } else {
                mostrarNotificacion('Error al cancelar inscripción', 'error');
            }
        });
    }
}

function cerrarModal() {
    document.getElementById('confirmationModal').style.display = 'none';
}

// Compartir en redes sociales
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