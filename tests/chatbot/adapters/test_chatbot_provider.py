import pytest

from src.pantrypal_api.chatbot.adapters.chatbot_provider import GroqChatbotProvider


@pytest.mark.asyncio
async def test_handle_single_turn(monkeypatch, mock_secret_key_provider):
    provider = GroqChatbotProvider(secret_provider=mock_secret_key_provider)

    async def mock_handle_single_turn(msg):
        return "Here's a fake recipe!"

    monkeypatch.setattr(provider, "handle_single_turn", mock_handle_single_turn)

    result = await provider.handle_single_turn("msg")
    assert result == "Here's a fake recipe!"


@pytest.mark.asyncio
async def test_handle_multi_turn(monkeypatch, mock_secret_key_provider):
    provider = GroqChatbotProvider(secret_provider=mock_secret_key_provider)

    async def mock_handle_multi_turn(msg, history=None):
        return "Mocked multi-turn completion"

    monkeypatch.setattr(provider, "handle_multi_turn", mock_handle_multi_turn)

    result = await provider.handle_multi_turn("msg")
    assert result == "Mocked multi-turn completion"
