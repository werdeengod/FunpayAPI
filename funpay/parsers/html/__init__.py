from typing import Union

from .base_html_parser import BaseHtmlParser
from .account_parser import FunpayUserLotsParser, FunpayUserProfileParser, FunpayUserReviewsParser, \
    FunpayUserNodeIdsParser
from .lots_trade_parser import FunpayLotGameIdParser


UserParser = Union[
    FunpayUserLotsParser,
    FunpayUserNodeIdsParser,
    FunpayUserProfileParser,
    FunpayUserReviewsParser
]
