from fastapi import Header, HTTPException
from database import get_connection

def get_user_by_token(token: str):
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE email=%s", (token,))
    user = cursor.fetchone()

    cursor.close()
    conexion.close()
    return user


def require_admin(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="No autorizado")

    token = authorization.replace("Bearer ", "")
    user = get_user_by_token(token)

    if not user or user["rol"] != "admin":
        raise HTTPException(status_code=403, detail="Solo admin")

    return user