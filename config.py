
import os
from pathlib import Path
from dotenv import load_dotenv

# Obtener la ruta de la carpeta principal del proyecto
BASE_DIR = Path(__file__).resolve().parent

# Cargar las variables del archivo .env
load_dotenv(BASE_DIR / ".env")


class Settings:

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

    DATABASE_URL = os.getenv("DATABASE_URL")


settings = Settings()
