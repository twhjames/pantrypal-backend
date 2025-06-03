from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext


class DateTimeUtils:
    """Utility class for working with UTC time."""

    @staticmethod
    def get_utc_now() -> datetime:
        """
        Returns the current UTC datetime with timezone info.

        :return: Current datetime in UTC.
        """
        return datetime.now(timezone.utc)

    @staticmethod
    def add_minutes(base_time: datetime, minutes: int) -> datetime:
        """
        Adds the specified number of minutes to a given datetime.

        :param base_time: The base datetime to add minutes to.
        :param minutes: Number of minutes to add.
        :return: A new datetime with minutes added.
        """
        return base_time + timedelta(minutes=minutes)

    @staticmethod
    def add_seconds(base_time: datetime, seconds: int) -> datetime:
        """
        Adds the specified number of seconds to a given datetime.

        :param base_time: The base datetime to add seconds to.
        :param seconds: Number of seconds to add.
        :return: A new datetime with seconds added.
        """
        return base_time + timedelta(seconds=seconds)


class HashUtil:
    """Utility for password hashing and verification using bcrypt."""

    _context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def hash(raw_password: str) -> str:
        """Hash a plain-text password using bcrypt."""
        return HashUtil._context.hash(raw_password)

    @staticmethod
    def verify(raw_password: str, hashed_password: str) -> bool:
        """Verify a plain-text password against a hashed one."""
        return HashUtil._context.verify(raw_password, hashed_password)
