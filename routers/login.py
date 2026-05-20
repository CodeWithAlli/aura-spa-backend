from fastapi import APIRouter
from database import get_connection
from passlib.context import CryptContext
from fastapi.responses import JSONResponse

router = APIRouter(tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain: str, stored: str) -> bool:
    """Verifica contraseña: soporta bcrypt y texto plano (para dev local)."""
    # Si el hash luce como bcrypt, usar passlib
    if stored.startswith("$2b$") or stored.startswith("$2a$"):
        try:
            return pwd_context.verify(plain, stored)
        except Exception:
            return False
    # Contraseña en texto plano (usuarios insertados manualmente en dev)
    return plain == stored


@router.post("/login")
def login(data: dict):
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE email=%s", (data["email"],))
    user = cursor.fetchone()

    cursor.close()
    conexion.close()

    if not user or not verify_password(data["password"], user["password"]):
        return JSONResponse(status_code=401, content={"detail": "Credenciales inválidas"})

    return {
        "token": data["email"],
        "user": {
            "email": user["email"],
            "rol": user["rol"]
        }
    }
