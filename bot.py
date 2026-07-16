import asyncio
import json
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from telegram import Bot
from telegram.error import BadRequest, TelegramError

from youtube_api import obtener_estadisticas_canal


load_dotenv()

TOKEN = os.getenv("TOKEN")
CANAL = os.getenv("CANAL")

ARCHIVO_DATOS = Path("datos.json")


def cargar_datos() -> dict:
    datos_iniciales = {
        "suscriptores": 0,
        "visualizaciones": 0,
        "videos": 0,
        "message_id": None,
    }

    if not ARCHIVO_DATOS.exists():
        guardar_datos(datos_iniciales)
        return datos_iniciales

    try:
        with ARCHIVO_DATOS.open("r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except json.JSONDecodeError:
        guardar_datos(datos_iniciales)
        return datos_iniciales


def guardar_datos(datos: dict) -> None:
    with ARCHIVO_DATOS.open("w", encoding="utf-8") as archivo:
        json.dump(
            datos,
            archivo,
            ensure_ascii=False,
            indent=4,
        )


def formatear_numero(numero: int) -> str:
    return f"{numero:,}".replace(",", ".")


def formatear_variacion(numero: int) -> str:
    if numero > 0:
        return f"+{formatear_numero(numero)}"

    return formatear_numero(numero)


def crear_mensaje(
    estadisticas: dict,
    datos_anteriores: dict,
) -> str:
    variacion_suscriptores = (
        estadisticas["suscriptores"]
        - int(datos_anteriores["suscriptores"])
    )

    variacion_visualizaciones = (
        estadisticas["visualizaciones"]
        - int(datos_anteriores["visualizaciones"])
    )

    fecha = datetime.now().strftime("%d/%m/%Y - %H:%M")

    return (
        "🔴 <b>INDEPENDIENTE EN YOUTUBE</b>\n\n"
        f"📺 <b>Canal</b>\n"
        f"{estadisticas['nombre']}\n\n"
        f"👥 <b>Suscriptores</b>\n"
        f"{formatear_numero(estadisticas['suscriptores'])}\n"
        f"Variación registrada: "
        f"{formatear_variacion(variacion_suscriptores)}\n\n"
        f"👁️ <b>Visualizaciones totales</b>\n"
        f"{formatear_numero(estadisticas['visualizaciones'])}\n"
        f"Nuevas visualizaciones: "
        f"{formatear_variacion(variacion_visualizaciones)}\n\n"
        f"🎬 <b>Videos publicados</b>\n"
        f"{formatear_numero(estadisticas['videos'])}\n\n"
        f"🕒 <b>Última actualización</b>\n"
        f"{fecha}\n\n"
        "Seguimiento no oficial basado en datos públicos de YouTube."
    )


async def actualizar_telegram() -> None:
    if not TOKEN:
        raise ValueError("No se encontró TOKEN en el archivo .env.")

    if not CANAL:
        raise ValueError("No se encontró CANAL en el archivo .env.")

    datos_anteriores = cargar_datos()
    estadisticas = obtener_estadisticas_canal()

    mensaje = crear_mensaje(
        estadisticas,
        datos_anteriores,
    )

    bot = Bot(token=TOKEN)
    message_id = datos_anteriores.get("message_id")

    try:
        if message_id is None:
            resultado = await bot.send_message(
                chat_id=CANAL,
                text=mensaje,
                parse_mode="HTML",
            )

            message_id = resultado.message_id
            print("Mensaje de YouTube publicado correctamente.")

        else:
            try:
                await bot.edit_message_text(
                    chat_id=CANAL,
                    message_id=message_id,
                    text=mensaje,
                    parse_mode="HTML",
                )

                print("Estadísticas actualizadas correctamente.")

            except BadRequest as error:
                if "Message is not modified" in str(error):
                    print("Los datos todavía no cambiaron.")
                else:
                    raise

        nuevos_datos = {
            "suscriptores": estadisticas["suscriptores"],
            "visualizaciones": estadisticas["visualizaciones"],
            "videos": estadisticas["videos"],
            "message_id": message_id,
        }

        guardar_datos(nuevos_datos)

    except TelegramError as error:
        print(f"Error de Telegram: {error}")
        raise


if __name__ == "__main__":
    asyncio.run(actualizar_telegram())