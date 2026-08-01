import asyncio

from analytics.signals import calcular_senales
from config import validar_configuracion
from storage.repository import cargar_datos, guardar_datos
from storage.history import (
    calcular_comparaciones,
    cargar_historial,
    registrar_medicion,
)
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
    validar_configuracion()

    datos_anteriores = cargar_datos()
    historial = cargar_historial()

    # Migra automáticamente la última medición de la versión anterior.
    if not historial and any(
        int(datos_anteriores.get(metrica, 0))
        for metrica in ("suscriptores", "visualizaciones", "videos")
    ):
        historial = registrar_medicion(historial, datos_anteriores)

    estadisticas = obtener_estadisticas_canal()

    print("Message ID guardado:", datos_anteriores.get("message_id"))

    comparaciones = calcular_comparaciones(historial, estadisticas)
    senales = calcular_senales(estadisticas, comparaciones)
    mensaje = crear_mensaje(estadisticas, comparaciones, senales)

    print("\nMensaje generado:")
    print(mensaje)
    print()

    message_id = await publicar_o_actualizar_mensaje(
        texto=mensaje,
        message_id=datos_anteriores.get("message_id"),
    )

    print("Message ID utilizado:", message_id)

    nuevos_datos = {
        "suscriptores": estadisticas["suscriptores"],
        "visualizaciones": estadisticas["visualizaciones"],
        "videos": estadisticas["videos"],
        "message_id": message_id,
    }

    guardar_datos(nuevos_datos)
    registrar_medicion(historial, estadisticas)

    print("✅ RojoStats terminó la ejecución.")


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
