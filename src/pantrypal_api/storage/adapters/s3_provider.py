import boto3
from injector import inject

from src.core.logging.ports.logging_provider import ILoggingProvider
from src.core.storage.ports.object_storage_provider import IObjectStorageProvider


class S3Provider(IObjectStorageProvider):
    """AWS S3 implementation for object storage."""

    @inject
    def __init__(self, logging_provider: ILoggingProvider) -> None:
        self.logging_provider = logging_provider
        self.client = boto3.client("s3")

    def generate_presigned_post(self, bucket: str, key: str, expires_in: int):
        try:
            return self.client.generate_presigned_post(
                Bucket=bucket, Key=key, ExpiresIn=expires_in
            )
        except Exception as exc:  # pragma: no cover - external
            self.logging_provider.error(
                "Failed to generate presigned POST",
                extra_data={"error": str(exc), "bucket": bucket, "key": key},
                tag="S3Provider",
            )
            raise
