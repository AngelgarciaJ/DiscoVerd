document.addEventListener('DOMContentLoaded', function() {
    console.log('Evento.js cargado correctamente');
    
    // Referencia al formulario de crear evento
    const formCrearEvento = document.getElementById('formCrearEvento');
    
    if (formCrearEvento) {
        formCrearEvento.addEventListener('submit', async function(e) {
            e.preventDefault();
            console.log('Formulario enviado');
            
            try {
                const formData = new FormData(this);
                
                const response = await fetch('/organizador/evento/crear/', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                });
                
                const data = await response.json();
                
                if (data.status === 'success') {
                    alert('Evento creado exitosamente');
                    window.location.reload();
                } else {
                    alert('Error: ' + data.message);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error al crear el evento');
            }
        });
    }
});

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