"""SQL parser using regex."""

import re
from typing import Dict, Any
from .base import BaseParser


class SQLParser(BaseParser):
    """Parser for SQL code."""
    
    def get_language(self) -> str:
        return "sql"
    
    def parse(self, code: str) -> Dict[str, Any]:
        tables = re.findall(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)', code, re.IGNORECASE)
        views = re.findall(r'CREATE\s+VIEW\s+(\w+)', code, re.IGNORECASE)
        indexes = re.findall(r'CREATE\s+INDEX\s+(\w+)', code, re.IGNORECASE)
        
        return {
            "language": "sql",
            "tables": [{"name": t} for t in tables],
            "views": [{"name": v} for v in views],
            "indexes": [{"name": i} for i in indexes],
            "line_count": len(code.splitlines())
        }
