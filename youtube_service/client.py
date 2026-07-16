from typing import Any

import requests

from config import YOUTUBE_API_KEY, YOUTUBE_HANDLE


YOUTUBE_CHANNELS_URL = (
    "https://www.googleapis.com/youtube/v3/channels"
)


class YouTubeAPIError(Exception):
    """Error producido al consultar YouTube."""


def obtener_estadisticas_canal() -> dict[str, Any]:
    """Obtiene las estadísticas públicas del canal configurado."""

    parametros = {
        "part": "snippet,statistics",
        "forHandle": YOUTUBE_HANDLE,
        "key": YOUTUBE_API_KEY,
    }

    try:
        respuesta = requests.get(
            YOUTUBE_CHANNELS_URL,
            params=parametros,
            timeout=20,
        )

        respuesta.raise_for_status()

    except requests.Timeout as error:
        raise YouTubeAPIError(
            "YouTube tardó demasiado en responder."
        ) from error

    except requests.RequestException as error:
        raise YouTubeAPIError(
            f"No se pudo consultar YouTube: {error}"
        ) from error

    datos = respuesta.json()
    canales = datos.get("items", [])

    if not canales:
        raise YouTubeAPIError(
            f"No se encontró el canal {YOUTUBE_HANDLE}."
        )

    canal = canales[0]
    informacion = canal["snippet"]
    estadisticas = canal["statistics"]

    return {
        "id_canal": canal["id"],
        "nombre": informacion["title"],
        "suscriptores": int(
            estadisticas.get("subscriberCount", 0)
        ),
        "visualizaciones": int(
            estadisticas.get("viewCount", 0)
        ),
        "videos": int(
            estadisticas.get("videoCount", 0)
        ),
    }