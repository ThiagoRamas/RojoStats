import json
from datetime import datetime, timedelta, timezone
from typing import Any

from config import HISTORY_FILE


METRICAS = ("suscriptores", "visualizaciones", "videos")
ZONA_LOCAL = timezone(timedelta(hours=-3), name="ART")


def cargar_historial() -> list[dict[str, Any]]:
    if not HISTORY_FILE.exists():
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except (json.JSONDecodeError, OSError):
        return []

    return datos if isinstance(datos, list) else []


def guardar_historial(historial: list[dict[str, Any]]) -> None:
    with open(HISTORY_FILE, "w", encoding="utf-8") as archivo:
        json.dump(historial, archivo, ensure_ascii=False, indent=4)


def crear_medicion(
    estadisticas: dict[str, Any],
    fecha: datetime | None = None,
) -> dict[str, Any]:
    instante = (fecha or datetime.now(ZONA_LOCAL)).astimezone(ZONA_LOCAL)
    return {
        "timestamp": instante.isoformat(timespec="seconds"),
        **{metrica: int(estadisticas[metrica]) for metrica in METRICAS},
    }


def registrar_medicion(
    historial: list[dict[str, Any]],
    estadisticas: dict[str, Any],
    fecha: datetime | None = None,
) -> list[dict[str, Any]]:
    actualizado = compactar_historial(
        [*historial, crear_medicion(estadisticas, fecha)],
        fecha,
    )
    guardar_historial(actualizado)
    return actualizado


def _fecha_medicion(medicion: dict[str, Any]) -> datetime:
    return datetime.fromisoformat(str(medicion["timestamp"]))


def compactar_historial(
    historial: list[dict[str, Any]],
    fecha: datetime | None = None,
) -> list[dict[str, Any]]:
    """Conserva detalle reciente y una referencia diaria para el largo plazo."""
    ahora = (fecha or datetime.now(ZONA_LOCAL)).astimezone(ZONA_LOCAL)
    limite_horario = ahora - timedelta(days=7)
    validas = sorted(
        (
            medicion for medicion in historial
            if all(clave in medicion for clave in ("timestamp", *METRICAS))
            and _fecha_medicion(medicion) <= ahora
        ),
        key=_fecha_medicion,
    )

    antiguas_por_dia: dict[str, dict[str, Any]] = {}
    recientes = []
    for medicion in validas:
        instante = _fecha_medicion(medicion)
        if instante >= limite_horario:
            recientes.append(medicion)
        else:
            dia_local = instante.astimezone(ZONA_LOCAL).date().isoformat()
            antiguas_por_dia.setdefault(dia_local, medicion)

    return [*antiguas_por_dia.values(), *recientes]


def _variacion(
    actuales: dict[str, Any],
    referencia: dict[str, Any] | None,
    ahora: datetime,
) -> dict[str, Any] | None:
    if referencia is None:
        return None
    fecha_referencia = _fecha_medicion(referencia)
    dias_transcurridos = max(
        (ahora - fecha_referencia).total_seconds() / 86400,
        1 / 24,
    )
    variaciones = {
        metrica: int(actuales[metrica]) - int(referencia[metrica])
        for metrica in METRICAS
    }
    return {
        "timestamp": referencia["timestamp"],
        "dias_transcurridos": dias_transcurridos,
        "porcentajes": {
            metrica: (
                variaciones[metrica] / int(referencia[metrica]) * 100
                if int(referencia[metrica]) != 0
                else None
            )
            for metrica in METRICAS
        },
        "promedios_diarios": {
            metrica: variaciones[metrica] / dias_transcurridos
            for metrica in METRICAS
        },
        **variaciones,
    }


def calcular_comparaciones(
    historial: list[dict[str, Any]],
    actuales: dict[str, Any],
    fecha: datetime | None = None,
) -> dict[str, dict[str, Any] | None]:
    ahora = (fecha or datetime.now(ZONA_LOCAL)).astimezone(ZONA_LOCAL)
    validas = sorted(
        (
            medicion
            for medicion in historial
            if all(clave in medicion for clave in ("timestamp", *METRICAS))
            and _fecha_medicion(medicion) <= ahora
        ),
        key=_fecha_medicion,
    )

    inicio_dia = ahora.replace(hour=0, minute=0, second=0, microsecond=0)
    mediciones_hoy = [
        medicion for medicion in validas
        if _fecha_medicion(medicion) >= inicio_dia
    ]
    referencia_hoy = mediciones_hoy[0] if mediciones_hoy else (
        validas[-1] if validas else None
    )

    def referencia_periodo(dias: int) -> dict[str, Any] | None:
        objetivo = ahora - timedelta(days=dias)
        candidatas = [
            medicion for medicion in validas
            if _fecha_medicion(medicion) <= objetivo
        ]
        return candidatas[-1] if candidatas else None

    return {
        "hoy": _variacion(actuales, referencia_hoy, ahora),
        "7_dias": _variacion(actuales, referencia_periodo(7), ahora),
        "30_dias": _variacion(actuales, referencia_periodo(30), ahora),
    }
