// Debugging y funciones principales del modal
let modalVisible = false;

function showPoliticasModal() {
    console.log('Intentando mostrar el modal');
    const modal = document.getElementById('modalPoliticas');
    
    if (!modal) {
        console.error('Modal no encontrado, creando dinámicamente');
        createModal();
        return;
    }
    
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    modalVisible = true;
    console.log('Modal mostrado correctamente');
}

function closePoliticasModal() {
    const modal = document.getElementById('modalPoliticas');
    if (modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = 'auto';
        modalVisible = false;
    }
}

function createModal() {
    const modalHTML = `
        <div id="modalPoliticas" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div class="relative top-20 mx-auto p-5 border w-full max-w-xl shadow-lg rounded-md bg-white">
                <div class="flex flex-col">
                    <!-- Encabezado -->
                    <div class="flex justify-between items-center pb-3">
                        <div class="text-xl font-bold text-gray-700">
                            <i class="fas fa-info-circle text-blue-500 mr-2"></i>
                            Acerca de DiscoVerd
                        </div>
                        <button onclick="closePoliticasModal()" class="text-gray-400 hover:text-gray-500">
                            <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                            </svg>
                        </button>
                    </div>

                    <!-- Contenido -->
                    <div class="mt-4">
                        <div class="bg-blue-50 p-4 rounded-lg mb-4">
                            <h3 class="text-lg font-semibold text-blue-800 mb-2">Sobre Nosotros</h3>
                            <p class="text-blue-700">
                                DiscoVerd es una plataforma diseñada para conectar a la comunidad universitaria 
                                a través de eventos educativos, culturales y profesionales.
                            </p>
                        </div>

                        <div class="bg-gray-50 p-4 rounded-lg">
                            <h3 class="text-lg font-semibold text-gray-800 mb-2">Normas de Publicación 📝</h3>
                            <ul class="space-y-2 text-gray-600">
                                <li class="flex items-start">
                                    <span class="text-red-500 mr-2">🚫</span>
                                    No se permiten contenidos ofensivos o discriminatorios
                                </li>
                                <li class="flex items-start">
                                    <span class="text-green-500 mr-2">✅</span>
                                    Los eventos deben promover valores positivos
                                </li>
                                <li class="flex items-start">
                                    <span class="text-blue-500 mr-2">🕵️‍♂️</span>
                                    Los eventos serán revisados antes de su aprobación
                                </li>
                            </ul>
                        </div>
                    </div>

                    <!-- Pie -->
                    <div class="flex justify-end pt-4">
                        <button onclick="closePoliticasModal()" 
                                class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
                            Entendido
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;

    const modalElement = document.createElement('div');
    modalElement.innerHTML = modalHTML;
    document.body.appendChild(modalElement.firstElementChild);
    
    // Mostrar el modal después de crearlo
    setTimeout(showPoliticasModal, 100);
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded - Inicializando modal de políticas');
    
    const politicasBtn = document.getElementById('politicasBtn');
    if (politicasBtn) {
        politicasBtn.addEventListener('click', showPoliticasModal);
        console.log('Event listener agregado al botón de políticas');
    }

    // Manejador para cerrar el modal al hacer clic fuera
    document.addEventListener('click', function(e) {
        const modal = document.getElementById('modalPoliticas');
        if (modal && modalVisible && e.target === modal) {
            closePoliticasModal();
        }
    });
});