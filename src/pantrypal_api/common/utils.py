from datetime import datetime, timezone


class TimeUtils:
    @staticmethod
    def get_utc_now() -> datetime:
        """
        Returns the current UTC time as a timezone-aware datetime object.
        """
        return datetime.now(timezone.utc)
