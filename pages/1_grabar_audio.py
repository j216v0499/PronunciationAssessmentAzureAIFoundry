import time

import streamlit as st
import tempfile
import os
import hashlib

from app.services.speech import PronunciationEvaluator
from app.utils.validation import validate_audio_file
from app.utils.languages_phrases import LANGUAGE_OPTIONS,EXAMPLE_PHRASES
from audio_recorder_streamlit import audio_recorder

"""
Grabacion de audio
"""

# Iniciar evaluador de pronunciación
@st.cache_resource
def get_evaluator():
    return PronunciationEvaluator()

evaluator = get_evaluator()
@st.cache_data(ttl=300)
def cached_evaluate(audio_bytes: bytes, phrase: str, language_code: str):
    """
    Evalúa la pronunciación y cachea solo los datos serializables (JSON).
    """
    # Crear hash único
    h = hashlib.sha256()
    h.update(audio_bytes)
    h.update(phrase.encode('utf-8'))
    h.update(language_code.encode('utf-8'))

    # Llamar al evaluador
    result = evaluator.evaluate_pronunciation_bytes(audio_bytes, phrase, language_code)

    # Retornar solo datos serializables
    return {
        "success": result.get("success"),
        "error": result.get("error"),
        "json_result": result.get("json_result")  # Esto es un dict serializable
    }


