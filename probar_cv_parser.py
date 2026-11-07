import sys

from modulos.cv_parser import extract_cv


def main():
    if len(sys.argv) < 2:
        print("Uso: python probar_cv_parser.py ruta/a/tu_cv.pdf")
        return

    text = extract_cv(sys.argv[1])

    print(f"Caracteres extraídos: {len(text)}")
    print("=" * 60)
    print(text[:1000])


if __name__ == "__main__":
    main()