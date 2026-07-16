import asyncio

from config import validar_configuracion
from storage.repository import cargar_datos, guardar_datos
from telegram_service.client import (
    TelegramServiceError,
    publicar_o_actualizar_mensaje,
)
from telegram_service.formatter import crear_mensaje
from youtube_service.client import (
    YouTubeAPIError,
    obtener_estadisticas_canal,
)


async def ejecutar_actualizacion() -> None:
    """Consulta YouTube y actualiza el mensaje de Telegram."""

    validar_configuracion()

    datos_anteriores = cargar_datos()
    estadisticas = obtener_estadisticas_canal()

    mensaje = crear_mensaje(
        estadisticas=estadisticas,
        datos_anteriores=datos_anteriores,
    )

    message_id = await publicar_o_actualizar_mensaje(
        texto=mensaje,
        message_id=datos_anteriores.get("message_id"),
    )

    nuevos_datos = {
        "suscriptores": estadisticas["suscriptores"],
        "visualizaciones": estadisticas["visualizaciones"],
        "videos": estadisticas["videos"],
        "message_id": message_id,
    }

    guardar_datos(nuevos_datos)

    print("✅ RojoStats se actualizó correctamente.")
    print(f"Canal: {estadisticas['nombre']}")
    print(f"Suscriptores: {estadisticas['suscriptores']}")
    print(f"Visualizaciones: {estadisticas['visualizaciones']}")
    print(f"Videos: {estadisticas['videos']}")


def main() -> None:
    try:
        asyncio.run(ejecutar_actualizacion())

    except ValueError as error:
        print(f"❌ Error de configuración: {error}")

    except YouTubeAPIError as error:
        print(f"❌ Error de YouTube: {error}")

    except TelegramServiceError as error:
        print(f"❌ Error de Telegram: {error}")

    except Exception as error:
        print(f"❌ Error inesperado: {error}")


if __name__ == "__main__":
    main()