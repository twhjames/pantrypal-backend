from typing import Any, Dict

from pydantic import BaseModel


class ReceiptWebhookRequest(BaseModel):
    user_id: int
    receipt: Dict[str, Any]


class ReceiptUploadRequest(BaseModel):
    image_base64: str
