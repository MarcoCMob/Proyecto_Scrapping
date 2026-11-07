
from services.job_collection_service import collect_and_save_offers

if __name__ == "__main__":
    result = collect_and_save_offers(headless=False)

    print("\nRESUMEN FINAL")
    print("=" * 40)
    print(f"Ofertas extraídas: {result['extracted']}")
    print(f"Ofertas nuevas guardadas: {result['saved']}")
    print(f"Ofertas duplicadas descartadas: {result['duplicates']}")
    print(f"Errores de extracción: {len(result['errors'])}")

    if result["errors"]:
        print("\nOFERTAS CON ERRORES:")

        for error in result["errors"]:
            print(f"- {error['title']}: {error['error']}")
