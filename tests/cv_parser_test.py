from io import BytesIO

import pytest
from docx import Document

from modulos.cv_parser import extract_cv


class FakeUpload(BytesIO):
    """Simula el UploadedFile de Streamlit."""
    def __init__(self, data: bytes, name: str):
        super().__init__(data)
        self.name = name


def test_extract_txt():
    file = FakeUpload("Marco Castro\nJava y Spring Boot".encode("utf-8"), "cv.txt")
    assert "Spring Boot" in extract_cv(file)


def test_extract_docx():
    buffer = BytesIO()
    doc = Document()
    doc.add_paragraph("Desarrollador Java")
    doc.save(buffer)

    file = FakeUpload(buffer.getvalue(), "cv.docx")
    assert "Desarrollador Java" in extract_cv(file)


def test_unsupported_format():
    with pytest.raises(ValueError):
        extract_cv(FakeUpload(b"datos", "cv.png"))


def test_empty_text_raises():
    with pytest.raises(ValueError):
        extract_cv(FakeUpload(b"   ", "cv.txt"))