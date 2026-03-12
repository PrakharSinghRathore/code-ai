"""Frontend utilities."""

LANGUAGE_CONFIG = {
    "python": {"name": "Python", "highlight": "python", "ext": ".py"},
    "javascript": {"name": "JavaScript", "highlight": "javascript", "ext": ".js"},
    "typescript": {"name": "TypeScript", "highlight": "typescript", "ext": ".ts"},
    "java": {"name": "Java", "highlight": "java", "ext": ".java"},
    "cpp": {"name": "C++", "highlight": "cpp", "ext": ".cpp"},
    "csharp": {"name": "C#", "highlight": "csharp", "ext": ".cs"},
    "go": {"name": "Go", "highlight": "go", "ext": ".go"},
    "rust": {"name": "Rust", "highlight": "rust", "ext": ".rs"},
    "ruby": {"name": "Ruby", "highlight": "ruby", "ext": ".rb"},
    "php": {"name": "PHP", "highlight": "php", "ext": ".php"},
    "sql": {"name": "SQL", "highlight": "sql", "ext": ".sql"},
}


def get_language_name(lang_id: str) -> str:
    """Get language name by ID."""
    return LANGUAGE_CONFIG.get(lang_id, {}).get("name", lang_id)


def get_language_highlight(lang_id: str) -> str:
    """Get syntax highlighting language."""
    return LANGUAGE_CONFIG.get(lang_id, {}).get("highlight", "plaintext")


def get_language_ext(lang_id: str) -> str:
    """Get file extension for language."""
    return LANGUAGE_CONFIG.get(lang_id, {}).get("ext", ".txt")
