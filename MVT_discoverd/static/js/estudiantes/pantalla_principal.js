document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    const eventosDestacados = document.getElementById('eventos-destacados');
    const proximosEventos = document.getElementById('proximos-eventos');
    const cardTemplate = document.getElementById('event-card-template');

    async function handleSearch(e) {
        e.preventDefault();
        const searchTerm = e.target.search.value.trim();
        
        showLoading();

        try {
            const response = await fetch('/estudiantes/estudiantes/buscar-eventos/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({ query: searchTerm })
            });

            const data = await response.json();
            console.log('Datos recibidos:', data);

            if (data.status === 'success') {
                renderEventos(data.eventos_destacados || [], data.proximos_eventos || []);
            } else {
                showError('Error al buscar eventos: ' + (data.message || 'Error desconocido'));
            }
        } catch (error) {
            console.error('Error en la búsqueda:', error);
            showError('Error al conectar con el servidor');
        } finally {
            hideLoading();
        }
    }

    function createEventCard(evento, isDestacado) {
        if (!cardTemplate) return '';
        
        const template = cardTemplate.content.cloneNode(true);
        const card = template.querySelector('.event-card');
        
        try {
            // Manejo mejorado de imágenes
            const img = card.querySelector('.event-image');
            if (img) {
                let imageUrl = evento.imagen_url;
                
                // Verificar si la URL es absoluta
                if (imageUrl && !imageUrl.startsWith('http') && !imageUrl.startsWith('/')) {
                    // Si la imagen está en media/temp_eventos
                    if (imageUrl.includes('temp_eventos')) {
                        imageUrl = '/media/' + imageUrl;
                    } else {
                        // Para otras imágenes locales
                        imageUrl = '/media/temp_eventos/' + imageUrl;
                    }
                }
                
                console.log('URL de imagen procesada:', imageUrl);
                
                // Configurar imagen con fallback
                img.src = imageUrl || '/static/img/default-header.jpg';
                img.alt = evento.titulo || 'Imagen del evento';
                img.onerror = function() {
                    console.log('Fallback: Cargando imagen por defecto');
                    this.src = '/static/img/default-header.jpg';
                    this.onerror = null; // Prevenir bucle infinito
                };
            }

            // Resto de la información del evento
            if (isDestacado) {
                const badge = card.querySelector('.event-badge');
                if (badge) {
                    badge.style.display = 'block';
                }
            } else {
                const badge = card.querySelector('.event-badge');
                if (badge) {
                    badge.style.display = 'none';
                }
            }

            const title = card.querySelector('.event-title');
            if (title) {
                title.textContent = evento.titulo || 'Evento sin título';
            }

            const description = card.querySelector('.event-description');
            if (description) {
                description.textContent = evento.descripcion || 'Sin descripción disponible';
            }

            const date = card.querySelector('.event-date');
            if (date) {
                const formattedDate = evento.fecha ? new Date(evento.fecha).toLocaleDateString() : 'Fecha por confirmar';
                date.innerHTML = `
                    <i class="far fa-calendar-alt mr-2"></i>
                    <span>${formattedDate}</span>
                `;
            }

            const verMasBtn = card.querySelector('.view-more-button');
            if (verMasBtn) {
                verMasBtn.onclick = function(e) {
                    e.preventDefault();
                    window.location.href = `/estudiantes/eventos/${evento.id}`;
                };
            }

            return card.outerHTML;
        } catch (error) {
            console.error('Error al crear tarjeta de evento:', error);
            return `
                <div class="event-card bg-white rounded-lg shadow-lg p-4">
                    <p class="text-red-600">Error al cargar el evento: ${error.message}</p>
                </div>
            `;
        }
    }

    function renderEventos(destacados = [], proximos = []) {
        console.log('Renderizando eventos destacados:', destacados);
        console.log('Renderizando próximos eventos:', proximos);

        if (destacados.length > 0) {
            eventosDestacados.innerHTML = destacados
                .map(evento => createEventCard(evento, true))
                .join('');
        } else {
            showMessage(eventosDestacados, 'No se encontraron eventos destacados');
        }

        if (proximos.length > 0) {
            proximosEventos.innerHTML = proximos
                .map(evento => createEventCard(evento, false))
                .join('');
        } else {
            showMessage(proximosEventos, 'No se encontraron próximos eventos');
        }
    }

    // Funciones auxiliares existentes...
    function showLoading() {
        const loadingHTML = '<div class="loading p-4 text-center"><i class="fas fa-spinner fa-spin mr-2"></i>Cargando eventos...</div>';
        eventosDestacados.innerHTML = loadingHTML;
        proximosEventos.innerHTML = loadingHTML;
    }

    function hideLoading() {
        const loadings = document.querySelectorAll('.loading');
        loadings.forEach(loading => loading.remove());
    }

    function showMessage(container, message, type = 'info') {
        container.innerHTML = `
            <div class="message ${type} p-4 rounded-lg">
                <p class="text-center">${message}</p>
            </div>
        `;
    }

    function showError(message) {
        showMessage(eventosDestacados, message, 'error');
        showMessage(proximosEventos, message, 'error');
    }

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    // Event listeners
    searchForm.addEventListener('submit', handleSearch);
});