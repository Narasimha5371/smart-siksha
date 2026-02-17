import pytest
from backend.data_processor import DataProcessor

class TestFormatQAForEmbedding:
    @pytest.fixture
    def processor(self):
        # We pass a dummy path to avoid any file system operations during init
        # although __init__ just sets self.jsonl_path.
        return DataProcessor(jsonl_path="dummy.jsonl")

    def test_format_qa_for_embedding_standard(self, processor):
        """Test formatting with all fields present."""
        entry = {
            "question": "What is the capital of France?",
            "options": {"A": "London", "B": "Paris", "C": "Berlin"},
            "explanation": "Paris is the capital.",
            "subject": "Geography",
            "topic": "Capitals"
        }
        expected = """Subject: Geography
Topic: Capitals
Question: What is the capital of France?
Options:
A. London
B. Paris
C. Berlin
Explanation: Paris is the capital."""

        result = processor.format_qa_for_embedding(entry)
        assert result == expected

    def test_format_qa_for_embedding_missing_fields(self, processor):
        """Test formatting with missing optional fields."""
        entry = {
            "question": "Simple question?",
            # No options, explanation, subject, topic
        }
        expected = """Subject:
Topic:
Question: Simple question?
Options:

Explanation: """

        result = processor.format_qa_for_embedding(entry)
        assert result == expected

    def test_format_qa_for_embedding_empty_options(self, processor):
        """Test formatting with empty options dict."""
        entry = {
            "question": "Q",
            "options": {},
            "explanation": "E"
        }
        expected = """Subject:
Topic:
Question: Q
Options:

Explanation: E"""

        result = processor.format_qa_for_embedding(entry)
        assert result == expected

    def test_format_qa_for_embedding_unicode(self, processor):
        """Test formatting with unicode characters."""
        entry = {
            "question": "¿Qué hora es?",
            "options": {"A": "Uno", "B": "Dos"},
            "explanation": "Es la una.",
            "subject": "Español",
            "topic": "Tiempo"
        }
        expected = """Subject: Español
Topic: Tiempo
Question: ¿Qué hora es?
Options:
A. Uno
B. Dos
Explanation: Es la una."""

        result = processor.format_qa_for_embedding(entry)
        assert result == expected

    def test_format_qa_for_embedding_none_values(self, processor):
        """Test formatting with None values if they occur explicitly."""
        entry = {
            "question": None,
            "options": None,
            "explanation": None,
            "subject": None,
            "topic": None
        }

        # Current implementation converts None to string "None" in f-strings
        expected = """Subject: None
Topic: None
Question: None
Options:

Explanation: None"""

        result = processor.format_qa_for_embedding(entry)
        assert result == expected
