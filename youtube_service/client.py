from datetime import datetime, timedelta, timezone
from typing import Any

import requests

from config import YOUTUBE_API_KEY, YOUTUBE_HANDLE


YOUTUBE_CHANNELS_URL = (
    "https://www.googleapis.com/youtube/v3/channels"
)
YOUTUBE_PLAYLIST_ITEMS_URL = (
    "https://www.googleapis.com/youtube/v3/playlistItems"
)
YOUTUBE_VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"


class YouTubeAPIError(Exception):
    """Error producido al consultar YouTube."""


def _consultar_youtube(url: str, parametros: dict[str, Any]) -> dict[str, Any]:
    try:
        respuesta = requests.get(url, params=parametros, timeout=20)
        respuesta.raise_for_status()
        return respuesta.json()
    except requests.Timeout as error:
        raise YouTubeAPIError("YouTube tardó demasiado en responder.") from error
    except (requests.RequestException, ValueError) as error:
        raise YouTubeAPIError(
            "No se pudo consultar YouTube. Revisá la conexión y la clave API."
        ) from error


def _fecha_youtube(valor: str) -> datetime:
    return datetime.fromisoformat(valor.replace("Z", "+00:00"))


def obtener_rendimiento_videos(
    playlist_subidas: str,
    fecha: datetime | None = None,
) -> dict[str, Any]:
    """Obtiene el último video y el más visto de los últimos 30 días."""
    lista = _consultar_youtube(
        YOUTUBE_PLAYLIST_ITEMS_URL,
        {
            "part": "contentDetails",
            "playlistId": playlist_subidas,
            "maxResults": 50,
            "key": YOUTUBE_API_KEY,
        },
    )
    ids = [
        item.get("contentDetails", {}).get("videoId")
        for item in lista.get("items", [])
    ]
    ids = [video_id for video_id in ids if video_id]
    if not ids:
        return {"ultimo": None, "mas_visto_30_dias": None, "publicados_30_dias": 0}

    detalle = _consultar_youtube(
        YOUTUBE_VIDEOS_URL,
        {
            "part": "snippet,statistics",
            "id": ",".join(ids),
            "maxResults": 50,
            "key": YOUTUBE_API_KEY,
        },
    )
    por_id = {item["id"]: item for item in detalle.get("items", [])}
    videos = []
    for video_id in ids:
        item = por_id.get(video_id)
        if item is None:
            continue
        snippet = item.get("snippet", {})
        estadisticas = item.get("statistics", {})
        videos.append({
            "id": video_id,
            "titulo": snippet.get("title", "Sin título"),
            "publicado_en": snippet.get("publishedAt"),
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "vistas": int(estadisticas.get("viewCount", 0)),
            "likes": (
                int(estadisticas["likeCount"])
                if "likeCount" in estadisticas else None
            ),
            "comentarios": (
                int(estadisticas["commentCount"])
                if "commentCount" in estadisticas else None
            ),
        })

    ahora = fecha or datetime.now(timezone.utc)
    limite = ahora - timedelta(days=30)
    recientes = [
        video for video in videos
        if video["publicado_en"]
        and _fecha_youtube(video["publicado_en"]) >= limite
    ]
    return {
        "ultimo": videos[0] if videos else None,
        "mas_visto_30_dias": (
            max(recientes, key=lambda video: video["vistas"])
            if recientes else None
        ),
        "publicados_30_dias": len(recientes),
    }


def obtener_estadisticas_canal() -> dict[str, Any]:
    """Obtiene las estadísticas públicas del canal configurado."""

    parametros = {
        "part": "snippet,statistics,contentDetails",
        "forHandle": YOUTUBE_HANDLE,
        "key": YOUTUBE_API_KEY,
    }

    datos = _consultar_youtube(YOUTUBE_CHANNELS_URL, parametros)
    canales = datos.get("items", [])

    if not canales:
        raise YouTubeAPIError(
            f"No se encontró el canal {YOUTUBE_HANDLE}."
        )

    canal = canales[0]
    informacion = canal["snippet"]
    estadisticas = canal["statistics"]
    playlist_subidas = canal["contentDetails"]["relatedPlaylists"]["uploads"]
    try:
        rendimiento_videos = obtener_rendimiento_videos(playlist_subidas)
    except YouTubeAPIError:
        rendimiento_videos = {
            "ultimo": None,
            "mas_visto_30_dias": None,
            "publicados_30_dias": 0,
        }

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
        "rendimiento_videos": rendimiento_videos,
    }
