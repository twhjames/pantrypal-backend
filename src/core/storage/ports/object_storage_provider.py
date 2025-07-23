from abc import ABC, abstractmethod
from typing import Any, Dict


class IObjectStorageProvider(ABC):
    """Provides object storage utilities like presigned uploads."""

    @abstractmethod
    def generate_presigned_post(
        self, bucket: str, key: str, expires_in: int
    ) -> Dict[str, Any]:
        """Return presigned POST data for client upload."""
        raise NotImplementedError
