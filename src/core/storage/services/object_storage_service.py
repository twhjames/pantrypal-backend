from uuid import uuid4

from injector import inject

from src.core.common.constants import SecretKey
from src.core.common.ports.secretkey_provider import ISecretProvider
from src.core.logging.ports.logging_provider import ILoggingProvider
from src.core.storage.ports.object_storage_provider import IObjectStorageProvider


class ObjectStorageService:
    """Provide utilities for interacting with object storage."""

    @inject
    def __init__(
        self,
        storage_provider: IObjectStorageProvider,
        secret_provider: ISecretProvider,
        logging_provider: ILoggingProvider,
    ) -> None:
        self.storage_provider = storage_provider
        self.secret_provider = secret_provider
        self.logging_provider = logging_provider

    def create_upload_url(
        self,
        bucket: str,
        key_prefix: str,
        *,
        extension: str = ".jpg",
        expires_in: int = 300,
    ) -> dict:
        """Generate a presigned POST URL for uploading a file."""
        key = f"{key_prefix}/{uuid4()}{extension}"
        presigned = self.storage_provider.generate_presigned_post(
            bucket=bucket,
            key=key,
            expires_in=expires_in,
        )

        return {"key": key, "upload": presigned}

    def create_receipt_upload_url(self, user_id: int) -> dict | None:
        bucket = self.secret_provider.get_secret(SecretKey.RECEIPT_UPLOAD_BUCKET)
        if not bucket:
            self.logging_provider.error(
                "RECEIPT_UPLOAD_BUCKET is not configured",
                tag="ObjectStorageService",
            )
            return None
        return self.create_upload_url(bucket=bucket, key_prefix=str(user_id))

    def create_receipt_upload_url_poc(self, user_id: int) -> dict | None:
        """Return static AWS endpoints for the receipt pipeline.

        TODO: remove this once the cloud infrastructure supports presigned
        uploads via :meth:`create_receipt_upload_url`.
        """
        upload_url = self.secret_provider.get_secret(SecretKey.RECEIPT_UPLOAD_ENDPOINT)
        retrieve_url = self.secret_provider.get_secret(
            SecretKey.RECEIPT_RETRIEVE_ENDPOINT
        )
        if not upload_url or not retrieve_url:
            self.logging_provider.error(
                "RECEIPT_UPLOAD_ENDPOINT and/or RECEIPT_RETRIEVE_ENDPOINT are not configured",
                tag="ObjectStorageService",
            )
            return None
        receipt_id = str(uuid4())

        return {
            "receipt_id": receipt_id,
            "upload_url": upload_url,
            "retrieve_url": retrieve_url,
        }
