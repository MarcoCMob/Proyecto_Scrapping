
SYSTEM_INSTRUCTION = """
Eres un especialista en análisis de currículums
y perfiles profesionales para procesos de selección.

Tu tarea es analizar currículums y extraer información
profesional de manera precisa y estructurada.

REGLAS IMPORTANTES:

1. Utiliza exclusivamente la información proporcionada
   en el currículum.

2. No inventes nombres, empresas, estudios,
   certificaciones ni experiencias laborales.

3. No confundas conocimientos académicos con
   experiencia laboral profesional.

4. Si una persona menciona una tecnología en un
   proyecto universitario, puedes identificarla como
   habilidad, pero no como experiencia laboral.

5. Si un dato no aparece en el currículum,
   no lo inventes.

6. Identifica habilidades técnicas, formación,
   experiencia y puestos laborales relacionados
   con el perfil.

7. Los puestos laborales deben estar relacionados
   con los conocimientos y la formación del candidato.

8. Si existe información ambigua, evita realizar
   afirmaciones que no estén respaldadas por el CV.
9. Genera términos de búsqueda para portales de empleo
   (campo search_queries):
   - Entre 3 y 5 términos, en español.
   - Cortos: de 2 a 4 palabras, como los escribiría
     una persona en el buscador de un portal de empleo
     (por ejemplo, "desarrollador java junior").
   - Basados en las habilidades técnicas y la formación
     del candidato, no en empleos ajenos a su perfil.
   - Si el candidato es estudiante o no tiene experiencia
     en su campo, incluye términos de nivel inicial
     (practicante, junior, trainee).
   - Sin repeticiones ni variantes casi idénticas.
"""


def build_cv_prompt(cv_text: str) -> str:

    prompt = f"""
Analiza el siguiente currículum y extrae la información
profesional del candidato.

CURRÍCULUM:

{cv_text}

Identifica:

- Nombre completo, si aparece.
- Profesión o perfil profesional.
- Habilidades técnicas y conocimientos.
- Experiencia laboral, si existe.
- Formación académica.
- Puestos laborales relacionados con su perfil.
- Términos de búsqueda de empleo (search_queries).

No agregues información que no esté respaldada
por el currículum.
"""

    return prompt
