"""Base parser interface."""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseParser(ABC):
    """Abstract base class for language parsers."""
    
    @abstractmethod
    def parse(self, code: str) -> Dict[str, Any]:
        """Parse code and return structured data."""
        pass
    
    @abstractmethod
    def get_language(self) -> str:
        """Return the language name."""
        pass
