import datetime
from typing import TYPE_CHECKING

from funpay.types import User
from funpay.enums import Locale
from funpay.utils import string_to_datetime

from .base_html_parser import BaseHtmlParser

if TYPE_CHECKING:
    from bs4 import Tag


class FunpayUserProfileHtmlParser(BaseHtmlParser):
    """Parser for get profile from link https://funpay.com/users/{USER_ID}/"""
    def _extract_profile_container(self) -> 'Tag':
        return self.soup.find("div", {"class": "profile"})

    def _parse_implementation(self, locale: 'Locale', user_id: int) -> 'User':
        profile_container = self._extract_profile_container()

        user_title_data = self.get_text(profile_container, "h1").split()

        banned = False
        username = user_title_data[0]
        last_online_string = " ".join((x for x in user_title_data[1:])).strip()

        if last_online_string.lower() in ("online", "онлайн"):
            last_online = datetime.datetime.now(tz=datetime.timezone.utc)

        elif last_online_string.lower() in ("заблокирован", "banned"):
            banned, last_online = True, None

        else:
            string_datetime = last_online_string.split('(')[0][4:]
            last_online = string_to_datetime(
                locale=locale,
                datetime_string=string_datetime
            )

        created_date_string = profile_container.find(
            "div", {"class": "profile-header-cols"}
        ).find_next("div").find_next("div").text.strip()

        created_date = string_to_datetime(
            locale=locale,
            datetime_string=created_date_string.split('\n')[0]
        )

        return User(
            id=user_id,
            created_date=created_date,
            last_online=last_online,
            username=username,
            banned=banned
        )








