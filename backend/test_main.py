import sys
from unittest.mock import MagicMock, patch

# Mock heavy dependencies before importing main
sys.modules['chromadb'] = MagicMock()
sys.modules['chromadb.config'] = MagicMock()
sys.modules['sentence_transformers'] = MagicMock()
sys.modules['groq'] = MagicMock()
sys.modules['ollama'] = MagicMock()
sys.modules['libretranslate'] = MagicMock()
sys.modules['pandas'] = MagicMock()
sys.modules['uvicorn'] = MagicMock()
sys.modules['pdfplumber'] = MagicMock()

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_health_check_healthy():
    """Test health check when AI is initialized and data is loaded."""
    with patch("main.ai_tutor.is_initialized", True), \
         patch("main.data_processor.data", [1, 2, 3]):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {
            "status": "healthy",
            "ai_initialized": True,
            "data_loaded": True
        }

def test_health_check_not_initialized_empty_data():
    """Test health check when AI is not initialized and data is empty."""
    with patch("main.ai_tutor.is_initialized", False), \
         patch("main.data_processor.data", []):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {
            "status": "healthy",
            "ai_initialized": False,
            "data_loaded": False
        }
