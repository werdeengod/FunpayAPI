from typing import TYPE_CHECKING

from funpay.types import RaiseNode
from .base_json_parser import BaseJsonParser

if TYPE_CHECKING:
    from funpay.types import Node


class RaiseNodeParser(BaseJsonParser):
    def _parse_implementation(self, node: 'Node') -> 'RaiseNode':
        return RaiseNode(
            node=node,
            message=self.data.get('msg'),
            success=not bool(self.data.get('error'))
        )