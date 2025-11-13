import streamlit as st
from app.services.speech import PronunciationEvaluator

st.set_page_config(
    page_title="🗣️ Tutor de Pronunciación",
    page_icon="🗣️",
    layout="wide"
)

st.title("🗣️ Tutor de Pronunciación Multilingüe")

evaluator = PronunciationEvaluator()
config_status = evaluator.get_configuration_status()

if config_status["status"] == "error":
    st.error(config_status["message"])
    st.info("⚙️ Ve a tu archivo `.env` o `secrets.toml` para agregar las credenciales.")
    st.stop()
else:
    st.success(config_status["message"])

st.markdown(
    """
    Bienvenido a tu **asistente inteligente de pronunciación**.
    Esta app utiliza inteligencia artificial de **Azure Speech Services**
    para evaluar tu pronunciación en distintos idiomas 🌍.

    ---
    ### 🧩 Características destacadas
    - 🎤 **Grabación en tiempo real** o subida de archivos `.wav`
    - 📊 **Análisis detallado** con puntuación fonética
    - 🕓 **Historial automático** de tus últimas sesiones
    - 💡 **Consejos personalizados** según tus resultados
    - 🌐 Soporte completo para **Inglés, Español, Francés, Alemán e Italiano**
    ---
    """
)


st.subheader("🚀 Elige una acción para comenzar")

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("### 🎙️ Grabar Audio")
    st.markdown("Graba tu voz directamente desde el navegador y practica frases seleccionadas.")
    if st.button("Ir a Grabar", use_container_width=True, type="primary"):
        st.switch_page("pages/1_grabar_audio.py")

with col2:
    st.markdown("### 📊 Resultados")
    st.markdown("Consulta los análisis detallados de tu pronunciación más reciente.")
    if st.button("Ver Resultados", use_container_width=True):
        st.switch_page("pages/2_resultados.py")

with col3:
    st.markdown("### 🕓 Historial")
    st.markdown("Explora tus evaluaciones anteriores y sigue tu progreso.")
    if st.button("Ver Historial", use_container_width=True):
        st.switch_page("pages/3_historial.py")
