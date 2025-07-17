from abc import ABC, abstractmethod


class IAuthProvider(ABC):
    @abstractmethod
    def verify_password(self, raw_password: str, hashed_password: str) -> bool:
        """Check if the raw password matches the hashed password."""
        raise NotImplementedError

    @abstractmethod
    def generate_token(self, user_id: int) -> str:
        """Generate an access token for the given user ID."""
        raise NotImplementedError

    @abstractmethod
    def get_hashed_password(self, raw_password: str) -> str:
        """Hash the provided raw password securely."""
        raise NotImplementedError

    @abstractmethod
    def decode_token(self, token: str) -> int:
        """Return the user ID encoded in the JWT token."""
        raise NotImplementedError
