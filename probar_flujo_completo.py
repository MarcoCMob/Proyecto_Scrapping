import sys

from services.cv_matching_service import match_cv_file


def main():
    if len(sys.argv) < 2:
        print("Uso: python probar_flujo_completo.py ruta/a/tu_cv.pdf")
        return

    output = match_cv_file(sys.argv[1])

    print(f"Perfil: {output['profile'].full_name}")
    print(f"Ofertas comparadas: {len(output['results'])}\n")

    for i, item in enumerate(output["results"], start=1):
        offer = item["offer"]
        print(
            f"#{i:2d}  score {item['score']:.2f}  "
            f"sim {item['similarity'] * 100:.1f}%  {offer.title[:60]}"
        )
        print(f"      skills: {', '.join(item['skill_matches']) or '-'}")


if __name__ == "__main__":
    main()