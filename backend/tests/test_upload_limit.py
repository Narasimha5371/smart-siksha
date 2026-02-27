import sys
import os
import io
import pytest
from unittest.mock import MagicMock

# --- MOCKING START ---
# Mock modules that are difficult to install or not needed for this test
# We must do this BEFORE importing main

# Create mock modules
mock_ai_tutor_module = MagicMock()
mock_translator_module = MagicMock()
mock_data_processor_module = MagicMock()
mock_pdfplumber = MagicMock()

# Configure ai_tutor
mock_ai_tutor_obj = MagicMock()
mock_ai_tutor_obj.initialize = MagicMock()
mock_ai_tutor_obj.is_initialized = True
mock_ai_tutor_obj.generate_response = MagicMock(return_value={"answer": "mock", "is_educational": True})
mock_ai_tutor_module.ai_tutor = mock_ai_tutor_obj

# Configure translator
mock_translator_service = MagicMock()
mock_translator_service.get_supported_languages = MagicMock(return_value=["en"])
mock_translator_service.translate = MagicMock(return_value="mock")
mock_translator_module.translation_service = mock_translator_service

# Configure data_processor
mock_dp_obj = MagicMock()
mock_dp_obj.data = []
mock_dp_obj.get_subjects = MagicMock(return_value=[])
mock_dp_obj.get_topics = MagicMock(return_value=[])
mock_dp_obj.get_random_questions = MagicMock(return_value=[])
mock_dp_obj.get_statistics = MagicMock(return_value={})
mock_data_processor_module.data_processor = mock_dp_obj

# Apply mocks to sys.modules
sys.modules["ai_tutor"] = mock_ai_tutor_module
sys.modules["translator"] = mock_translator_module
sys.modules["data_processor"] = mock_data_processor_module
sys.modules["pdfplumber"] = mock_pdfplumber

# Also mock pdfplumber's behavior for the valid file test
# pdfplumber.open() returns a context manager that yields a pdf object
# pdf object has pages, each page has extract_text()
mock_pdf_instance = MagicMock()
mock_page = MagicMock()
mock_page.extract_text.return_value = "Extracted text"
mock_pdf_instance.pages = [mock_page]

# The context manager needs to return the pdf instance
mock_pdf_context = MagicMock()
mock_pdf_context.__enter__.return_value = mock_pdf_instance
mock_pdf_context.__exit__.return_value = None

mock_pdfplumber.open.return_value = mock_pdf_context
# --- MOCKING END ---

# Add backend directory to sys.path so we can import main and config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app
from config import settings

client = TestClient(app)

def test_upload_large_file():
    # Mock settings.MAX_UPLOAD_SIZE to be small
    original_limit = settings.MAX_UPLOAD_SIZE
    settings.MAX_UPLOAD_SIZE = 100  # 100 bytes

    try:
        # Create a file larger than 100 bytes
        file_content = b"a" * 200
        # Create a BytesIO object for the file content
        file_obj = io.BytesIO(file_content)

        files = {"file": ("test_large.pdf", file_obj, "application/pdf")}
        response = client.post("/pdf/upload", files=files)

        assert response.status_code == 413
        assert "File too large" in response.json()["detail"]
    finally:
        settings.MAX_UPLOAD_SIZE = original_limit

def test_upload_valid_file():
    # Mock settings.MAX_UPLOAD_SIZE to allow this file
    original_limit = settings.MAX_UPLOAD_SIZE
    settings.MAX_UPLOAD_SIZE = 1000  # 1000 bytes

    try:
        # Create a minimal PDF file content
        pdf_content = (
            b"%PDF-1.0\n"
            b"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj "
            b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj "
            b"3 0 obj<</Type/Page/MediaBox[0 0 3 3]/Parent 2 0 R>>endobj\n"
            b"xref\n"
            b"0 4\n"
            b"0000000000 65535 f\n"
            b"0000000010 00000 n\n"
            b"0000000060 00000 n\n"
            b"0000000111 00000 n\n"
            b"trailer<</Size 4/Root 1 0 R>>\n"
            b"startxref\n"
            b"190\n"
            b"%%EOF"
        )

        file_obj = io.BytesIO(pdf_content)
        files = {"file": ("test_valid.pdf", file_obj, "application/pdf")}
        response = client.post("/pdf/upload", files=files)

        assert response.status_code == 200
        assert response.json()["text"] == "Extracted text\n"
    finally:
        settings.MAX_UPLOAD_SIZE = original_limit
