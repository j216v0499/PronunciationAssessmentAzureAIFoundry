import json
import os

import azure.cognitiveservices.speech as speechsdk
import streamlit as st

from dotenv import load_dotenv
from app.utils.languages_phrases import LANGUAGE_OPTIONS

# Cargar variables de entorno desde .env y .st
load_dotenv()

"""
  Clase para evaluar la pronunciación usando Azure Cognitive Services (Speech SDK)
"""
class PronunciationEvaluator:

    def __init__(self):
        self.speech_key = st.secrets.get("AZURE_SPEECH_KEY", os.getenv("AZURE_SPEECH_KEY", ""))
        self.service_region = st.secrets.get("AZURE_SPEECH_REGION", os.getenv("AZURE_SPEECH_REGION", ""))
        self.is_configured = self.validate_credentials()

    def validate_credentials(self):
        """Valida que las credenciales estén configuradas"""
        if not self.speech_key or not self.service_region:
            return False
        if "tu_clave_aqui" in self.speech_key or "tu_region_aqui" in self.service_region:
            return False
        return True

    def get_configuration_status(self):
        """Devuelve el estado de configuración"""
        if not self.is_configured:
            return {
                "status": "error",
                "message": "⚠️ Credenciales de Azure no configuradas. Por favor, actualiza secrets.toml y .env con tus credenciales reales."
            }
        return {
            "status": "success",
            "message": "✅ Credenciales de Azure configuradas correctamente"
        }
    #                                                                 Valor por default
    def evaluate_pronunciation(self, audio_file_path, reference_text, language="en-US"):
        """
        Evalúa la pronunciación usando Azure Pronunciation Assessment
        """

        # Verificar que las credenciales están configuradas
        if not self.is_configured:
            return {
                "success": False,
                "error": "❌ Credenciales de Azure no configuradas.v",
                "sdk_result": None,
                "json_result": None
            }

        # Validar idioma
        if language not in LANGUAGE_OPTIONS.values():
            return {
                "success": False,
                "error": f"Idioma no soportado: {language}.",
                "sdk_result": None,
                "json_result": None
            }

        try:
            # Configuración de audio
            audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)

            # Configuración de speech
            speech_config = speechsdk.SpeechConfig(
                subscription=self.speech_key,
                region=self.service_region
            )
            speech_config.speech_recognition_language = language

            # Configuración de evaluación de pronunciación
            pronunciation_config = speechsdk.PronunciationAssessmentConfig(
                reference_text=reference_text,
                grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark,
                granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme,
                enable_miscue=True
            )

            # Crear reconocedor
            speech_recognizer = speechsdk.SpeechRecognizer(
                speech_config=speech_config,
                audio_config=audio_config
            )

            # Aplicar configuración de pronunciación
            pronunciation_config.apply_to(speech_recognizer)

            # Realizar reconocimiento
            result = speech_recognizer.recognize_once()

            # Verificar resultado
            if result.reason != speechsdk.ResultReason.RecognizedSpeech:
                error_msg = "No se pudo reconocer el habla. "
                if result.reason == speechsdk.ResultReason.NoMatch:
                    error_msg += "El audio no tiene sentido."
                elif result.reason == speechsdk.ResultReason.Canceled:
                    cancellation_details = result.cancellation_details
                    error_msg += f"Cancelado: {cancellation_details.reason}"
                    if cancellation_details.reason == speechsdk.CancellationReason.Error:
                        error_msg += f" - Error: {cancellation_details.error_details}"
                return {"success": False, "error": error_msg}

            # Resultados como JSON
            json_result = result.properties.get(speechsdk.PropertyId.SpeechServiceResponse_JsonResult)

            if json_result:
                json_data = json.loads(json_result)
                return {
                    "success": True,
                    "error": None,
                    "sdk_result": result,
                    "json_result": json_data

                }
            else:
                return {
                    "success": False,
                    "error": "No se obtuvieron resultados JSON",
                    "sdk_result": result,
                    "json_result": None
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"Error durante la evaluación: {str(e)}",
                "sdk_result": None,
                "json_result": None

            }

    def evaluate_pronunciation_bytes(self, audio_bytes: bytes, reference_text, language="en-US"):
        """
        Evalúa la pronunciación usando bytes de audio en lugar de archivo.
        """
        import tempfile

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_path = tmp_file.name

        try:
            return self.evaluate_pronunciation(tmp_path, reference_text, language)
        finally:
            os.unlink(tmp_path)

