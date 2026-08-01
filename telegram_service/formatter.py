from datetime import datetime
from html import escape
from typing import Any

from utils.numbers import formatear_numero, formatear_variacion


def _formatear_decimal(valor: float) -> str:
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _variacion_con_porcentaje(
    metrica: str,
    comparacion: dict[str, Any],
) -> str:
    variacion = formatear_variacion(int(comparacion[metrica]))
    porcentaje = comparacion["porcentajes"][metrica]
    if porcentaje is None:
        return variacion
    signo = "+" if porcentaje > 0 else ""
    return f"{variacion} ({signo}{_formatear_decimal(porcentaje)} %)"


def _lineas_variacion(
    metrica: str,
    comparaciones: dict[str, dict[str, Any] | None],
) -> str:
    etiquetas = (
        ("hoy", "Hoy"),
        ("7_dias", "Últimos 7 días"),
        ("30_dias", "Últimos 30 días"),
    )
    lineas = []
    for periodo, etiqueta in etiquetas:
        comparacion = comparaciones.get(periodo)
        valor = (
            _variacion_con_porcentaje(metrica, comparacion)
            if comparacion is not None
            else "Sin historial suficiente"
        )
        lineas.append(f"{etiqueta}: {valor}")
    return "\n".join(lineas)


def _promedio_periodo(
    comparaciones: dict[str, dict[str, Any] | None],
    periodo: str,
) -> str:
    comparacion = comparaciones.get(periodo)
    if comparacion is None:
        return "Sin historial suficiente"
    suscriptores = comparacion["promedios_diarios"]["suscriptores"]
    visualizaciones = comparacion["promedios_diarios"]["visualizaciones"]
    return (
        f"{formatear_variacion(round(suscriptores))} suscriptores/día · "
        f"{formatear_variacion(round(visualizaciones))} vistas/día"
    )


def _metrica_opcional(valor: int | None) -> str:
    return formatear_numero(valor) if valor is not None else "No disponible"


def _rendimiento_videos(estadisticas: dict[str, Any]) -> str:
    rendimiento = estadisticas.get("rendimiento_videos", {})
    ultimo = rendimiento.get("ultimo")
    destacado = rendimiento.get("mas_visto_30_dias")
    if ultimo is None:
        return "🎥 <b>Rendimiento reciente</b>\nSin videos disponibles.\n\n"

    fecha = datetime.fromisoformat(
        ultimo["publicado_en"].replace("Z", "+00:00")
    ).strftime("%d/%m/%Y")
    bloque = (
        "🎥 <b>Rendimiento reciente</b>\n"
        "<b>Último video</b>\n"
        f'<a href="{ultimo["url"]}">{escape(ultimo["titulo"])}</a>\n'
        f"Publicado: {fecha}\n"
        f"Vistas: {formatear_numero(ultimo['vistas'])}\n"
        f"Likes: {_metrica_opcional(ultimo['likes'])}\n"
        f"Comentarios: {_metrica_opcional(ultimo['comentarios'])}\n\n"
    )
    if destacado is not None:
        bloque += (
            "🔥 <b>Más visto de los últimos 30 días</b>\n"
            f'<a href="{destacado["url"]}">{escape(destacado["titulo"])}</a>\n'
            f"{formatear_numero(destacado['vistas'])} vistas\n"
            f"Videos publicados en el período: "
            f"{rendimiento['publicados_30_dias']}\n\n"
        )
    return bloque


def crear_mensaje(
    estadisticas: dict[str, Any],
    comparaciones: dict[str, dict[str, Any] | None],
) -> str:
    """Construye el informe de Telegram con crecimiento y promedios."""
    fecha_actualizacion = datetime.now().strftime("%d/%m/%Y - %H:%M")

    return (
        "🔴 <b>ROJOSTATS</b>\n"
        "<i>Estadísticas digitales de Independiente</i>\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "📺 <b>YouTube</b>\n"
        f"{estadisticas['nombre']}\n\n"
        "👥 <b>Suscriptores</b>\n"
        f"{formatear_numero(estadisticas['suscriptores'])}\n"
        f"{_lineas_variacion('suscriptores', comparaciones)}\n\n"
        "👁️ <b>Visualizaciones totales</b>\n"
        f"{formatear_numero(estadisticas['visualizaciones'])}\n"
        f"{_lineas_variacion('visualizaciones', comparaciones)}\n\n"
        "🎬 <b>Videos publicados</b>\n"
        f"{formatear_numero(estadisticas['videos'])}\n"
        f"{_lineas_variacion('videos', comparaciones)}\n\n"
        "📈 <b>Promedio diario</b>\n"
        f"Últimos 7 días: {_promedio_periodo(comparaciones, '7_dias')}\n"
        f"Últimos 30 días: {_promedio_periodo(comparaciones, '30_dias')}\n\n"
        f"{_rendimiento_videos(estadisticas)}"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "🕒 <b>Última actualización</b>\n"
        f"{fecha_actualizacion}\n\n"
        "Proyecto independiente y no oficial.\n"
        "Datos públicos obtenidos mediante YouTube Data API."
    )
