import streamlit as st
import matplotlib.pyplot as plt
import time

"""
Resultados de Pronunciación
"""

if "pronunciation_history" not in st.session_state:
    st.session_state.pronunciation_history = []

if "selected_history_item" not in st.session_state:
    st.session_state.selected_history_item = None

MAX_HISTORY = 10

def save_to_history(assessment):
    """Guarda una evaluación en el historial"""
    try:
        result = assessment["result"]

        # Guardar audio_bytes si existe, para grabaciones custom
        audio_bytes = assessment.get("audio_bytes")

        json_result = result.get("json_result", {})
        nbest = json_result.get("NBest", [{}])[0]
        pronunciation = nbest.get("PronunciationAssessment", {})

        entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "phrase": assessment.get("phrase", ""),
            "language": assessment.get("language", ""),
            "pron_score": round(float(pronunciation.get('PronScore', 0)), 1),
            "accuracy_score": round(float(pronunciation.get('AccuracyScore', 0)), 1),
            "fluency_score": round(float(pronunciation.get('FluencyScore', 0)), 1),
            "completeness_score": round(float(pronunciation.get('CompletenessScore', 0)), 1),
            "audio_bytes": audio_bytes,  # << aquí guardas el audio en bytes
            "result": result
        }

        st.session_state.pronunciation_history.insert(0, entry)
        if len(st.session_state.pronunciation_history) > MAX_HISTORY:
            st.session_state.pronunciation_history.pop()

    except Exception as e:
        st.error(f"Error al guardar en historial: {str(e)}")

def display_assessment_results(result, phrase, language):
    """Muestra los resultados de una evaluación"""
    if not result["success"]:
        st.error(f"❌ Error en los resultados: {result.get('error', 'Error desconocido')}")
        return False

    json_result = result.get("json_result", {})
    if not json_result:
        st.error("❌ No se obtuvieron resultados válidos de la evaluación.")
        return False

    nbest = json_result.get("NBest", [{}])[0]
    pronunciation = nbest.get("PronunciationAssessment", {})

    st.subheader("Puntuaciones Generales")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎯 Score General", f"{pronunciation.get('PronScore', 0):.1f}/100")
    with col2:
        st.metric("🎯 Precisión", f"{pronunciation.get('AccuracyScore', 0):.1f}/100")
    with col3:
        st.metric("⚡ Fluidez", f"{pronunciation.get('FluencyScore', 0):.1f}/100")
    with col4:
        st.metric("✅ Completitud", f"{pronunciation.get('CompletenessScore', 0):.1f}/100")

    st.subheader("📈 Análisis Visual")
    fig, ax = plt.subplots(figsize=(10, 4))
    scores = [
        pronunciation.get("PronScore", 0),
        pronunciation.get("AccuracyScore", 0),
        pronunciation.get("FluencyScore", 0),
        pronunciation.get("CompletenessScore", 0)
    ]
    labels = ['General', 'Precisión', 'Fluidez', 'Completitud']
    colors = ['#667eea', '#ff6b6b', '#48dbfb', '#1dd1a1']
    bars = ax.bar(labels, scores, color=colors)
    ax.set_ylim(0, 100)
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height + 1, f'{height:.1f}', ha='center', va='bottom', fontsize=9)
    st.pyplot(fig)
    plt.close()

    # Análisis Detallado por palabra
    st.subheader("Análisis Detallado por Palabra")
    words = nbest.get("Words", [])
    if words:
        for word in words:
            word_text = word.get("Word", "")
            word_assessment = word.get("PronunciationAssessment", {})
            accuracy = word_assessment.get("AccuracyScore", 0)
            error_type = word_assessment.get("ErrorType", "None")
            if accuracy >= 85:
                emoji = "✅"
                status = "Excelente"
            elif accuracy >= 70:
                emoji = "⚠️"
                status = "Bueno"
            else:
                emoji = "❌"
                status = "Necesita mejora"

            with st.expander(f"{emoji} **{word_text}** - {accuracy:.1f}/100 ({status})"):
                st.markdown(f"**Precisión:** {accuracy:.1f}/100")
                st.markdown(f"**Tipo de error:** {error_type if error_type != 'None' else 'Ninguno'}")

    # 💡 Sugerencias
    st.subheader("Sugerencias para Mejorar")
    suggestions = []
    accuracy_score = pronunciation.get("AccuracyScore", 0)
    fluency_score = pronunciation.get("FluencyScore", 0)
    completeness_score = pronunciation.get("CompletenessScore", 0)

    if accuracy_score < 70:
        suggestions.append("🎯 Mejora tu precisión: Algunos sonidos no se pronunciaron claramente...")
    elif accuracy_score < 85:
        suggestions.append("🎯 Refina tu pronunciación: Tu precisión es buena pero puedes mejorar...")
    else:
        suggestions.append("🎯 Excelente precisión: Tu pronunciación es muy clara y precisa...")

    if fluency_score < 60:
        suggestions.append("⚡ Trabaja en fluidez: Hay pausas innecesarias o ritmo irregular...")
    elif fluency_score < 80:
        suggestions.append("⚡ Mejora el ritmo: Buena fluidez pero con algunas interrupciones...")
    else:
        suggestions.append("⚡ Fluidez excelente: Hablas con un ritmo natural y fluido...")

    if completeness_score < 80:
        suggestions.append("✅ Completa todas las palabras: Algunas palabras faltan o no se reconocieron...")
    else:
        suggestions.append("✅ Buena completitud: Pronunciaste todas las palabras del texto...")

    for i, suggestion in enumerate(suggestions, 1):
        st.info(f"**Sugerencia #{i}:** {suggestion}")

    return True

def main():
    st.title("Resultados de Pronunciación")

    # 🔑 Verificar que haya una evaluación reciente o un ítem seleccionado del historial
    if not st.session_state.get("last_assessment") and not st.session_state.pronunciation_history:
        st.info("⚠️ No hay resultados aún. Por favor, graba y evalúa una frase primero.")
        if st.button("🎙️ Practicar una frase", use_container_width=True):
            st.switch_page("pages/1_grabar_audio.py")

        st.stop()  # Detiene la ejecución aquí

    assessment = st.session_state.get("last_assessment")

    # Solo guardar si venimos de una nueva evaluación, no del historial
    if "selected_history_item" not in st.session_state or st.session_state.selected_history_item is None:
        if not st.session_state.pronunciation_history or \
                (st.session_state.pronunciation_history[0].get("audio_bytes") != assessment.get("audio_bytes")):
            save_to_history(assessment)

    if st.session_state.get("selected_history_item") is not None:
        assessment = st.session_state.pronunciation_history[st.session_state.selected_history_item]
    else:
        assessment = st.session_state.last_assessment
        # Aquí solo guardar si es nueva evaluación
        if not st.session_state.pronunciation_history or \
                (st.session_state.pronunciation_history[0].get("audio_bytes") != assessment.get("audio_bytes")):
            save_to_history(assessment)

    phrase = assessment["phrase"]
    language = assessment["language"]
    result = assessment["result"]

    st.markdown(f"**Frase:** `{phrase}`")
    st.markdown(f"**Idioma:** `{language}`")

    display_assessment_results(result, phrase, language)
    audio_bytes = assessment.get("audio_bytes")
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")

    # Navegación
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Practicar Otra Frase", use_container_width=True):
            st.switch_page("pages/1_grabar_audio.py")
    with col2:
        if st.button("Ver Historial", use_container_width=True):
            st.switch_page("pages/3_historial.py")
    with col3:
        if st.button("Volver al Inicio", use_container_width=True):
            st.switch_page("main.py")

if __name__ == "__main__":
    main()

