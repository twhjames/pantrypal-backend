from unittest.mock import AsyncMock, MagicMock

import pytest

from src.core.receipt.services.receipt_service import ReceiptService


@pytest.mark.asyncio
async def test_process_receipt_webhook_adds_items():
    pantry_service = MagicMock()
    pantry_service.add_items = AsyncMock()

    chatbot_provider = MagicMock()
    chatbot_provider.handle_single_turn = AsyncMock(
        return_value='[{"ITEM": "Apple", "QUANTITY": 1}]'
    )

    service = ReceiptService(
        pantry_service=pantry_service,
        chatbot_provider=chatbot_provider,
        logging_provider=MagicMock(),
    )

    receipt_json = {"Items": [{"ITEM": "Apple"}]}
    await service.process_receipt_webhook(user_id=1, receipt_json=receipt_json)

    assert pantry_service.add_items.await_count == 1
    chatbot_provider.handle_single_turn.assert_awaited()
