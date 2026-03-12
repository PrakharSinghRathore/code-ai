"""JavaScript/TypeScript parser using regex."""

import re
from typing import Dict, Any
from .base import BaseParser


class JavaScriptParser(BaseParser):
    """Parser for JavaScript and TypeScript code."""
    
    def get_language(self) -> str:
        return "javascript"
    
    def parse(self, code: str) -> Dict[str, Any]:
        imports = re.findall(r'import\s+(?:{[^}]+}|\w+)\s+from\s+[\'"]([^\'"]+)[\'"]', code)
        requires = re.findall(r'require\([\'"]([^\'"]+)[\'"]\)', code)
        
        functions = re.findall(
            r'(?:function\s+(\w+)|const\s+(\w+)\s*=\s*(?:async\s*)?\(.*?\)\s*=>|(\w+)\s*:\s*(?:async\s*)?\(.*?\)\s*=>)',
            code
        )
        functions = [f[0] or f[1] or f[2] for f in functions if any(f)]
        
        classes = re.findall(r'class\s+(\w+)(?:\s+extends\s+(\w+))?', code)
        classes = [{"name": c[0], "extends": c[1]} for c in classes]
        
        interfaces = re.findall(r'interface\s+(\w+)', code)
        
        return {
            "language": "javascript",
            "imports": [{"name": i} for i in imports + requires],
            "functions": [{"name": f} for f in functions],
            "classes": classes,
            "interfaces": [{"name": i} for i in interfaces],
            "line_count": len(code.splitlines())
        }
