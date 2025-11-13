import streamlit as st
import matplotlib.pyplot as plt


"""
Historial de Pronunciación
"""


st.title("Historial de Pronunciación")

st.set_page_config(
    page_title="Historial de Evaluaciones",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar historial si no existe
if "pronunciation_history" not in st.session_state:
    st.session_state.pronunciation_history = []

history = st.session_state.pronunciation_history

if not history:
    st.info("No hay evaluaciones guardadas. Ve a **Grabar Audio**.")
    if st.button("🎙️ Ir a Grabar Audio", use_container_width=True):
        st.switch_page("pages/1_grabar_audio.py")
    st.stop()

# Crear tabs para cada evaluación
tab_labels = [
    f"{i+1}. {e['timestamp'].split()[1]} - {e['pron_score']}/100"
    for i, e in enumerate(history)
]
tabs = st.tabs(tab_labels)

for i, (tab, entry) in enumerate(zip(tabs, history)):
    with tab:
        st.markdown(f"### Fecha: `{entry.get('timestamp','')}`")
        st.markdown(f"**Frase:** `{entry.get('phrase','')}`")
        st.markdown(f"**Idioma:** `{entry.get('language','')}`")
        st.markdown(f"**Score General:** `{entry.get('pron_score',0)}/100`")

        scores = [
            entry.get('pron_score', 0),
            entry.get('accuracy_score', 0),
            entry.get('fluency_score', 0),
            entry.get('completeness_score', 0)
        ]
        labels = ['General', 'Precisión', 'Fluidez', 'Completitud']

        # Gráfico de puntuaciones
        fig, ax = plt.subplots(figsize=(6, 2))
        ax.bar(labels, scores, color=['#667eea', '#ff6b6b', '#48dbfb', '#1dd1a1'])
        ax.set_ylim(0, 100)
        ax.set_title('Resumen de puntuaciones', fontsize=9)
        for idx, val in enumerate(scores):
            ax.text(idx, val + 1, f"{val:.1f}", ha='center', va='bottom', fontsize=9)
        st.pyplot(fig)
        plt.close()

        # Reproducir audio (bytes) si existe
        audio_bytes = entry.get("audio_bytes")
        if audio_bytes:
            st.audio(audio_bytes, format="audio/wav")

        if st.button("Ver resultados de esta evaluación concreta", key=f"to_result_{i}"):
            st.session_state.last_assessment = entry
            st.session_state.selected_history_item = i

            st.switch_page("pages/2_resultados.py")

            st.rerun()


st.markdown("---")

# Navegación
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🎙️ Practicar Otra Frase", use_container_width=True):
        st.switch_page("pages/1_grabar_audio.py")
with col2:
    if st.button("🏠 Volver al Inicio", use_container_width=True):
        st.switch_page("main.py")
