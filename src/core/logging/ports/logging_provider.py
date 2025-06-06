from abc import ABC, abstractmethod
from typing import Dict, Optional


class ILoggingProvider(ABC):
    @abstractmethod
    def debug(
        self, message: str, extra_data: Optional[Dict] = None, tag: Optional[str] = None
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def info(
        self, message: str, extra_data: Optional[Dict] = None, tag: Optional[str] = None
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def warning(
        self, message: str, extra_data: Optional[Dict] = None, tag: Optional[str] = None
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def error(
        self, message: str, extra_data: Optional[Dict] = None, tag: Optional[str] = None
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def critical(
        self, message: str, extra_data: Optional[Dict] = None, tag: Optional[str] = None
    ) -> None:
        raise NotImplementedError
