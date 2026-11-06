import streamlit as st

st.set_page_config(
    page_title="Job Matcher",
    page_icon="💼",
    layout="wide"
)

st.title("Job Matcher")
st.write(
    "Tu buscador inteligente de oportunidades laborales"
)

uploaded_file = st.file_uploader(
    "Carga tu CV",
    type=["pdf", "docx", "txt"]
)

if uploaded_file:
    st.success("CV cargado correctamente")