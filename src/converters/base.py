from abc import ABC, abstractmethod
from typing import List, Dict

class Converter(ABC):
    """Abstract base class for all converters"""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name of the converter"""

    @property
    @abstractmethod
    def input_formats(self) -> List[str]:
        """List of supported input formats"""

    @property
    @abstractmethod
    def output_formats(self) -> List[str]:
        """List of supported output formats"""

    @abstractmethod
    def convert(self, input_file: str, output_format: str, options: Dict) -> str:
        """
        Convert a file to another format.
        Returns path to converted file.
        """
