from io import BytesIO
from pathlib import Path

import pymupdf
from docx import Document

SUPPORTED_EXTENSIONS = {"pdf", "docx", "txt"}


def _get_name(file) -> str:
    if isinstance(file, (str, Path)):
        return str(file)
    return getattr(file, "name", "") or ""


def _read_bytes(file) -> bytes:
    """Lee el archivo completo una sola vez y devuelve bytes."""
    if isinstance(file, (str, Path)):
        return Path(file).read_bytes()

    if hasattr(file, "seek"):
        file.seek(0)

    data = file.read()

    if isinstance(data, str):
        data = data.encode("utf-8")

    return data


def extract_pdf(data: bytes) -> str:
    with pymupdf.open(stream=data, filetype="pdf") as document:
        return "\n".join(page.get_text() for page in document)


def extract_docx(data: bytes) -> str:
    document = Document(BytesIO(data))

    parts = [p.text for p in document.paragraphs]

    # Muchos CVs organizan su contenido en tablas.
    for table in document.tables:
        for row in table.rows:
            cells = [c.text.strip() for c in row.cells if c.text.strip()]
            if cells:
                parts.append(" | ".join(cells))

    return "\n".join(parts)


def extract_txt(data: bytes) -> str:
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("latin-1")


def extract_cv(file) -> str:
    """
    Extrae el texto de un CV (PDF, DOCX o TXT).
    Acepta una ruta o un archivo con .name y .read()
    (por ejemplo, el UploadedFile de Streamlit).
    """
    extension = _get_name(file).lower().rsplit(".", 1)[-1]

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            "Formato no soportado. Usa PDF, DOCX o TXT."
        )

    data = _read_bytes(file)

    if extension == "pdf":
        text = extract_pdf(data)
    elif extension == "docx":
        text = extract_docx(data)
    else:
        text = extract_txt(data)

    if not text.strip():
        raise ValueError(
            "No se pudo extraer texto del CV. Si es un PDF "
            "escaneado (imagen), sube una versión con texto "
            "seleccionable o un DOCX."
        )

    return text