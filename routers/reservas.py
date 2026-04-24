from fastapi import APIRouter
from database import get_connection
import random

router = APIRouter(prefix="/reservas", tags=["Reservas"])

CAPACIDAD_POR_HORA = 3


@router.get("")
def obtener_reservas(estado: str = "todos"):
    conexion = get_connection()
    cursor = conexion.cursor()

    if estado == "todos":
        cursor.execute("SELECT * FROM reservas ORDER BY creado_en DESC")
    else:
        cursor.execute(
            "SELECT * FROM reservas WHERE estado=%s ORDER BY creado_en DESC",
            (estado,)
        )

    data = cursor.fetchall()

    cursor.close()
    conexion.close()

    return data


@router.post("")
def crear_reserva(reserva: dict):
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT COUNT(*) as total
        FROM reservas
        WHERE fecha=%s AND hora=%s AND estado!='cancelado'
    """, (reserva["fecha"], reserva["hora"]))

    if cursor.fetchone()["total"] >= CAPACIDAD_POR_HORA:
        return {"error": "Horario lleno"}

    codigo = f"SPA-{random.randint(1000,9999)}"

    cursor.execute("""
        INSERT INTO reservas
        (codigo,nombre,email,telefono,servicio,especialista,fecha,hora,mensaje)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        codigo,
        reserva["nombre"],
        reserva["email"],
        reserva["telefono"],
        reserva["servicio"],
        reserva["especialista"],
        reserva["fecha"],
        reserva["hora"],
        reserva.get("mensaje")
    ))

    conexion.commit()
    cursor.close()
    conexion.close()

    return {"mensaje": "Reserva creada", "codigo": codigo}

@router.patch("/{id}")
def cambiar_estado(id: int, data: dict):
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute(
        "UPDATE reservas SET estado=%s WHERE id=%s",
        (data["estado"], id)
    )

    conexion.commit()

    if cursor.rowcount == 0:
        return {"error": "Reserva no encontrada"}

    cursor.close()
    conexion.close()

    return {"mensaje": "Estado actualizado"}

@router.put("/{id}")
def actualizar_reserva(id: int, reserva: dict):
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE reservas
        SET nombre=%s, servicio=%s, fecha=%s, hora=%s
        WHERE id=%s
    """, (
        reserva["nombre"],
        reserva["servicio"],
        reserva["fecha"],
        reserva["hora"],
        id
    ))

    conexion.commit()

    if cursor.rowcount == 0:
        return {"error": "Reserva no encontrada"}

    cursor.close()
    conexion.close()

    return {"mensaje": "Reserva actualizada"}

@router.delete("/{id}")
def eliminar_reserva(id: int):
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM reservas WHERE id=%s", (id,))
    conexion.commit()

    if cursor.rowcount == 0:
        return {"error": "Reserva no encontrada"}

    cursor.close()
    conexion.close()

    return {"mensaje": "Reserva eliminada"}