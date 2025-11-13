

# Imagen base oficial de Python
FROM python:3.11-slim

# Establece directorio de trabajo
WORKDIR /app

# Instala librerías de sistema necesarias para audio y ffmpeg
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libasound2-dev \
        portaudio19-dev \
        libpulse-dev \
        ffmpeg \
        build-essential \
        && rm -rf /var/lib/apt/lists/*

# Copia requirements y actualiza azure-cognitiveservices-speech
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade azure-cognitiveservices-speech

# Copia todo el proyecto
COPY . .

# Exponer puerto de Streamlit
EXPOSE 8501

# Variables de entorno de Streamlit
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ENABLECORS=false

# Comando para ejecutar la app
CMD ["streamlit", "run", "main.py"]
