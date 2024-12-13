// static/js/estudiantes/privacy_modal.js
window.onload = function() {
    console.log('Página cargada');
    
    // Forzar la creación del modal
    const modal = document.createElement('div');
    modal.className = 'privacy-modal';
    modal.id = 'privacyModal';
    modal.style.display = 'flex'; // Forzar visualización
    
    modal.innerHTML = `
        <div class="modal-content">
            <div class="privacy-header">
                <h2>🔐 Política de Uso y Privacidad</h2>
                <p>Por favor, espere mientras preparamos su sesión...</p>
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
                        <li>Mantener un catálogo actualizado de eventos</li>
                        <li>Proporcionar información relevante a la comunidad</li>
                        <li>Facilitar el acceso a oportunidades académicas</li>
                    </ul>
                </div>

                <div class="privacy-footer">
                    <button type="button" id="acceptButton" class="accept-button">
                        Acepto y deseo continuar
                    </button>
                </div>
            </div>
        </div>
    `;
    
    // Agregar el modal al body
    document.body.appendChild(modal);
    console.log('Modal agregado al DOM');
    
    // Configurar el botón de aceptar
    const acceptButton = document.getElementById('acceptButton');
    if (acceptButton) {
        acceptButton.onclick = function() {
            console.log('Botón aceptar clickeado');
            modal.style.display = 'none';
            modal.remove();
        };
    }
};

// También escuchar DOMContentLoaded por si acaso
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded');
});