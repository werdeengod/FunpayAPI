import string
import random
import datetime
import re

from funpay.enums import Locale, StatusOrder


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
    def format_time(data: str) -> int:
        return int(data[1] if len(data) == 2 and data[0] == "0" else data)

    now = datetime.datetime.now(tz=datetime.timezone.utc)

    pattern = r"""
        (\d{1,2})                  # Day (1-2 digits)
        \s+                        # Whitespace
        ([а-яёa-z]+)               # Month name (Russian or English)
        \s*                        # Optional whitespace
        (?:                        # Optional year
            (\d{4})                # Year (4 digits)
            \s*                    # Optional whitespace
        )?
        \s*                        # Optional whitespace
        (?:в|at|,\s*)              # "в", "at" or comma with optional space
        \s*                        # Optional whitespace
        (\d{1,2})                  # Hours (1-2 digits)
        :                          # Colon
        (\d{2})                    # Minutes (2 digits)
        (?:                        # Optional seconds
            :(\d{2})               # Seconds (2 digits)
        )?
    """

    match_search = re.search(pattern, datetime_string, re.VERBOSE)

    if not match_search:
        return now

    day, month, year, hour, minute, second = match_search.groups()

    return datetime.datetime(
        year=year or now.year,
        day=int(day),
        month=get_number_month(locale, month),
        hour=format_time(hour),
        minute=format_time(minute),
        second=format_time(second) if second else 0
    )


def get_order_status_from_string(locale: 'Locale', status_string: str):
    if locale == Locale.RU:
        statuses = {
            "Закрыт": StatusOrder.CLOSED,
            "Оплачен": StatusOrder.PAID,
            "Возврат": StatusOrder.REFUNDED
        }

    else:
        statuses = {
            "Closed": StatusOrder.CLOSED,
            "Paid": StatusOrder.PAID,
            "Refund": StatusOrder.REFUNDED
        }

    status = statuses.get(status_string)
    return status
