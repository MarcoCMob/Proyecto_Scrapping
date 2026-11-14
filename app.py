import streamlit as st

from modulos.matching.matching_service import MatchingService
from services.cv_matching_service import (
    MAX_QUERIES,
    analyze_cv_file,
    get_search_terms,
    match_profile
)

st.set_page_config(
    page_title="Job Matcher",
    page_icon="💼",
    layout="wide"
)


@st.cache_resource(show_spinner="Cargando modelo de embeddings...")
def get_matching_service() -> MatchingService:
    return MatchingService()


def location_matches(location, filters) -> bool:
    if not filters:
        return True
    return any(f in (location or "").lower() for f in filters)


st.title("Job Matcher")
st.write("Tu buscador inteligente de oportunidades laborales")

uploaded_file = st.file_uploader(
    "Carga tu CV",
    type=["pdf", "docx", "txt"]
)

if uploaded_file is None:
    for key in ("file_key", "profile", "output"):
        st.session_state.pop(key, None)
    st.stop()

# Si cambia el archivo, se descarta el análisis anterior.
file_key = (uploaded_file.name, uploaded_file.size)

if st.session_state.get("file_key") != file_key:
    st.session_state["file_key"] = file_key
    st.session_state.pop("profile", None)
    st.session_state.pop("output", None)

# Paso 1: analizar el CV con Gemini.
if "profile" not in st.session_state:

    if st.button("Analizar CV", type="primary"):
        try:
            with st.spinner("Analizando tu CV con Gemini..."):
                st.session_state["profile"] = analyze_cv_file(uploaded_file)
        except Exception as error:
            st.error(f"No se pudo analizar el CV: {error}")
        else:
            st.rerun()

    st.stop()

profile = st.session_state["profile"]

st.subheader(profile.full_name or "Perfil del candidato")

if profile.profession:
    st.write(profile.profession)

with st.expander("Habilidades detectadas"):
    st.write(", ".join(profile.skills) or "No se detectaron habilidades.")

# Paso 2: términos de búsqueda editables.
st.subheader("Búsquedas en Computrabajo")

terms_text = st.text_area(
    "Un término por línea (puedes editarlos)",
    value="\n".join(get_search_terms(profile)),
    height=150
)

queries = [
    line.strip() for line in terms_text.splitlines() if line.strip()
][:MAX_QUERIES]

col1, col2 = st.columns(2)

max_per_query = col1.number_input(
    "Ofertas por búsqueda",
    min_value=1,
    max_value=20,
    value=10
)

headless = False

if st.button("Buscar ofertas", type="primary", disabled=not queries):
    try:
        with st.status(
            "Buscando y comparando ofertas (puede tardar varios minutos)..."
        ) as status:
            st.session_state["output"] = match_profile(
                profile,
                queries=queries,
                headless=headless,
                max_per_query=int(max_per_query),
                matching_service=get_matching_service()
            )
            status.update(label="Búsqueda completada", state="complete")
    except Exception as error:
        st.error(f"Error durante la búsqueda: {error}")

# Paso 3: resultados.
output = st.session_state.get("output")

if not output:
    st.stop()

st.divider()
st.subheader("Resultados")

location_text = st.text_input(
    "Filtrar por ubicación (separa con comas)",
    placeholder="Lima, Callao"
)

filters = [
    t.strip().lower() for t in location_text.split(",") if t.strip()
]

results = [
    r for r in output["results"]
    if location_matches(r["offer"].location, filters)
]

st.caption(
    f"{len(results)} de {len(output['results'])} ofertas · "
    f"{output['stats']['new']} nuevas en la base · "
    f"{len(output['errors'])} no se pudieron leer"
)

if not results:
    st.info("No hay ofertas que cumplan los filtros.")

for rank, item in enumerate(results, start=1):

    offer = item["offer"]

    with st.container(border=True):
        st.markdown(f"**#{rank} · {offer.title}**")
        st.write(
            f"{offer.company or 'Empresa no indicada'} · "
            f"{offer.location or 'Ubicación no indicada'}"
        )

        st.progress(
            min(max(item["score"], 0.0), 1.0),
            text="Afinidad relativa a esta búsqueda"
        )

        if item["skill_matches"]:
            st.write("Coincide con: " + ", ".join(item["skill_matches"]))

        with st.expander("Ver descripción"):
            st.text(offer.description)

        if offer.url:
            st.link_button("Abrir en Computrabajo", offer.url)

if output["errors"]:
    with st.expander("Ofertas que no se pudieron leer"):
        for error in output["errors"]:
            st.write(f"{error['title']}: {error['error']}")