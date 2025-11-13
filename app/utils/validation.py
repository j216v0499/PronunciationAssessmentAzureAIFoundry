import os
import tempfile
import wave
import contextlib

"""
Valida que el archivo de audio sea válido y devuelve errores específicos.

Return un dict:
{
    "valid": bool,
    "error": str | None
}
"""

def validate_audio_file(file_path):

    if not os.path.exists(file_path):
        return {"valid": False, "error": "Archivo no encontrado"}

    if not file_path.lower().endswith('.wav'):
        return {"valid": False, "error": "El archivo no es .wav"}

    file_size = os.path.getsize(file_path)
    if file_size == 0:
        return {"valid": False, "error": "Archivo vacío"}

    if file_size > 100 * 1024 * 1024:
        return {"valid": False, "error": "Archivo demasiado grande (>100 MB)"}

    try:
        with contextlib.closing(wave.open(file_path, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate) if rate > 0 else 0

            if duration <= 0.5:
                return {"valid": False, "error": f"Duración demasiado corta ({duration:.2f}s), debe ser >0.5s"}

    except wave.Error as e:
        return {"valid": False, "error": f"Error leyendo WAV: {str(e)}"}

    return {"valid": True, "error": None}


def validate_audio_bytes(audio_bytes: bytes) -> dict:
    """
    Valida un audio en bytes usando la función `validate_audio_file`.

    Retorna un dict con:
    {
        "valid": True/False,
        "error": "mensaje de error si no es válido"
    }
    """
    tmp_file_path = None
    try:
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_file_path = tmp_file.name

        # Validar usando tu función existente
        result = validate_audio_file(tmp_file_path)
        return result

    except Exception as e:
        return {"valid": False, "error": f"Error al validar audio: {str(e)}"}

    finally:
        # Eliminar temporal
        if tmp_file_path and os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
