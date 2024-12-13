document.addEventListener('DOMContentLoaded', function() {
    // Verificar si el usuario ya vio el mensaje
    if (!localStorage.getItem('hasSeenWelcome')) {
        // Crear el modal
        const modal = document.createElement('div');
        modal.className = 'welcome-modal';
        
        // Contenido del modal
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
                        <li>🕵️‍♂️ Los eventos publicados serán revisados antes de su aprobación.</li>
                    </ul>
                </div>
                
                <p><strong>Recuerda:</strong> El incumplimiento de estas normas puede llevar a la eliminación de tu evento o, en casos graves, a la suspensión de tu cuenta. Ayúdanos a construir una comunidad positiva para todos. 💙</p>
                
                <p>Si necesitas ayuda, ¡estamos aquí para apoyarte! 🌐</p>
                
                <div class="modal-footer">
                    <button class="start-button">¡Empecemos! 🚀</button>
                </div>
            </div>
        `;

        // Añadir el modal al body
        document.body.appendChild(modal);

        // Mostrar el modal con una pequeña demora para la animación
        setTimeout(() => {
            modal.classList.add('show');
        }, 100);

        // Manejar el cierre del modal
        const closeButton = modal.querySelector('.start-button');
        closeButton.addEventListener('click', function() {
            modal.classList.remove('show');
            setTimeout(() => {
                modal.remove();
            }, 300);
            localStorage.setItem('hasSeenWelcome', 'true');
        });
    }
});