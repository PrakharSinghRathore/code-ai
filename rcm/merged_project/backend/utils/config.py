"""Configuration constants."""

SUPPORTED_LANGUAGES = {
    "python": {"name": "Python", "ext": ".py"},
    "javascript": {"name": "JavaScript", "ext": ".js"},
    "typescript": {"name": "TypeScript", "ext": ".ts"},
    "java": {"name": "Java", "ext": ".java"},
    "cpp": {"name": "C++", "ext": ".cpp"},
    "csharp": {"name": "C#", "ext": ".cs"},
    "sql": {"name": "SQL", "ext": ".sql"},
    "go": {"name": "Go", "ext": ".go"},
    "rust": {"name": "Rust", "ext": ".rs"},
    "ruby": {"name": "Ruby", "ext": ".rb"},
    "php": {"name": "PHP", "ext": ".php"},
}

DIAGRAM_TYPES = [
    {"id": "flowchart", "name": "Flowchart", "description": "Process flows and decision trees"},
    {"id": "sequence", "name": "Sequence Diagram", "description": "Object interactions over time"},
    {"id": "erd", "name": "ER Diagram", "description": "Database entity relationships"},
    {"id": "class", "name": "Class Diagram", "description": "Object-oriented class structure"},
    {"id": "state", "name": "State Diagram", "description": "State transitions and workflows"},
    {"id": "architecture", "name": "Architecture", "description": "System architecture (C4)"},
]
