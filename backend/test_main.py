import sys
import os

# Add the backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
import unittest.mock as mock

# We need to mock the heavy dependencies before importing main
# as they are initialized on import
sys.modules['chromadb'] = mock.MagicMock()
sys.modules['chromadb.config'] = mock.MagicMock()
sys.modules['sentence_transformers'] = mock.MagicMock()
sys.modules['groq'] = mock.MagicMock()
sys.modules['ollama'] = mock.MagicMock()
sys.modules['libretranslate'] = mock.MagicMock()
sys.modules['pdfplumber'] = mock.MagicMock()
sys.modules['pandas'] = mock.MagicMock()

# Import the actual module, we will mock its internals
import main

# Mock data_processor
mock_data_processor = mock.MagicMock()
mock_data_processor.data = [1, 2, 3] # Some non-empty data
main.data_processor = mock_data_processor

# Mock ai_tutor
mock_ai_tutor = mock.MagicMock()
mock_ai_tutor.is_initialized = True
main.ai_tutor = mock_ai_tutor


client = TestClient(main.app)

def test_health_check_healthy():
    # Make sure we reset mocks to healthy state
    main.ai_tutor.is_initialized = True
    main.data_processor.data = [1, 2, 3]

    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["ai_initialized"] is True
    assert data["data_loaded"] is True

def test_health_check_not_initialized():
    # Simulate uninitialized state
    main.ai_tutor.is_initialized = False
    main.data_processor.data = []

    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["ai_initialized"] is False
    assert data["data_loaded"] is False
