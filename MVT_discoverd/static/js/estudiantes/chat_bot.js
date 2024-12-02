// Configuración del chatbot
const API_KEY = 'AIzaSyBvg8VwFkZ7dpCcbSRMeSuqPRH58JNaRtY';

// Objeto con respuestas predefinidas para diferentes tipos de eventos
const eventosRespuestas = {
    bienvenida: [
        "¡Hola! Soy tu asistente virtual especializado en eventos. ¿En qué puedo ayudarte hoy?",
        "¡Bienvenido! Estoy aquí para ayudarte con cualquier consulta sobre eventos. ¿Qué necesitas saber?"
    ],
    despedida: [
        "¡Gracias por tu consulta! No dudes en volver si necesitas más información.",
        "Ha sido un placer ayudarte. ¡Hasta pronto!"
    ],
    noEntiendo: [
        "Lo siento, no he podido entender tu consulta. ¿Podrías reformularla?",
        "Disculpa, ¿podrías explicarme tu pregunta de otra manera?"
    ]
};

async function generarRespuesta(query) {
    try {
        // Primero verificamos si es la primera interacción para mostrar mensaje de bienvenida
        if (!window.chatInitialized) {
            window.chatInitialized = true;
            return eventosRespuestas.bienvenida[Math.floor(Math.random() * eventosRespuestas.bienvenida.length)];
        }

        const response = await fetch(`https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key=${API_KEY}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: `Actúa como un experto en eventos y responde a la siguiente consulta: "${query}".
                              La respuesta debe ser profesional, informativa y útil.`
                    }]
                }]
            })
        });

        if (!response.ok) {
            throw new Error(`Error de API: ${response.status}`);
        }

        const data = await response.json();
        return data.candidates[0].content.parts[0].text;
    } catch (error) {
        console.error("Error al conectarse a Gemini:", error);
        return eventosRespuestas.noEntiendo[Math.floor(Math.random() * eventosRespuestas.noEntiendo.length)];
    }
}

// Función para agregar mensaje al chat
function agregarMensaje(mensaje, esUsuario = false) {
    const chatContainer = document.getElementById("chatContainer");
    const mensajeDiv = document.createElement("div");
    mensajeDiv.className = esUsuario ? "mensaje-usuario" : "mensaje-bot";
    mensajeDiv.textContent = mensaje;
    chatContainer.appendChild(mensajeDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById("chatForm");
    const chatInput = document.getElementById("chatInput");
    const chatContainer = document.getElementById("chatContainer");

    // Mostrar mensaje de bienvenida al cargar la página
    generarRespuesta("").then(mensaje => {
        agregarMensaje(mensaje);
    });

    chatForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const mensaje = chatInput.value.trim();
        
        if (!mensaje) return;

        // Agregar mensaje del usuario
        agregarMensaje(mensaje, true);
        chatInput.value = "";

        // Generar y agregar respuesta del bot
        const respuesta = await generarRespuesta(mensaje);
        agregarMensaje(respuesta);
    });
});