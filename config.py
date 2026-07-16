import os
from pathlib import Path

from dotenv import load_dotenv


# Carpeta principal del proyecto
BASE_DIR = Path(__file__).resolve().parent

# Carga el archivo .env ubicado en la carpeta principal
load_dotenv(BASE_DIR / ".env")


TELEGRAM_TOKEN = os.getenv("TOKEN")
TELEGRAM_CHANNEL = os.getenv("CANAL")

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_HANDLE = os.getenv("YOUTUBE_HANDLE", "@Independiente")

DATA_FILE = BASE_DIR / "datos.json"


def validar_configuracion() -> None:
    """Comprueba que estén configuradas todas las variables necesarias."""

    variables_faltantes = []

    if not TELEGRAM_TOKEN:
        variables_faltantes.append("TOKEN")

    if not TELEGRAM_CHANNEL:
        variables_faltantes.append("CANAL")

    if not YOUTUBE_API_KEY:
        variables_faltantes.append("YOUTUBE_API_KEY")

    if not YOUTUBE_HANDLE:
        variables_faltantes.append("YOUTUBE_HANDLE")

    if variables_faltantes:
        faltantes = ", ".join(variables_faltantes)

        raise ValueError(
            f"Faltan variables en el archivo .env: {faltantes}"
        )