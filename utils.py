import os
import random
import shutil
from PIL import Image
from fastapi import UploadFile, HTTPException

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def process_image(file: UploadFile):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Solo imágenes permitidas")

    filename = f"{random.randint(10000,99999)}.jpg"
    path = os.path.join(UPLOAD_DIR, filename)
    temp = path + "_tmp"

    with open(temp, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    img = Image.open(temp)
    img = img.convert("RGB")
    img.thumbnail((800, 800))
    img.save(path, optimize=True, quality=70)

    os.remove(temp)

    return f"http://localhost:8000/uploads/{filename}"