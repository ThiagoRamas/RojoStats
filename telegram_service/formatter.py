from datetime import datetime
from typing import Any

from utils.numbers import formatear_numero, formatear_variacion


def crear_mensaje(
    estadisticas: dict[str, Any],
    datos_anteriores: dict[str, Any],
) -> str:
    """Construye el mensaje que se mostrará en Telegram."""

    suscriptores_anteriores = int(
        datos_anteriores.get("suscriptores", 0)
    )

    visualizaciones_anteriores = int(
        datos_anteriores.get("visualizaciones", 0)
    )

    videos_anteriores = int(
        datos_anteriores.get("videos", 0)
    )

    primera_medicion = (
        suscriptores_anteriores == 0
        and visualizaciones_anteriores == 0
        and videos_anteriores == 0
    )

    variacion_suscriptores = (
        estadisticas["suscriptores"]
        - suscriptores_anteriores
    )

    variacion_visualizaciones = (
        estadisticas["visualizaciones"]
        - visualizaciones_anteriores
    )

    variacion_videos = (
        estadisticas["videos"]
        - videos_anteriores
    )

    fecha_actualizacion = datetime.now().strftime(
        "%d/%m/%Y - %H:%M"
    )

    if primera_medicion:
        texto_variacion_suscriptores = "Sin mediciones anteriores"
        texto_variacion_visualizaciones = "Sin mediciones anteriores"
        texto_variacion_videos = "Sin mediciones anteriores"
    else:
        texto_variacion_suscriptores = formatear_variacion(
            variacion_suscriptores
        )

        texto_variacion_visualizaciones = formatear_variacion(
            variacion_visualizaciones
        )

        texto_variacion_videos = formatear_variacion(
            variacion_videos
        )

    return (
        "🔴 <b>ROJOSTATS</b>\n"
        "<i>Estadísticas digitales de Independiente</i>\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "📺 <b>YouTube</b>\n"
        f"{estadisticas['nombre']}\n\n"
        "👥 <b>Suscriptores</b>\n"
        f"{formatear_numero(estadisticas['suscriptores'])}\n"
        f"Variación: {texto_variacion_suscriptores}\n\n"
        "👁️ <b>Visualizaciones totales</b>\n"
        f"{formatear_numero(estadisticas['visualizaciones'])}\n"
        f"Variación: {texto_variacion_visualizaciones}\n\n"
        "🎬 <b>Videos publicados</b>\n"
        f"{formatear_numero(estadisticas['videos'])}\n"
        f"Variación: {texto_variacion_videos}\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "🕒 <b>Última actualización</b>\n"
        f"{fecha_actualizacion}\n\n"
        "Proyecto independiente y no oficial.\n"
        "Datos públicos obtenidos mediante YouTube Data API."
    )