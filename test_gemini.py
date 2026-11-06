
from modulos.cv_analyzer import analyze_cv


def main():

    texto_prueba = """
    Marco Castro

    Estudiante de Ingeniería de Software de la universidad UTP.

    Conocimientos:
    Java, JavaScript, Python, SQL,
    Spring Boot, React y MySQL.

    Proyecto universitario:
    Desarrollo de una API REST utilizando
    Java y Spring Boot.

    Formación académica:
    Ingeniería de Software.

    Interés profesional:
    Backend Developer y Software Developer.
    """

    print("Analizando perfil con Gemini...\n")

    profile = analyze_cv(texto_prueba)

    print("PERFIL IDENTIFICADO")
    print("-------------------")

    print("Nombre:", profile.full_name)
    print("Profesión:", profile.profession)

    print("\nHabilidades:")
    for skill in profile.skills:
        print("-", skill)

    print("\nPuestos de interés:")
    for position in profile.target_positions:
        print("-", position)

    print("\nFormación:")
    for education in profile.education:
        print("-", education.degree)
        print("  Institución:", education.institution)

    print("\nExperiencia:")
    for experience in profile.experience:
        print("-", experience.position)
        print("  Empresa:", experience.company)
        print("  Descripción:", experience.description)


if __name__ == "__main__":
    main()
