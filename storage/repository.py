import json

from config import DATA_FILE


def cargar_datos() -> dict:
    datos_iniciales = {
        "suscriptores": 0,
        "visualizaciones": 0,
        "videos": 0,
        "message_id": None,
    }

    if not DATA_FILE.exists():
        guardar_datos(datos_iniciales)
        return datos_iniciales

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    except json.JSONDecodeError:
        guardar_datos(datos_iniciales)
        return datos_iniciales


def guardar_datos(datos: dict) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as archivo:
        json.dump(
            datos,
            archivo,
            ensure_ascii=False,
            indent=4,
        )