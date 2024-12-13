function redirectToHome() {
    window.location.href = 'LandingPage_orga.html';
}

function goToHome() {
    window.location.href = 'LandingPage_orga.html';
}

document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('modalCrearEvento');
    const btnNuevoEvento = document.querySelector('.btn-nuevo-evento');
    const span = document.getElementsByClassName('close')[0];
    const form = document.getElementById('formCrearEvento');

    // Abrir modal
    btnNuevoEvento.onclick = function() {
        modal.style.display = "block";
    }

    // Cerrar modal
    span.onclick = function() {
        modal.style.display = "none";
    }

    // Cerrar modal al hacer clic fuera
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    // Manejar envío del formulario
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const formData = new FormData(form);

        try {
            const response = await fetch('/crear-evento/', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.status === 'success') {
                alert('¡Evento creado exitosamente!');
                modal.style.display = "none";
                form.reset();
                // Recargar la página para mostrar el nuevo evento
                window.location.reload();
            } else {
                alert('Error al crear el evento: ' + data.message);
            }
        } catch (error) {
            alert('Error al crear el evento: ' + error.message);
        }
    });
});

// Función para eliminar eventos pasados
async function limpiarEventosPasados() {
    try {
        const response = await fetch('/limpiar-eventos-pasados/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
        });

        const data = await response.json();
        if (data.status === 'success') {
            console.log('Eventos pasados eliminados');
        }
    } catch (error) {
        console.error('Error al limpiar eventos:', error);
    }
}

// Ejecutar limpieza de eventos pasados cada día
setInterval(limpiarEventosPasados, 24 * 60 * 60 * 1000);

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