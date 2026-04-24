import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routers import servicios, reservas, users, login

app = FastAPI()

# 🔥 ASEGURAR CARPETA uploads (CRÍTICO EN PRODUCCIÓN)
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# 🔥 CORS (para que frontend pueda conectarse)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # luego puedes restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 RUTA BASE (evita paranoia al abrir el link)
@app.get("/")
def root():
    return {"status": "ok"}

# 🔥 STATIC FILES
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# 🔥 ROUTERS
app.include_router(servicios.router)
app.include_router(reservas.router)
app.include_router(users.router)
app.include_router(login.router)