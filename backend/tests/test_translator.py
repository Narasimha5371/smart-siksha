import sys
import os
import asyncio
from unittest.mock import patch, MagicMock

# Add backend directory to sys.path so we can import translator
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# We need to mock httpx and config because they are missing in the test environment.
# To avoid polluting sys.modules globally, we will mock them inside the test using patch.dict.

def test_translation_service_exception_fallback():
    """
    Test that TranslationService.translate returns the original text
    when httpx.AsyncClient().post raises an exception.
    """
    mock_httpx = MagicMock()
    mock_config = MagicMock()
    mock_config.settings = MagicMock()
    mock_config.settings.LIBRETRANSLATE_URL = "http://mock-libretranslate"
    mock_config.settings.LIBRETRANSLATE_API_KEY = "mock-key"

    with patch.dict('sys.modules', {'httpx': mock_httpx, 'config': mock_config}):
        # Import inside the patched context to resolve dependencies
        from translator import TranslationService

        service = TranslationService()

        # We patch httpx.AsyncClient to return a mock client
        # and its post method to raise an exception
        with patch("translator.httpx.AsyncClient") as mock_client_class:
            # Create a mock for the client instance
            mock_client = MagicMock()

            # Make the context manager return our mock client
            mock_client_class.return_value.__aenter__.return_value = mock_client

            # Make the post method raise an exception when awaited
            async def mock_post(*args, **kwargs):
                raise Exception("Mocked connection error")

            mock_client.post = mock_post

            # Test string
            original_text = "Hello, world!"

            # Run the async translate function
            result = asyncio.run(service.translate(original_text, "en", "hi"))

            # Verify it returns the original text
            assert result == original_text
