import pytest
from unittest.mock import AsyncMock, patch
import httpx
from backend.translator import translation_service

@pytest.mark.asyncio
async def test_translate_exception_returns_original_text():
    original_text = "Hello world"

    # Mock httpx.AsyncClient.post to raise an exception
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.side_effect = Exception("Mocked connection error")

        # Act
        result = await translation_service.translate(original_text, source_lang="en", target_lang="hi")

        # Assert
        assert result == original_text
        mock_post.assert_called_once()
