from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException
from database import get_connection
from auth import require_admin
from utils import process_image

router = APIRouter(prefix="/servicios", tags=["Servicios"])


# ✅ GET TODOS (SIN SLASH FINAL)
@router.get("")
def get_servicios():
    conexion = get_connection()
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT * FROM servicios ORDER BY id DESC")
        return cursor.fetchall()
    finally:
        cursor.close()
        conexion.close()


# ✅ TOP 6 DESTACADOS
@router.get("/top")
def get_servicios_top():
    conexion = get_connection()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            SELECT * FROM servicios
            WHERE destacado = 1
            ORDER BY id DESC
            LIMIT 6
        """)
        return cursor.fetchall()
    finally:
        cursor.close()
        conexion.close()


# ✅ CREAR
@router.post("")
def create_servicio(
    title: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    destacado: bool = Form(False),
    file: UploadFile = File(None),
    user=Depends(require_admin)
):
    conexion = get_connection()
    cursor = conexion.cursor()

    try:
        # límite destacados
        if destacado:
            cursor.execute("SELECT COUNT(*) as total FROM servicios WHERE destacado=1")
            if cursor.fetchone()["total"] >= 6:
                raise HTTPException(400, "Máximo 6 destacados")

        image_url = process_image(file) if file else None

        cursor.execute("""
            INSERT INTO servicios (title, description, price, image_url, destacado)
            VALUES (%s,%s,%s,%s,%s)
        """, (title, description, price, image_url, destacado))

        conexion.commit()
        return {"mensaje": "Servicio creado"}

    finally:
        cursor.close()
        conexion.close()


# ✅ ACTUALIZAR
@router.put("/{id}")
def update_servicio(
    id: int,
    title: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    destacado: bool = Form(False),
    file: UploadFile = File(None),
    user=Depends(require_admin)
):
    conexion = get_connection()
    cursor = conexion.cursor()

    try:
        # validar destacados
        if destacado:
            cursor.execute("""
                SELECT COUNT(*) as total 
                FROM servicios 
                WHERE destacado=1 AND id != %s
            """, (id,))
            if cursor.fetchone()["total"] >= 6:
                raise HTTPException(400, "Máximo 6 destacados")

        if file:
            image_url = process_image(file)
            cursor.execute("""
                UPDATE servicios
                SET title=%s, description=%s, price=%s, image_url=%s, destacado=%s
                WHERE id=%s
            """, (title, description, price, image_url, destacado, id))
        else:
            cursor.execute("""
                UPDATE servicios
                SET title=%s, description=%s, price=%s, destacado=%s
                WHERE id=%s
            """, (title, description, price, destacado, id))

        conexion.commit()
        return {"mensaje": "Servicio actualizado"}

    finally:
        cursor.close()
        conexion.close()


# ✅ DELETE
@router.delete("/{id}")
def delete_servicio(id: int, user=Depends(require_admin)):
    conexion = get_connection()
    cursor = conexion.cursor()

    try:
        cursor.execute("DELETE FROM servicios WHERE id=%s", (id,))
        conexion.commit()
        return {"mensaje": "Servicio eliminado"}
    finally:
        cursor.close()
        conexion.close()