# Validación de audio en bytes
def validate_audio_bytes(audio_bytes: bytes):
    """
    Valida audio convirtiéndolo temporalmente a archivo WAV
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(audio_bytes)
        tmp_path = tmp_file.name
    try:
        return validate_audio_file(tmp_path)
    finally:
        # Borrar temporal
        import os
        os.unlink(tmp_path)


def main():
    st.title("🗣️ Grabar Pronunciación")

    # Selección de idioma
    st.subheader("🌍 Selecciona el idioma")
    selected_language = st.selectbox("Idioma para practicar:", list(LANGUAGE_OPTIONS.keys()))
    language_code = LANGUAGE_OPTIONS[selected_language]

    # Selección de frase
    st.subheader("Selecciona una frase genérica para practicar")
    selected_phrase = st.selectbox("Frase modelo:", EXAMPLE_PHRASES[language_code])
    custom_phrase = st.text_input("O escribe una frase propia:", "")
    if custom_phrase.strip():
        selected_phrase = custom_phrase

    st.markdown(f"**Frase seleccionada:** `{selected_phrase}`")

    # Tabs para audio
    tab1, tab2 = st.tabs(["Grabar audio","Subir archivo"])



    # ------------------ TAB 1: Grabar audio ------------------
    with tab1:
        st.subheader("Graba tu pronunciación")
        st.info("Pulsa el botón para grabar y luego evaluarla con Azure.")

        if "audio_bytes" not in st.session_state:
            st.session_state.audio_bytes = None
        if "recording_done" not in st.session_state:
            st.session_state.recording_done = False

        audio_bytes = audio_recorder(
            text="🎙️ Presiona para grabar / detener  -->",
            recording_color="#ef233c",
            neutral_color="#457b9d",
            icon_name="microphone",
            icon_size="3x",
            sample_rate=16000,
        )

        # Guardar nueva grabación
        if audio_bytes:
            st.session_state.audio_bytes = audio_bytes
            st.session_state.recording_done = True

        if st.session_state.audio_bytes is not None or st.session_state.recording_done:
            st.success("✅ Grabación completada")
            st.audio(st.session_state.audio_bytes, format="audio/wav")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("🗑️ Eliminar grabación", use_container_width=True):
                    st.session_state.audio_bytes = None
                    st.warning("Grabación eliminada")
                    st.stop()

            with col2:
                if st.button("Evaluar Pronunciación", use_container_width=True, key="record_eval"):
                    validation = validate_audio_bytes(st.session_state.audio_bytes)
                    if validation["valid"]:
                        with st.spinner("Analizando pronunciación..."):
                            try:
                                result = cached_evaluate(st.session_state.audio_bytes,
                                                         selected_phrase,
                                                         language_code)
                                if result["success"]:
                                    st.session_state.last_assessment = {
                                        "phrase": selected_phrase,
                                        "language": language_code,
                                        "result": result,
                                        "audio_bytes": st.session_state.audio_bytes
                                    }
                                    st.success("¡Evaluación completada!")
                                    st.balloons()

                                    if "pronunciation_history" not in st.session_state:
                                        st.session_state.pronunciation_history = []

                                    json_result = result.get("json_result", {})
                                    nbest = json_result.get("NBest", [{}])[0]
                                    pron = nbest.get("PronunciationAssessment", {})

                                    entry = {
                                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                                        "phrase": selected_phrase,
                                        "language": language_code,
                                        "pron_score": round(pron.get("PronScore", 0), 1),
                                        "accuracy_score": round(pron.get("AccuracyScore", 0), 1),
                                        "fluency_score": round(pron.get("FluencyScore", 0), 1),
                                        "completeness_score": round(pron.get("CompletenessScore", 0), 1),
                                        "audio_bytes": audio_bytes,
                                        "result": result
                                    }

                                    # Insertar al inicio
                                    st.session_state.pronunciation_history.insert(0, entry)

                                    # Limitar a 10 elementos
                                    if len(st.session_state.pronunciation_history) > 10:
                                        st.session_state.pronunciation_history.pop()
                                else:
                                    st.error(f"❌ Error: {result.get('error', 'Error desconocido')}")
                            except Exception as e:
                                st.error(f"❌ Error durante la evaluación: {str(e)}")
                    else:
                        st.error(f"❌ {validation['error']}")

    # ------------------ TAB 2: Subir archivo ------------------
    with tab2:
        st.subheader("Sube tu archivo de audio")
        uploaded_file = st.file_uploader("Elige un archivo .wav", type=["wav"])

        if uploaded_file is not None:
            audio_bytes = uploaded_file.read()
            validation = validate_audio_bytes(audio_bytes)

            if validation["valid"]:
                st.success("Archivo válido ✅")
                st.audio(audio_bytes, format="audio/wav")

                if st.button("Evaluar Pronunciación", use_container_width=True, key="upload_eval"):
                    with st.spinner("Analizando tu pronunciación..."):
                        try:
                            result = cached_evaluate(audio_bytes, selected_phrase, language_code)
                            if result["success"]:
                                st.session_state.last_assessment = {
                                    "phrase": selected_phrase,
                                    "language": language_code,
                                    "result": result,
                                    "audio_bytes": audio_bytes
                                }
                                st.success("¡Evaluación completada!")
                                st.snow()

                                if "pronunciation_history" not in st.session_state:
                                    st.session_state.pronunciation_history = []

                                json_result = result.get("json_result", {})
                                nbest = json_result.get("NBest", [{}])[0]
                                pron = nbest.get("PronunciationAssessment", {})

                                entry = {
                                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                                    "phrase": selected_phrase,
                                    "language": language_code,
                                    "pron_score": round(pron.get("PronScore", 0), 1),
                                    "accuracy_score": round(pron.get("AccuracyScore", 0), 1),
                                    "fluency_score": round(pron.get("FluencyScore", 0), 1),
                                    "completeness_score": round(pron.get("CompletenessScore", 0), 1),
                                    "audio_bytes": audio_bytes,
                                    "result": result
                                }

                                # Insertar al inicio
                                st.session_state.pronunciation_history.insert(0, entry)

                                # Limitar a 10 elementos
                                if len(st.session_state.pronunciation_history) > 10:
                                    st.session_state.pronunciation_history.pop()

                            else:
                                st.error(f"❌ Error: {result.get('error', 'Error desconocido')}")
                        except Exception as e:
                            st.error(f"❌ Error durante la evaluación: {str(e)}")
            else:
                st.error(f"❌ {validation['error']}")

    st.markdown("\n---")

    # Navegación
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Ver Resultados", use_container_width=True):
            st.switch_page("pages/2_resultados.py")
    with col2:
        if st.button("Volver al Inicio", use_container_width=True):
            st.switch_page("main.py")
    with col3:
        if st.button("Ver Historial", use_container_width=True):
            st.switch_page("pages/3_historial.py")



if __name__ == "__main__":
    main()
