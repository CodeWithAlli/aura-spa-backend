from fastapi import APIRouter
from database import get_connection
from passlib.context import CryptContext
from fastapi.responses import JSONResponse

router = APIRouter(tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login")
def login(data: dict):
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE email=%s", (data["email"],))
    user = cursor.fetchone()

    cursor.close()
    conexion.close()

    if not user or not pwd_context.verify(data["password"], user["password"]):
        return JSONResponse(status_code=401, content={"detail": "Credenciales inválidas"})

    return {
        "token": data["email"],
        "user": {
            "email": user["email"],
            "rol": user["rol"]
        }
    }