import os

import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_HANDLE = os.getenv("YOUTUBE_HANDLE", "@Independiente")


def obtener_estadisticas_canal() -> dict:
    if not API_KEY:
        raise ValueError(
            "No se encontró YOUTUBE_API_KEY en el archivo .env."
        )

    url = "https://www.googleapis.com/youtube/v3/channels"

    parametros = {
        "part": "snippet,statistics",
        "forHandle": YOUTUBE_HANDLE,
        "key": API_KEY,
    }

    respuesta = requests.get(
        url,
        params=parametros,
        timeout=20,
    )

    respuesta.raise_for_status()
    datos = respuesta.json()

    if not datos.get("items"):
        raise ValueError(
            f"No se encontró ningún canal con el handle {YOUTUBE_HANDLE}."
        )

    canal = datos["items"][0]
    informacion = canal["snippet"]
    estadisticas = canal["statistics"]

    return {
        "id_canal": canal["id"],
        "nombre": informacion["title"],
        "suscriptores": int(estadisticas.get("subscriberCount", 0)),
        "visualizaciones": int(estadisticas.get("viewCount", 0)),
        "videos": int(estadisticas.get("videoCount", 0)),
    }


def formatear_numero(numero: int) -> str:
    return f"{numero:,}".replace(",", ".")


def main() -> None:
    canal = obtener_estadisticas_canal()

    print("Datos obtenidos correctamente:")
    print(f"Canal: {canal['nombre']}")
    print(f"ID: {canal['id_canal']}")
    print(
        f"Suscriptores: {formatear_numero(canal['suscriptores'])}"
    )
    print(
        f"Visualizaciones: {formatear_numero(canal['visualizaciones'])}"
    )
    print(
        f"Videos públicos: {formatear_numero(canal['videos'])}"
    )


if __name__ == "__main__":
    main()