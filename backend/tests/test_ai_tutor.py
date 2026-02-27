import unittest
from unittest.mock import MagicMock, patch, AsyncMock
import sys
import os

# Mock dependencies before importing ai_tutor
sys.modules['chromadb'] = MagicMock()
sys.modules['chromadb.config'] = MagicMock()
sys.modules['sentence_transformers'] = MagicMock()
sys.modules['groq'] = MagicMock()
sys.modules['ollama'] = MagicMock()
sys.modules['pandas'] = MagicMock()

# Add backend to path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestAITutor(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        # Start patching ai_tutor.settings
        self.patcher = patch('ai_tutor.settings')
        self.mock_settings = self.patcher.start()

        # Setup mocks
        self.mock_settings.LOCAL_MODEL_NAME = "test-model"
        self.mock_settings.CHROMA_PERSIST_DIR = "test-db"
        self.mock_settings.GROQ_API_KEY = "test-key"
        self.mock_settings.USE_OLLAMA = False
        self.mock_settings.GROQ_MODEL = "mixtral-8x7b-32768"
        self.mock_settings.EDUCATION_KEYWORDS = ["learn", "study"]
        self.mock_settings.OLLAMA_MODEL = "llama3"

        # Configure ollama mock
        import ollama
        ollama.chat.return_value = {'message': {'content': 'Ollama response'}}

        # Import AITutor after patching
        from ai_tutor import AITutor
        self.AITutor = AITutor

        self.ai_tutor = AITutor()

        # Mock methods that might be called
        self.ai_tutor.is_educational_query = MagicMock(return_value=True)
        self.ai_tutor.search_similar = AsyncMock(return_value=[
            {
                "subject": "Math",
                "topic": "Algebra",
                "question": "What is x?",
                "correct_answer": "x is a variable",
                "explanation": "It varies"
            }
        ])

        # Mock Groq client inside ai_tutor
        self.ai_tutor.groq_client = MagicMock()

    def tearDown(self):
        self.patcher.stop()

    async def test_generate_response_educational_groq(self):
        # Ensure USE_OLLAMA is False
        self.mock_settings.USE_OLLAMA = False

        # Debug check
        import ai_tutor
        # print(f"DEBUG TEST: ai_tutor.settings type: {type(ai_tutor.settings)}")

        # Mock Groq client response
        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = "This is an AI response."
        self.ai_tutor.groq_client.chat.completions.create.return_value = mock_completion

        response = await self.ai_tutor.generate_response("What is math?")

        self.assertEqual(response["answer"], "This is an AI response.")
        self.assertTrue(response["is_educational"])
        self.assertEqual(response["subject"], "Math")

    async def test_generate_response_non_educational(self):
        self.ai_tutor.is_educational_query.return_value = False

        response = await self.ai_tutor.generate_response("Who won the game?")

        self.assertFalse(response["is_educational"])
        self.assertIn("study buddy", response["answer"])

    async def test_generate_response_fallback(self):
        self.mock_settings.USE_OLLAMA = False
        # Mock exception in AI generation
        self.ai_tutor.groq_client.chat.completions.create.side_effect = Exception("API Error")

        response = await self.ai_tutor.generate_response("What is math?")

        self.assertTrue(response["is_educational"])
        # Should fall back to the similar item
        self.assertIn("**Answer**: x is a variable", response["answer"])

if __name__ == '__main__':
    unittest.main()
