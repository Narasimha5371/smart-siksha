import sys
import os
import json
from unittest.mock import MagicMock, patch, mock_open
import pytest

# Add backend directory to sys.path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock dependencies BEFORE importing the module under test
config_mock = MagicMock()
settings_mock = MagicMock()
settings_mock.JSONL_DATA_PATH = "dummy_path.jsonl"
config_mock.settings = settings_mock
sys.modules['config'] = config_mock

# Now import the module under test
try:
    from data_processor import DataProcessor, data_processor
except ImportError as e:
    pytest.fail(f"Failed to import data_processor: {e}")

def test_data_processor_import():
    """Test that DataProcessor can be imported and instantiated"""
    dp = DataProcessor()
    assert dp is not None
    assert dp.jsonl_path == "dummy_path.jsonl"

def test_load_data():
    """Test load_data with mocked file"""
    dp = DataProcessor()

    mock_data = '{"subject": "Math", "topic": "Algebra", "question": "Q1", "options": {"A": "1"}, "correct_answer_index": 0}\n'

    with patch("builtins.open", mock_open(read_data=mock_data)):
        data = dp.load_data()
        assert len(data) == 1
        assert data[0]["subject"] == "Math"
        assert "Math" in dp.subjects
        assert "Algebra" in dp.topics

def test_get_subjects():
    dp = DataProcessor()
    dp.subjects = {"Math", "Science"}
    # set order is not guaranteed, but get_subjects sorts it
    subjects = dp.get_subjects()
    assert subjects == ["Math", "Science"]

def test_filter_by_subject():
    dp = DataProcessor()
    dp.data = [
        {"subject": "Math", "question": "Q1"},
        {"subject": "Science", "question": "Q2"}
    ]
    math_q = dp.filter_by_subject("Math")
    assert len(math_q) == 1
    assert math_q[0]["question"] == "Q1"
