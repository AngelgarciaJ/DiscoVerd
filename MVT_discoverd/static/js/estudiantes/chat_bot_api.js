
// Configuración de la API
const API_KEY = ''; // si quieres que tu chatbot funcione ingresa tu clave del APi AQUi
// Sistema de prompts mejorado
const SYSTEM_PROMPT = `
Eres el asistente virtual oficial de DiscoVerd, una plataforma especializada en eventos universitarios en Perú.

CONTEXTO ESPECÍFICO DE DISCOVERD:
1. Tipos de Eventos:
   - Eventos académicos universitarios
   - Conferencias y seminarios
   - Talleres y capacitaciones
   - Eventos deportivos universitarios
   - Eventos culturales académicos

2. Características de la Plataforma:
   - Sistema de scraping de eventos universitarios
   - Registro de estudiantes y organizadores
   - Publicación y gestión de eventos
   - Sistema de perfiles personalizados
   - Calendario de eventos integrado

CAPACIDADES PRINCIPALES:
1. Navegación y Uso:
   - Explicar el proceso de registro
   - Guiar en la creación de perfil
   - Mostrar cómo buscar eventos
   - Ayudar con la publicación de eventos

2. Información de Eventos:
   - Detalles sobre eventos actuales
   - Requisitos de participación
   - Fechas y ubicaciones
   - Proceso de inscripción

3. Asistencia Técnica:
   - Problemas de acceso
   - Actualización de perfil
   - Gestión de eventos
   - Problemas de registro

4. Recomendaciones:
   - Eventos según intereses
   - Eventos populares
   - Próximos eventos
   - Eventos gratuitos

REGLAS DE RESPUESTA:
1. Mantén respuestas breves y directas (máximo 3 oraciones)
2. Prioriza información específica de DiscoVerd
3. Incluye siempre una acción concreta que el usuario pueda realizar
4. Si no tienes información específica, sugiere consultar la sección relevante de la plataforma

Consulta actual: "{query}"
`;

class ChatBot {
    constructor() {
        this.resultDiv = document.getElementById('result');
        this.searchInput = document.getElementById('searchInput');
        this.searchButton = document.getElementById('searchButton');
        this.suggestedQuestions = [
            "¿Cómo puedo crear un evento?",
            "¿Qué eventos hay disponibles?",
            "¿Cómo me registro en la plataforma?",
            "¿Cómo puedo buscar eventos específicos?",
            "¿Cómo publico un evento?",
            "¿Hay eventos gratuitos disponibles?"
        ];
        this.initialize();
    }

