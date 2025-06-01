from typing import Any
from abc import ABC, abstractmethod


class ABCParser(ABC):
    """Abstract base class defining the interface for all response parsers.

    This class serves as the foundation for implementing custom parsers that transform
    raw API responses into domain objects. All concrete parsers must implement the
    parse() method.

    Note:
        - This is an abstract base class (ABC) - cannot be instantiated directly
        - Designed to work with any response format (JSON, HTML, XML, etc.)
    """
    def __init__(self, *args, **kwargs):
        """Initializes the parser with optional arguments.

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        pass

    @abstractmethod
    def parse(self) -> Any:
        """Transforms raw data into domain objects.

        This method must be implemented by all concrete subclasses.

        Returns:
            Any: Parsed data in domain-specific format

        Raises:
            ParserError: If input data cannot be parsed
        """
        pass
