import sys
import os
import pytest
from unittest.mock import mock_open, patch, MagicMock
import json

# Add backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_processor import DataProcessor

class TestDataProcessor:
    def test_load_data_success(self):
        mock_json_content = '{"question": "q1", "subject": "Math", "topic": "Algebra"}\n{"question": "q2", "subject": "Science", "topic": "Physics"}'
        with patch("builtins.open", mock_open(read_data=mock_json_content)):
            dp = DataProcessor(jsonl_path="dummy.jsonl")
            data = dp.load_data()
            assert len(data) == 2
            assert data[0]['question'] == "q1"
            assert data[1]['question'] == "q2"
            assert "Math" in dp.subjects
            assert "Science" in dp.subjects

    def test_load_data_file_not_found(self):
        with patch("builtins.open", side_effect=FileNotFoundError):
            dp = DataProcessor(jsonl_path="nonexistent.jsonl")
            data = dp.load_data()
            assert data == []

    def test_load_data_json_decode_error_partial(self):
        # One valid line, one invalid line, one valid line
        mock_json_content = '{"question": "q1"}\nINVALID_JSON\n{"question": "q3"}'
        with patch("builtins.open", mock_open(read_data=mock_json_content)):
            dp = DataProcessor(jsonl_path="dummy.jsonl")
            data = dp.load_data()
            assert len(data) == 2
            assert data[0]['question'] == "q1"
            assert data[1]['question'] == "q3"

    def test_load_data_json_decode_error_complete(self):
        # All invalid lines
        mock_json_content = 'INVALID_JSON_1\nINVALID_JSON_2'
        with patch("builtins.open", mock_open(read_data=mock_json_content)):
            dp = DataProcessor(jsonl_path="dummy.jsonl")
            data = dp.load_data()
            assert data == []

    def test_load_data_generic_exception(self):
         with patch("builtins.open", side_effect=Exception("Generic error")):
            dp = DataProcessor(jsonl_path="dummy.jsonl")
            data = dp.load_data()
            assert data == []
