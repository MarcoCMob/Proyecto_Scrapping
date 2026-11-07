import sys

from services.cv_matching_service import match_cv_file


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    if not args:
        print("Uso: python probar_flujo_completo.py ruta/cv.pdf [--headless]")
        return

    output = match_cv_file(
        args[0],
        headless="--headless" in sys.argv
    )

    print("\n" + "=" * 60)
    print(f"Perfil: {output['profile'].full_name}")
    print("Búsquedas:", " | ".join(output["queries"]))
    print(f"Estadísticas: {output['stats']}")
    print(f"Errores: {len(output['errors'])}")
    print("=" * 60)

    for i, item in enumerate(output["results"], start=1):
        offer = item["offer"]
        print(
            f"\n#{i:2d}  score {item['score']:.2f}  {offer.title[:70]}"
        )
        print(f"     {offer.company} | {offer.location}")
        print(f"     skills: {', '.join(item['skill_matches']) or '-'}")
        print(f"     {offer.url}")

    for error in output["errors"]:
        print("\nERROR:", error)


if __name__ == "__main__":
    main()