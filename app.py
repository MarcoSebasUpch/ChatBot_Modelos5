import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

st.set_page_config(page_title="Epicall ChatBot", page_icon="🧠", layout="centered")

# Cargar la API key de forma segura
try:
    load_dotenv()  # Carga variables desde .env si existe (entorno local)
    API_KEY = os.getenv("GROQ_API_KEY")  #para Groq; usar "OPENAI_API_KEY" si es OpenAI
except:
    API_KEY = st.secrets["GROQ_API_KEY"]

os.environ["GROQ_API_KEY"] = API_KEY
client = Groq()  # Cliente para invocar la API de Groq

# Inicializar el historial de chat en la sesión
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # lista de dicts: {"role": ..., "content": ...}

SYSTEM_PROMPT = """
Eres EPICALL_IA, un asistente conversacional de Epicall (startup de salud digital enfocada en epilepsia).
Tu objetivo es informar con claridad y empatía lo que son las epilepsias, habla sobre cómo afectan al paciente y a la familia.
Evita los tecnicismo, se claro y breve.
Ten en cuenta que la startup se basa en que:
- Epicall es un dispositivo de monitoreo y alertas para eventos compatibles con crisis epiléptica.
- Sus beneficios clave son:
  - Monitoreo continuo del estado de la persona.
  - Emisión de alertas automáticas a familiares o cuidadores en caso se detecte una convulsión prolongada (más de 5 minutos).
  - Registro histórico de eventos para mejorar el seguimiento médico.
  - La privacidad y seguridad de los datos está garantizada.
  - Es fácil de usar, ya que consta del dispositivo wearable que es una prenda y de una app
  - Epicall se distingue como el único wearable médico en el país especializado en la monitorización de crisis epilépticas tónico–clónicas y la emisión de alertas ante episodios prolongados.
- Epicall ofrece tranquilidad a las familias al reducir tiempos de respuesta en emergencias.
- En caso de ventas indica que se realiza en todo el Perú, siendo tu sede principal en Lima, desde harás los envíos. 
- Permites brindar un soporte técnico, el dispositivo es electrónico, por lo que debes dar recomendaciones básicas. Cuando las termines de dar indica que, en casos más específicos, llamar al 966990206.

Ten en cuenta que solo vendes el dispositivo, no puedes dar consejos médicos ni algún tratamiento, Epicall no reemplaza la atención médica, sino que la complementa.
"""

st.title("🧠 Epicall IA - Tu Aliado en Epilepsia")
st.write("Monitoreo continuo y alertas inteligentes para cuidar a quienes más quieres. Pregunta lo que desees.")

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Escribe tu pregunta aquí...")

if user_input:
    # Mostrar el mensaje del usuario
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Construir mensajes para el modelo
    messages = []
    if SYSTEM_PROMPT:
        messages.append({"role": "system", "content": SYSTEM_PROMPT})
    messages.extend(st.session_state.chat_history)

    # Llamar a la API **solo** si hay user_input (evita NameError)
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7,
        )
        respuesta_texto = response.choices[0].message.content  # objeto, no dict
    except Exception as e:
        respuesta_texto = f"Lo siento, ocurrió un error al llamar a la API: `{e}`"

    # Mostrar respuesta del asistente
    with st.chat_message("assistant"):
        st.markdown(respuesta_texto)

    # Guardar en historial
    st.session_state.chat_history.append({"role": "assistant", "content": respuesta_texto})





