from funpay.types import RaiseNode
from .base_json_parser import BaseJsonParser


class RaiseNodeParser(BaseJsonParser):
    def parse(self) -> 'RaiseNode':
        return RaiseNode(
            node_id=self.data.get('node_id'),
            message=self.data.get('msg'),
            success=not bool(self.data.get('error'))
        )