from fastapi import APIRouter
from database import get_connection
import bcrypt

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("")
def get_users():
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("SELECT id,email,rol,creado_en FROM usuarios ORDER BY id DESC")
    data = cursor.fetchall()

    cursor.close()
    conexion.close()

    return data


@router.delete("/{id}")
def delete_user(id: int):
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM usuarios WHERE id=%s", (id,))
    conexion.commit()

    cursor.close()
    conexion.close()

    return {"mensaje": "Usuario eliminado"}

@router.post("")
def create_user(user: dict):
    conexion = get_connection()
    cursor = conexion.cursor()

    # 🔐 HASH DE CONTRASEÑA
    hashed_password = bcrypt.hashpw(
        user["password"].encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    cursor.execute("""
        INSERT INTO usuarios (email, password, rol)
        VALUES (%s, %s, %s)
    """, (
        user["email"],
        hashed_password,
        user["rol"]
    ))

    conexion.commit()

    cursor.close()
    conexion.close()

    return {"mensaje": "Usuario creado"}