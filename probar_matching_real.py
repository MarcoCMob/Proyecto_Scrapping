
from database.connection import SessionLocal
from services.job_offer_service import JobOfferService
from modulos.matching.matching_service import MatchingService
from schemas.cv_schema import CVProfile


def main():

    db = SessionLocal()

    try:
        # 1. Recuperar ofertas desde PostgreSQL.
        job_service = JobOfferService(db)

        response = job_service.search_offers(
            page=1,
            per_page=10
        )

        offers = response["offers"]

        print(f"\nOfertas recuperadas: {len(offers)}")

        if not offers:
            print("No hay ofertas disponibles en PostgreSQL.")
            return

        # 2. Crear un perfil profesional de ejemplo.
        profile = CVProfile(
            profession="Estudiante de Ingeniería de Software",
            skills=[
                "Java",
                "Spring Boot",
                "Python",
                "JavaScript",
                "SQL",
                "PostgreSQL",
                "MySQL",
                "REST APIs",
                "Git",
                "React",
                "Angular"
            ],
            target_positions=[
                "Desarrollador Backend Junior",
                "Desarrollador de Software Junior",
                "Programador Java Junior"
            ]
        )

        # 3. Inicializar el motor de compatibilidad.
        print("\nCargando modelo de embeddings...")

        matching_service = MatchingService()

        # 4. Calcular compatibilidad.
        print("Calculando compatibilidad...\n")

        results = matching_service.match_offers(
            profile,
            offers
        )

        # 5. Mostrar resultados ordenados.
        print("=" * 60)
        print("RESULTADOS DE COMPATIBILIDAD")
        print("=" * 60)

        for index, result in enumerate(results, start=1):

            offer = result["offer"]
            similarity = result["similarity"]

            print(f"\nPUESTO #{index}")
            print(f"Título: {offer.title}")
            print(f"Empresa: {offer.company}")
            print(f"Ubicación: {offer.location}")
            print(
                f"Similitud semántica: {similarity * 100:.2f}%"
            )

        print("\nProceso completado correctamente.")

    finally:
        db.close()


if __name__ == "__main__":
    main()
