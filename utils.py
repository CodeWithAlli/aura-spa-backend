import os
import random
from PIL import Image
from fastapi import UploadFile, HTTPException
from dotenv import load_dotenv
import httpx
import io

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
BUCKET = "imagenes"

def process_image(file: UploadFile):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Solo imágenes permitidas")

    # Leer y redimensionar imagen
    contents = file.file.read()
    img = Image.open(io.BytesIO(contents))
    img = img.convert("RGB")
    img.thumbnail((800, 800))

    # Guardar en buffer
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", optimize=True, quality=70)
    buffer.seek(0)

    # Nombre único
    filename = f"{random.randint(10000,99999)}.jpg"

    # Subir a Supabase Storage
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "image/jpeg",
    }

    response = httpx.put(
        f"{SUPABASE_URL}/storage/v1/object/{BUCKET}/{filename}",
        content=buffer.read(),
        headers=headers,
    )

    if response.status_code not in (200, 201):
        raise HTTPException(status_code=500, detail="Error subiendo imagen")

    return f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET}/{filename}"