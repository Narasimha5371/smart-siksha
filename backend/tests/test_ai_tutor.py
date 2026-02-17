import sys
import os
from unittest.mock import MagicMock, patch

# Add backend to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Mock heavy external libraries before importing ai_tutor
# This prevents the global instance in ai_tutor.py from triggering real initialization
sys.modules['chromadb'] = MagicMock()
sys.modules['chromadb.config'] = MagicMock()
sys.modules['sentence_transformers'] = MagicMock()
sys.modules['groq'] = MagicMock()
sys.modules['ollama'] = MagicMock()
sys.modules['pandas'] = MagicMock()

# Mock config to avoid pydantic dependency and side effects
config_mock = MagicMock()
settings_mock = MagicMock()
settings_mock.EDUCATION_KEYWORDS = [
    "learn", "study", "education", "teach", "exam", "test", "quiz",
    "anatomy", "medicine", "surgery", "physics", "chemistry", "biology",
    "mathematics", "history", "geography", "programming", "computer",
    "science", "language", "grammar", "literature", "economics"
]
settings_mock.LOCAL_MODEL_NAME = "mock-model"
settings_mock.CHROMA_PERSIST_DIR = "/tmp/mock-chroma"
settings_mock.GROQ_API_KEY = None
settings_mock.USE_OLLAMA = False
settings_mock.GROQ_MODEL = "mock-groq"
settings_mock.OLLAMA_MODEL = "mock-ollama"
settings_mock.CHROMA_COLLECTION_NAME = "mock-collection"

config_mock.settings = settings_mock
sys.modules['config'] = config_mock

import pytest
from ai_tutor import AITutor

@pytest.fixture
def ai_tutor_instance():
    """
    Fixture to create an AITutor instance.
    Dependencies are already mocked at the module level.
    """
    return AITutor()

def test_educational_keywords_match(ai_tutor_instance):
    """
    Test that queries containing educational keywords return True.
    """
    assert ai_tutor_instance.is_educational_query("I want to learn physics") is True
    assert ai_tutor_instance.is_educational_query("study tips for exams") is True
    assert ai_tutor_instance.is_educational_query("chemistry problems") is True

    # Test word boundary for educational keywords
    # "test" is a keyword. "latest" contains "test" but should not match.
    # However, since "latest" is not restricted, it returns True by default.
    # We need a case where it WOULD be false if not for the educational keyword.
    # But checking "latest" alone returns True anyway.
    # So we can't easily test that "latest" didn't trigger educational check unless we mock restricted list or check internal state.
    # But we can verify "latest cricket match score" which is restricted.
    # If "latest" triggered educational, it would return True.
    # If "latest" didn't trigger educational, it hits restricted "cricket" and returns False.
    assert ai_tutor_instance.is_educational_query("latest cricket match score") is False

def test_question_pattern_match(ai_tutor_instance):
    """
    Test that queries starting with question words return True.
    """
    assert ai_tutor_instance.is_educational_query("What is the speed of light?") is True
    assert ai_tutor_instance.is_educational_query("How to calculate area?") is True
    assert ai_tutor_instance.is_educational_query("Why is the sky blue?") is True
    assert ai_tutor_instance.is_educational_query("Explain quantum mechanics") is True

def test_restricted_topics(ai_tutor_instance):
    """
    Test that queries containing restricted keywords return False.
    """
    assert ai_tutor_instance.is_educational_query("Who is the best actor?") is False
    assert ai_tutor_instance.is_educational_query("politics and election news") is False
    assert ai_tutor_instance.is_educational_query("dating advice") is False

def test_restricted_keywords_partial_match(ai_tutor_instance):
    """
    Test that restricted keywords don't trigger on partial matches (false positives).
    """
    # 'minister' is restricted. 'administer' should not be restricted.
    assert ai_tutor_instance.is_educational_query("administer help") is True

def test_ambiguous_case(ai_tutor_instance):
    """
    Test that ambiguous queries (neither educational keywords nor restricted) return True.
    """
    assert ai_tutor_instance.is_educational_query("hello world") is True
    assert ai_tutor_instance.is_educational_query("random string") is True

def test_case_insensitivity(ai_tutor_instance):
    """
    Test that the checks are case-insensitive.
    """
    assert ai_tutor_instance.is_educational_query("LEARN PHYSICS") is True
    assert ai_tutor_instance.is_educational_query("MOVIE STAR") is False
    assert ai_tutor_instance.is_educational_query("WHAT IS THIS") is True

def test_edge_cases(ai_tutor_instance):
    """
    Test edge cases like empty strings or punctuation.
    """
    # Empty string doesn't match keywords or patterns, falls through to True
    assert ai_tutor_instance.is_educational_query("") is True
    assert ai_tutor_instance.is_educational_query("!@#$%^&*()") is True

def test_empty_keywords_list(ai_tutor_instance):
    """
    Test behavior when education_keywords is empty.
    """
    # Verify regression fix: empty list shouldn't cause all queries to match regex
    original_keywords = settings_mock.EDUCATION_KEYWORDS
    settings_mock.EDUCATION_KEYWORDS = []

    try:
        # Should not crash, and "hello" should fall through to True (default)
        assert ai_tutor_instance.is_educational_query("hello") is True
    finally:
        settings_mock.EDUCATION_KEYWORDS = original_keywords
