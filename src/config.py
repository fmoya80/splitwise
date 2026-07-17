"""Configuration loaded from local environment variables."""

import os

from dotenv import load_dotenv


BASE_URL = "https://secure.splitwise.com/api/v3.0"

load_dotenv()
SPLITWISE_API_KEY = os.getenv("SPLITWISE_API_KEY")

if not SPLITWISE_API_KEY:
    raise RuntimeError(
        "Falta SPLITWISE_API_KEY. Cree un archivo .env basado en .env.example "
        "y agregue allí su API Key de Splitwise."
    )
