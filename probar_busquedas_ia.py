import sys

from modulos.cv_parser import extract_cv
from modulos.cv_analyzer import analyze_cv


def main():
    if len(sys.argv) < 2:
        print("Uso: python probar_busquedas_ia.py ruta/a/tu_cv.pdf")
        return

    profile = analyze_cv(extract_cv(sys.argv[1]))

    print("Puestos objetivo:")
    for position in profile.target_positions:
        print("-", position)

    print("\nTérminos de búsqueda:")
    for query in profile.search_queries:
        print("-", query)


if __name__ == "__main__":
    main()