from typing import Any


NOMBRES_METRICAS = {
    "suscriptores": "suscriptores",
    "visualizaciones": "visualizaciones",
}


def _senal_tendencia(
    metrica: str,
    semanal: dict[str, Any],
    mensual: dict[str, Any],
) -> str | None:
    promedio_semanal = float(semanal["promedios_diarios"][metrica])
    promedio_mensual = float(mensual["promedios_diarios"][metrica])
    nombre = NOMBRES_METRICAS[metrica]

    if promedio_semanal < 0:
        return f"⚠️ Descenso semanal de {nombre}."
    if promedio_mensual <= 0:
        return None

    diferencia = (promedio_semanal / promedio_mensual - 1) * 100
    if diferencia >= 25:
        return (
            f"🚀 El ritmo semanal de {nombre} está "
            f"{round(diferencia)} % por encima del mensual."
        )
    if diferencia <= -25:
        return (
            f"📉 El ritmo semanal de {nombre} está "
            f"{round(abs(diferencia))} % por debajo del mensual."
        )
    return None


def calcular_senales(
    estadisticas: dict[str, Any],
    comparaciones: dict[str, dict[str, Any] | None],
) -> list[str]:
    """Genera señales breves únicamente cuando hay evidencia suficiente."""
    senales: list[str] = []
    hoy = comparaciones.get("hoy")
    if hoy is not None and int(hoy["videos"]) > 0:
        cantidad = int(hoy["videos"])
        texto = "video nuevo" if cantidad == 1 else "videos nuevos"
        senales.append(f"🎬 {cantidad} {texto} publicado hoy.")

    rendimiento = estadisticas.get("rendimiento_videos", {})
    ultimo = rendimiento.get("ultimo")
    destacado = rendimiento.get("mas_visto_30_dias")
    if (
        ultimo is not None
        and destacado is not None
        and ultimo.get("id") == destacado.get("id")
        and int(rendimiento.get("publicados_30_dias", 0)) >= 2
    ):
        senales.append("🔥 El último video es el más visto de los últimos 30 días.")

    semanal = comparaciones.get("7_dias")
    mensual = comparaciones.get("30_dias")
    if semanal is not None and mensual is not None:
        for metrica in NOMBRES_METRICAS:
            senal = _senal_tendencia(metrica, semanal, mensual)
            if senal is not None:
                senales.append(senal)

    return senales