    initialize() {
        if (!this.resultDiv || !this.searchInput || !this.searchButton) {
            console.error('No se encontraron elementos necesarios del chat');
            return;
        }

        // Configurar eventos
        this.searchButton.addEventListener('click', () => this.handleUserInput());
        this.searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.handleUserInput();
        });

        // Mensaje de bienvenida
        this.addMessage('¡Hola! Soy el asistente virtual de DiscoVerd. Puedo ayudarte con información sobre eventos académicos, registro, publicación y más. ¿En qué puedo ayudarte?', false);
        
        // Agregar preguntas sugeridas
        this.addSuggestedQuestions();
    }

    addSuggestedQuestions() {
        const suggestionsDiv = document.createElement('div');
        suggestionsDiv.className = 'suggested-questions';
        
        this.suggestedQuestions.forEach(question => {
            const button = document.createElement('button');
            button.className = 'suggestion-button';
            button.textContent = question;
            button.onclick = () => {
                this.searchInput.value = question;
                this.handleUserInput();
            };
            suggestionsDiv.appendChild(button);
        });

        this.resultDiv.appendChild(suggestionsDiv);
    }

    addMessage(text, isUser = false) {
        if (!this.resultDiv) return;

        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${isUser ? 'user-message' : 'bot-message'}`;
        
        // Formatear links si existen en el texto
        const formattedText = this.formatLinks(text);
        messageDiv.innerHTML = formattedText;
        
        this.resultDiv.appendChild(messageDiv);
        this.resultDiv.scrollTop = this.resultDiv.scrollHeight;
    }

    formatLinks(text) {
        // Convertir URLs en links clickeables
        return text.replace(
            /(https?:\/\/[^\s]+)/g, 
            '<a href="$1" target="_blank" class="chat-link">$1</a>'
        );
    }

    addTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'typing-indicator';
        indicator.innerHTML = `
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        `;
        this.resultDiv.appendChild(indicator);
        return indicator;
    }

    async handleUserInput() {
        if (!this.searchInput || !this.resultDiv) return;

        const query = this.searchInput.value.trim();
        if (!query) return;

        this.addMessage(query, true);
        this.searchInput.value = '';

        try {
            if (!API_KEY || API_KEY === 'TU_API_KEY_AQUI') {
                throw new Error('API key no configurada');
            }

            const typingIndicator = this.addTypingIndicator();

            const response = await this.generateResponse(query);
            
            typingIndicator.remove();
            this.addMessage(response, false);

        } catch (error) {
            console.error('Error en el chatbot:', error);
            
            // Remover indicador de escritura si existe
            const typingIndicator = this.resultDiv.querySelector('.typing-indicator');
            if (typingIndicator) {
                typingIndicator.remove();
            }

            if (error.message === 'API key no configurada') {
                this.addMessage('Error: El chatbot no está configurado correctamente. Por favor, contacta al administrador.', false);
            } else {
                this.addMessage('Lo siento, hubo un problema al procesar tu consulta. Por favor, intenta nuevamente.', false);
            }
        }
    }

    async generateResponse(query) {
        try {
            const response = await fetch(`https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key=${API_KEY}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    contents: [{
                        parts: [{
                            text: SYSTEM_PROMPT.replace('{query}', query)
                        }]
                    }],
                    generationConfig: {
                        temperature: 0.7,
                        topK: 40,
                        topP: 0.95,
                        maxOutputTokens: 500,
                    }
                })
            });

            if (!response.ok) {
                throw new Error(`Error de API: ${response.status}`);
            }

            const data = await response.json();
            return data.candidates[0].content.parts[0].text;

        } catch (error) {
            console.error("Error al conectarse a Gemini:", error);
            throw error;
        }
    }
}

// Estilos CSS necesarios
const styles = `
    .chat-message {
        margin: 4px;
        padding: 5px;
        border-radius: 8px;
        max-width: 80%;
        word-wrap: break-word;
    }

    .user-message {
        background-color: #2196F3;
        color: white;
        margin-left: auto;
    }

    .bot-message {
        background-color: #f0f0f0;
        color: black;
        margin-right: 4px;
    }

    .suggested-questions {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin: 10px;
    }

    .suggestion-button {
        padding: 8px 12px;
        background-color: #e3f2fd;
        color: #2196F3;
        border: 1px solid #2196F3;
        border-radius: 16px;
        cursor: pointer;
        font-size: 0.9em;
        transition: all 0.3s ease;
    }

    .suggestion-button:hover {
        background-color: #2196F3;
        color: white;
    }

    .typing-indicator {
        display: flex;
        gap: 4px;
        padding: 8px;
        margin: 8px;
    }

    .typing-dot {
        width: 8px;
        height: 8px;
        background: #2196F3;
        border-radius: 50%;
        animation: typing 1s infinite ease-in-out;
    }

    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }

    @keyframes typing {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-4px); }
    }

    .chat-link {
        color: #2196F3;
        text-decoration: underline;
    }
`;

// Agregar estilos al documento
document.addEventListener('DOMContentLoaded', () => {
    // Agregar estilos
    const styleSheet = document.createElement('style');
    styleSheet.textContent = styles;
    document.head.appendChild(styleSheet);

    // Inicializar chatbot
    const chatbot = new ChatBot();
});