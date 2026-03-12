"""Utility functions."""

from .config import SUPPORTED_LANGUAGES, DIAGRAM_TYPES


def get_languages():
    """Get list of supported languages."""
    return [{"id": k, "name": v["name"]} for k, v in SUPPORTED_LANGUAGES.items()]


def get_diagram_types():
    """Get list of diagram types."""
    return DIAGRAM_TYPES


__all__ = [
    "SUPPORTED_LANGUAGES",
    "DIAGRAM_TYPES",
    "get_languages",
    "get_diagram_types",
]
