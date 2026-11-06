from pydantic import ValidationError

from schemas.cv_schema import CVProfile

from modulos.ai.gemini_client import generate_response

from modulos.ai.prompts.cv_prompt import (
    SYSTEM_INSTRUCTION,
    build_cv_prompt
)


def analyze_cv(cv_text: str) -> CVProfile:

    if not cv_text or not cv_text.strip():
        raise ValueError(
            "El currículum no contiene texto para analizar."
        )

    # 1. Construir el prompt con el contenido del CV
    prompt = build_cv_prompt(cv_text)

    # 2. Enviar el texto a Gemini solicitando
    # una respuesta estructurada según CVProfile
    response_text = generate_response(
        prompt=prompt,
        system_instruction=SYSTEM_INSTRUCTION,
        response_schema=CVProfile
    )

    # 3. Validar y convertir la respuesta JSON
    # en un objeto CVProfile
    try:
        profile = CVProfile.model_validate_json(
            response_text
        )

    except ValidationError as error:
        raise ValueError(
            "Gemini devolvió información que no cumple "
            "con el esquema del perfil."
        ) from error

    return profile
