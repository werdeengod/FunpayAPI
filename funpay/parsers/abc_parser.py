from typing import Any
from abc import ABC, abstractmethod
import logging

from .exceptions import ParseError


class ABCParser(ABC):
    """Abstract base class defining the interface for all response parsers.

    This class serves as the foundation for implementing custom parsers that transform
    raw API responses into domain objects. All concrete parsers must implement the
    parse() method.

    Note:
        - This is an abstract base class (ABC) - cannot be instantiated directly
        - Designed to work with any response format (JSON, HTML)
    """
    def __init__(self, *args, **kwargs):
        """Initializes the parser with optional arguments.

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        self.logger = logging.getLogger('funpay.Parser')

    def parse(self, **kwargs) -> Any:
        """Transforms raw data into domain objects.

        Returns:
            Any: Parsed data in domain-specific format

        Raises:
            ParserError: If input data cannot be parsed
        """
        try:
            self.logger.debug(f"class={self} data={kwargs}")
            return self._parse_implementation(**kwargs)
        except NotImplementedError:
            raise

        except Exception as e:
            raise ParseError(f"Failed to parse content: {str(e)}") from e

    @abstractmethod
    def _parse_implementation(self, **kwargs) -> Any:
        """Parses HTML content into domain objects (abstract).

        Note:
            Concrete subclasses must implement this method

        Raises:
            NotImplementedError: If not implemented by subclass
        """
        pass
