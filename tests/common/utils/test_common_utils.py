from datetime import datetime, timedelta, timezone

from src.core.common.utils import DateTimeUtils, HashUtil


def test_get_utc_now_returns_utc_datetime():
    """Should return datetime object with UTC timezone."""
    now = DateTimeUtils.get_utc_now()
    assert isinstance(now, datetime)
    assert now.tzinfo == timezone.utc


def test_add_minutes_adds_correctly():
    """Should add correct number of minutes to base time."""
    base = datetime(2023, 1, 1, 12, 0, tzinfo=timezone.utc)
    result = DateTimeUtils.add_minutes(base, 30)
    assert result == base + timedelta(minutes=30)


def test_add_seconds_adds_correctly():
    """Should add correct number of seconds to base time."""
    base = datetime(2023, 1, 1, 12, 0, tzinfo=timezone.utc)
    result = DateTimeUtils.add_seconds(base, 90)
    assert result == base + timedelta(seconds=90)


def test_hash_and_verify_password():
    """Should hash password and verify correctness."""
    raw_password = "securepassword123"
    hashed = HashUtil.hash(raw_password)

    assert hashed != raw_password
    assert HashUtil.verify(raw_password, hashed) is True
    assert HashUtil.verify("wrongpassword", hashed) is False
