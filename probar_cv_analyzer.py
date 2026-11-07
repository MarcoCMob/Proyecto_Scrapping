import sys

from modulos.cv_parser import extract_cv
from modulos.cv_analyzer import analyze_cv


def main():
    if len(sys.argv) < 2:
        print("Uso: python probar_cv_analyzer.py ruta/a/tu_cv.pdf")
        return

    text = extract_cv(sys.argv[1])
    print(f"Caracteres extraídos: {len(text)}")

    print("\nAnalizando con Gemini...\n")
    profile = analyze_cv(text)

    print(profile.model_dump_json(indent=2))


if __name__ == "__main__":
    main()