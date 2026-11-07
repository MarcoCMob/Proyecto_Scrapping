
from google import genai
from google.genai import types
import time
from google.genai.errors import ServerError
from config import settings


def create_gemini_client():

    if not settings.GEMINI_API_KEY:
        raise ValueError(
            "No se encontró GEMINI_API_KEY. "
            "Verifica tu archivo .env"
        )

    return genai.Client(
        api_key=settings.GEMINI_API_KEY
    )


# Cliente reutilizable
client = create_gemini_client()



def generate_response(
    prompt: str,
    system_instruction: str,
    response_schema=None,
    temperature: float = 0.2
):

    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=temperature
    )

    if response_schema is not None:
        config.response_mime_type = "application/json"
        config.response_schema = response_schema

    # Realizar hasta 3 intentos
    max_attempts = 3

    for attempt in range(max_attempts):

        try:

            response = client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt,
                config=config
            )

            if not response.text:
                raise RuntimeError(
                    "Gemini no devolvió una respuesta de texto."
                )

            return response.text

        except ServerError as error:

            # Solo reintentar errores 503
            if getattr(error, "code", None) != 503:
                raise

            # Si ya agotamos los intentos, propagar el error
            if attempt == max_attempts - 1:
                raise

            # Espera exponencial: 2, 4 segundos
            wait_time = 2 ** (attempt + 1)

            print(
                f"Gemini está temporalmente ocupado. "
                f"Reintentando en {wait_time} segundos..."
            )

            time.sleep(wait_time)
