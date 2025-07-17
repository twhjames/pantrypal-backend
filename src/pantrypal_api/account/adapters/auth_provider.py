from injector import inject
from jose import jwt

from src.core.account.ports.auth_provider import IAuthProvider
from src.core.common.constants import SecretKey
from src.core.common.ports.secretkey_provider import ISecretProvider
from src.core.common.utils import DateTimeUtils, HashUtil
from src.core.logging.ports.logging_provider import ILoggingProvider


class AuthProvider(IAuthProvider):
    """Handles password hashing/verification and JWT token generation."""

    @inject
    def __init__(
        self,
        secret_provider: ISecretProvider,
        logging_provider: ILoggingProvider,
    ):
        self.secret_provider = secret_provider
        self.logging_provider = logging_provider

    def get_hashed_password(self, raw_password: str) -> str:
        """Hash the provided raw password securely."""
        return HashUtil.hash(raw_password)

    def verify_password(self, raw_password: str, hashed_password: str) -> bool:
        """Check if the raw password matches the hashed password."""
        return HashUtil.verify(raw_password, hashed_password)

    def generate_token(self, user_id: int) -> str:
        """Generate a JWT access token for the given user ID."""
        secret_key = self.__get_secret_key()
        algorithm = self.__get_algorithm()
        expire_minutes = self.__get_expiry_minutes()

        expire = DateTimeUtils.add_minutes(DateTimeUtils.get_utc_now(), expire_minutes)
        payload = {"sub": str(user_id), "exp": expire}

        return jwt.encode(payload, secret_key, algorithm=algorithm)

    def decode_token(self, token: str) -> int:
        """Decode a JWT token and return the user id."""
        secret_key = self.__get_secret_key()
        algorithm = self.__get_algorithm()
        try:
            payload = jwt.decode(token, secret_key, algorithms=[algorithm])
            user_id_str = payload.get("sub")
            if user_id_str is None:
                raise ValueError("Token missing subject")
            return int(user_id_str)
        except Exception as e:  # JWTError or ValueError
            self.logging_provider.warning(
                "Failed to decode auth token",
                extra_data={"error": str(e)},
                tag="AuthProvider",
            )
            raise ValueError("Invalid token")

    def __get_secret_key(self) -> str:
        key = self.secret_provider.get_secret(SecretKey.AUTH_SECRET_KEY)
        if not key:
            self.logging_provider.error(
                "Missing AUTH_SECRET_KEY in environment", tag="AuthProvider"
            )
            raise ValueError("AUTH_SECRET_KEY is missing from environment")
        return key

    def __get_algorithm(self) -> str:
        return self.secret_provider.get_secret(SecretKey.AUTH_ALGORITHM)

    def __get_expiry_minutes(self) -> int:
        try:
            return int(
                self.secret_provider.get_secret(SecretKey.AUTH_TOKEN_EXPIRY_MINUTES)
            )
        except (TypeError, ValueError) as e:
            self.logging_provider.error(
                "Invalid AUTH_TOKEN_EXPIRY_MINUTES value in environment",
                extra_data={"error": str(e)},
                tag="AuthProvider",
            )
            raise ValueError("Invalid AUTH_TOKEN_EXPIRY_MINUTES value in .env")
