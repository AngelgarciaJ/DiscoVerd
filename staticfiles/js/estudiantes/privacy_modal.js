// Función para obtener el CSRF token
function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            return value;
        }
    }
    return null;
}

// Función para crear el modal
function createPrivacyModal() {
    const modal = document.createElement('div');
    modal.className = 'privacy-modal show';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="privacy-header">
                <h2>🔐 Política de Uso y Privacidad</h2>
                <p>Por favor, espere mientras preparamos su sesión...</p>
            </div>
            
            <div class="loading-indicator">
                <p>⌛ Buscando eventos académicos...</p>
            </div>

            <div class="privacy-content">
                <div class="privacy-warning">
                    <strong>Nota importante:</strong> DiscoVerd está realizando una búsqueda de eventos académicos. 
                    Este proceso puede tomar unos momentos.
                </div>

                <div class="privacy-section">
                    <h3>🎯 Propósito del Scraping</h3>
                    <p>DiscoVerd recopila información de eventos académicos para:</p>
                    <ul>
                        <li>• Mantener un catálogo actualizado de eventos</li>
                        <li>• Proporcionar información relevante a la comunidad</li>
                        <li>• Facilitar el acceso a oportunidades académicas</li>
                    </ul>
                </div>

                <div class="privacy-section">
                    <h3>📋 Normas de Uso</h3>
                    <ul>
                        <li>• La información mostrada es solo para fines académicos</li>
                        <li>• Respetar los derechos de propiedad intelectual</li>
                        <li>• No utilizar la información para fines comerciales</li>
                    </ul>
                </div>

                <div class="privacy-section">
                    <h3>🔒 Compromiso de Privacidad</h3>
                    <ul>
                        <li>• Protegemos la información personal de nuestros usuarios</li>
                        <li>• No compartimos datos con terceros</li>
                        <li>• Cumplimos con las normativas de protección de datos</li>
                    </ul>
                </div>
            </div>

            <div class="privacy-footer">
                <button type="button" class="accept-button">Acepto y deseo continuar</button>
            </div>
        </div>
    `;
    return modal;
}

// Función para inicializar el modal
function initializeModal() {
    try {
        console.log('Inicializando modal...');
        
        // Esperar un momento para asegurarse de que todo esté cargado
        setTimeout(() => {
            if (!sessionStorage.getItem('modalShown')) {
                console.log('Creando nuevo modal...');
                
                const modal = createPrivacyModal();
                document.body.appendChild(modal);
                console.log('Modal agregado al DOM');
                
                const acceptButton = modal.querySelector('.accept-button');
                if (acceptButton) {
                    acceptButton.addEventListener('click', function() {
                        console.log('Botón aceptar clickeado');
                        modal.remove();
                        sessionStorage.setItem('modalShown', 'true');
                    });
                } else {
                    console.error('No se encontró el botón de aceptar');
                }
            } else {
                console.log('Modal ya fue mostrado anteriormente');
            }
        }, 500); // Pequeño retraso para asegurar que el DOM esté listo
    } catch (error) {
        console.error('Error al inicializar el modal:', error.message);
    }
}

// Inicializar cuando el DOM esté completamente cargado
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeModal);
} else {
    initializeModal();
}

// Manejo global de errores
window.addEventListener('error', function(e) {
    console.error('Error en el script:', e.message);
});