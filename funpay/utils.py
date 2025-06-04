import string
import random
import datetime
import re

from funpay.enums import Locale


def random_tag() -> str:
    return "".join(random.choice(string.digits + string.ascii_lowercase) for _ in range(10))


def get_number_month(locale: 'Locale', month: str) -> int:
    if locale == Locale.RU:
        months = {
            "января": 1,
            "февраля": 2,
            "марта": 3,
            "апреля": 4,
            "мая": 5,
            "июня": 6,
            "июля": 7,
            "августа": 8,
            "сентября": 9,
            "октября": 10,
            "ноября": 11,
            "декабря": 12
        }

    else:
        months = {
            "january": 1,
            "february": 2,
            "march": 3,
            "april": 4,
            "may": 5,
            "june": 6,
            "july": 7,
            "august": 8,
            "september": 9,
            "october": 10,
            "november": 11,
            "december": 12
        }

    return months[month]


def string_to_datetime(locale: 'Locale', datetime_string: str) -> datetime.datetime:
    now = datetime.datetime.now(tz=datetime.timezone.utc)

    pattern = r"""
        (\d{1,2})          # Day (1-2 digits)
        \s+                # One or more whitespace characters
        ([а-яё]+)          # Month name (Russian letters)
        \s*                # Optional whitespace
        (?:                # Non-capturing group for year
            (\d{4})        # Year (4 digits)
            ,?             # Optional comma
        )?                 # Year is optional
        \s*                # Optional whitespace
        ,?                 # Optional comma
        \s*                # Optional whitespace
        (\d{1,2}):         # Hours (1-2 digits)
        (\d{2}):           # Minutes (2 digits)
        (\d{2})            # Seconds (2 digits)
    """

    match_search = re.search(pattern, datetime_string, re.VERBOSE)

    if not match_search:
        return now

    day, month, year, hour, minute, second = match_search.groups()

    return datetime.datetime(
        year=year or now.year,
        day=int(day),
        month=get_number_month(locale, month),
        hour=int(hour),
        minute=int(minute),
        second=int(second)
    )

