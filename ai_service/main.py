import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from openai import OpenAI
from dotenv import load_dotenv
from google.cloud import vision # <-- Nueva importación para OCR
import re

# Cargar variables de entorno (tu API Key de OpenAI)
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configuramos la ruta de la llave de Google para el OCR
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_key.json"

app = FastAPI()

@app.post("/api/transcribir/")
async def transcribir_audio(audio: UploadFile = File(...)):
    try:
        # Guardamos el archivo temporalmente (Whisper necesita leer un archivo físico)
        temp_file_path = f"temp_{audio.filename}"
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)

        # Enviamos a OpenAI Whisper
        with open(temp_file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file,
                response_format="text",
                language="es"
            )

        # Borramos el archivo temporal para no llenar el servidor
        os.remove(temp_file_path)

        # Devolvemos el texto a Django
        return {"texto": transcript}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/api/estructurar-checklist/")
async def estructurar_checklist(datos: dict):
    texto_libre = datos.get("texto", "")
    
    prompt_sistema = """
    Eres un asistente experto en talleres de motos. 
    Tu tarea es recibir una transcripción de un mecánico y convertirla en una lista JSON de tareas.
    
    REGLAS ESTRICTAS:
    1. Debes devolver UN OBJETO JSON que contenga UNA ÚNICA CLAVE llamada "tareas".
    2. El valor de "tareas" debe ser una lista (arreglo) de objetos. Cada objeto debe tener: "descripcion" y "completada" (siempre false).
    3. REGLA CRÍTICA: Si el texto recibido es muy corto (ej. "Arreglar mordaza", "llanta pinchada", "aceite"), DEBES interpretarlo obligatoriamente como una tarea válida. NUNCA devuelvas una lista vacía si recibes algún texto comprensible.
    4. Mejora ligeramente la redacción si es necesario (ej. "arreglar mordaza" -> "Arreglar mordaza del freno"), pero mantén la intención.
    
    Ejemplo de salida esperado: 
    {
      "tareas": [
        {"descripcion": "Arreglar mordaza del freno", "completada": false}
      ]
    }
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": f"Convierte esto en checklist: {texto_libre}"}
            ],
            response_format={ "type": "json_object" } # Forzamos respuesta JSON
        )
        
        import json
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- NUEVO ENDPOINT PARA LEER PLACAS (BLOQUE 5.2) ---
@app.post("/api/leer-placa/")
async def leer_placa(file: UploadFile = File(...)):
    """
    Recibe una imagen, la guarda temporalmente, consulta a Google Vision y devuelve el texto.
    """
    temp_file_path = f"temp_vision_{file.filename}"
    try:
        # 1. Guardamos el archivo temporalmente en el disco (El truco de Whisper)
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 2. Lo leemos en modo binario físico para Google Vision
        with open(temp_file_path, "rb") as image_file:
            content = image_file.read()
        
        # 3. Conectamos con el cliente de Google Vision
        vision_client = vision.ImageAnnotatorClient()
        image = vision.Image(content=content)
        
        # Solicitamos la detección de texto
        response = vision_client.text_detection(image=image)
        texts = response.text_annotations

        # 4. Borramos la imagen temporal para no llenar el servidor
        os.remove(temp_file_path)

        if response.error.message:
            raise HTTPException(status_code=500, detail=response.error.message)

        if texts:
            # texts[0].description trae todo el texto detectado en la foto
            texto_crudo = texts[0].description.upper()
            
            # 1. Limpieza de "ruido" visual (palabras comunes en las placas de Ecuador)
            palabras_a_ignorar = ["ANT", "ECUADOR", "NACIONAL", "TRANSITO"]
            for palabra in palabras_a_ignorar:
                texto_crudo = texto_crudo.replace(palabra, "")
                
            # 2. Quitamos espacios y saltos de línea restantes
            texto_limpio = "".join(texto_crudo.split())
            
            # 3. Búsqueda inteligente (Regex): 
            # Busca de 2 a 3 letras, seguidas de 3 a 4 números, y opcionalmente 1 letra al final (Ej: JW467F o ABC1234)
            patron_placa = r'[A-Z]{2,3}\d{3,4}[A-Z]?'
            coincidencia = re.search(patron_placa, texto_limpio)
            
            if coincidencia:
                placa_final = coincidencia.group(0)
            else:
                # Si la IA lee algo muy raro, devolvemos lo que quedó limpio como plan de contingencia
                placa_final = texto_limpio 
            
            return {"placa_detectada": placa_final}

    except Exception as e:
        # Si ocurre un error, nos aseguramos de borrar el archivo basura
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=str(e))