from abc import ABC, abstractmethod
from typing import Optional

from src.core.common.constants import SecretKey


class ISecretProvider(ABC):
    @abstractmethod
    def get_secret(
        self, key: SecretKey, default: Optional[str] = None
    ) -> Optional[str]:
        raise NotImplementedError
