document.addEventListener('DOMContentLoaded', function() {
    const DAYS_INTERVAL = 1; // Intervalo de 1 día
    
    function shouldShowModal() {
        const lastShown = sessionStorage.getItem('lastShownWelcome');
        
        if (!lastShown) {
            return true;
        }
        
        const lastShownDate = new Date(parseInt(lastShown));
        const currentDate = new Date();
        
        // Verificar si es un nuevo día
        return lastShownDate.toDateString() !== currentDate.toDateString();
    }
    
    function createModal() {
        const modal = document.createElement('div');
        modal.className = 'welcome-modal';
        
        modal.innerHTML = `
            <div class="modal-content">
                <img src="/static/img/estudiantes/lecture-3986809_1280.jpg" alt="Bienvenida a DiscoVerd" class="welcome-image">
                <div class="modal-header">
                    <h2>¡Bienvenido a DiscoVerd! 🌟</h2>
                    <p>Conéctate, Comparte y Crea Impacto</p>
                </div>
                
                <p>Estamos encantados de tenerte aquí. En nuestra plataforma, puedes descubrir y crear eventos que inspiren, conecten y fortalezcan nuestra comunidad.</p>
                
                <div class="rules-section">
                    <h3>Normas de Publicación en DiscoVerd 📝</h3>
                    <ul class="rules-list">
                        <li>🚫 No se permiten contenidos ofensivos, racistas, violentos, discriminatorios u obscenos.</li>
                        <li>✅ Todos los eventos deben promover valores de respeto, inclusión y aprendizaje.</li>
                        <li>🕵️‍♂️ Los eventos publicados serán revisados antes de su aprobación, IMPORTANTE:Los eventos tienen que ser creados con 2 dias de antipacion a mas, caso contrario nose publicara el evento. </li>
                        
                    </ul>
                </div>
                
                <p><strong>Recuerda:</strong> El incumplimiento de estas normas puede llevar a la eliminación de tu evento o, en casos graves, a la suspensión de tu cuenta. Ayúdanos a construir una comunidad positiva para todos. 💙</p>
                
                <p>Si necesitas ayuda, ¡estamos aquí para apoyarte! 🌐</p>
                
                <div class="modal-footer">
                    <button class="start-button">¡Entendido! 🚀</button>
                    <label class="dont-show-again">
                        <input type="checkbox" id="dontShowToday">
                        No mostrar más por hoy
                    </label>
                </div>
            </div>
        `;
        
        return modal;
    }
    
    function showModal() {
        const modal = createModal();
        document.body.appendChild(modal);
        
        // Mostrar el modal con una pequeña demora para la animación
        setTimeout(() => {
            modal.classList.add('show');
        }, 100);
        
        // Manejar el cierre del modal
        const closeButton = modal.querySelector('.start-button');
        const dontShowCheckbox = modal.querySelector('#dontShowToday');
        
        closeButton.addEventListener('click', function() {
            modal.classList.remove('show');
            setTimeout(() => {
                modal.remove();
            }, 300);
            
            if (dontShowCheckbox.checked) {
                // Guardar la fecha actual en sessionStorage
                sessionStorage.setItem('lastShownWelcome', Date.now().toString());
            }
        });
    }
    
    // Verificar si debemos mostrar el modal
    if (shouldShowModal()) {
        showModal();
    }
});