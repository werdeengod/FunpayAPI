from typing import TYPE_CHECKING

from funpay.types import RaiseNode
from .base_json_parser import BaseJsonParser

if TYPE_CHECKING:
    from funpay.types import Node


class RaiseNodeJsonParser(BaseJsonParser):
    """Parser to retrieve raised nodes from link https://funpay.com/lots/raise"""

    def _parse_implementation(self, node: 'Node') -> 'RaiseNode':
        return RaiseNode(
            node=node,
            message=self.data.get('msg'),
            success=not bool(self.data.get('error'))
        )