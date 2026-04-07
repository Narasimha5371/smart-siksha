import sys
from unittest.mock import MagicMock

# Mock heavy modules before importing main
sys.modules['chromadb'] = MagicMock()
sys.modules['chromadb.config'] = MagicMock()
sys.modules['sentence_transformers'] = MagicMock()
sys.modules['groq'] = MagicMock()
sys.modules['ollama'] = MagicMock()
sys.modules['pdfplumber'] = MagicMock()
sys.modules['pandas'] = MagicMock()

from fastapi.testclient import TestClient
from unittest.mock import patch

from backend.main import app

client = TestClient(app)

@patch("backend.main.translation_service.get_supported_languages")
def test_get_languages(mock_get_supported_languages):
    mock_get_supported_languages.return_value = {
        "en": "English",
        "hi": "Hindi - हिंदी"
    }

    response = client.get("/languages")

    assert response.status_code == 200
    assert response.json() == {
        "en": "English",
        "hi": "Hindi - हिंदी"
    }
    mock_get_supported_languages.assert_called_once()
