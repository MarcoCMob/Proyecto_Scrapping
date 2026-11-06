#EXTRACCION DE TEXTO DE ARCHIVOS PDF Y DOCX
#PDF
import fitz

def extract_pdf(file):
    document = fitz.open(
        stream=file.read(),
        filetype="pdf"
    )

    pages = []

    for page in document:
        text = page.get_text()
        pages.append(text)

    return "\n".join(pages)
#DOCX
from docx import Document

def extract_docx(file):

    document = Document(file)

    paragraphs = [
        paragraph.text
        for paragraph in document.paragraphs
    ]

    return "\n".join(paragraphs)

##EXTRACCION GENERAL DE CV IMPLEMENTANDO LAS FUNCIONES DE EXTRACCION DE DOCX Y PDF
def extract_cv(file):

    extension = file.name.lower().split(".")[-1]

    if extension == "pdf":
        return extract_pdf(file)

    elif extension == "docx":
        return extract_docx(file)

    elif extension == "txt":
        return file.read().decode("utf-8")

    raise ValueError("Formato no soportado")