"""Frontend utilities."""

from .helpers import LANGUAGE_CONFIG, get_language_name, get_language_highlight, get_language_ext
from .theme import apply_theme, DARK_THEME, LIGHT_THEME
from .diagram_renderer import render_mermaid_diagram, download_svg_link, render_diagram_with_fallback

__all__ = [
    "LANGUAGE_CONFIG",
    "get_language_name",
    "get_language_highlight",
    "get_language_ext",
    "apply_theme",
    "DARK_THEME",
    "LIGHT_THEME",
    "render_mermaid_diagram",
    "download_svg_link",
    "render_diagram_with_fallback",
]
