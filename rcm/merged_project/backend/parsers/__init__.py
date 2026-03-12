"""Code parsers for multiple languages."""

from .base import BaseParser
from .python_parser import PythonParser
from .javascript_parser import JavaScriptParser
from .sql_parser import SQLParser
from .generic_parser import (
    GenericParser,
    create_java_parser,
    create_cpp_parser,
    create_csharp_parser,
    create_go_parser,
    create_rust_parser,
    create_ruby_parser,
    create_php_parser,
)


def get_parser(language: str) -> BaseParser:
    """Get parser instance for the specified language."""
    parsers = {
        "python": PythonParser(),
        "javascript": JavaScriptParser(),
        "typescript": JavaScriptParser(),
        "sql": SQLParser(),
        "java": create_java_parser(),
        "cpp": create_cpp_parser(),
        "csharp": create_csharp_parser(),
        "go": create_go_parser(),
        "rust": create_rust_parser(),
        "ruby": create_ruby_parser(),
        "php": create_php_parser(),
    }
    return parsers.get(language.lower())


__all__ = [
    "BaseParser",
    "PythonParser",
    "JavaScriptParser", 
    "SQLParser",
    "GenericParser",
    "get_parser",
]
