"""Metrics calculation service."""

import re
import ast


class MetricsService:
    """Service for calculating code metrics."""
    
    @staticmethod
    def compute(code: str, language: str) -> dict:
        """Calculate code metrics."""
        lines = code.splitlines()
        loc = len(lines)
        
        if language == "python":
            try:
                tree = ast.parse(code)
                func_cnt = sum(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) for node in ast.walk(tree))
                class_cnt = sum(isinstance(node, ast.ClassDef) for node in ast.walk(tree))
            except:
                func_cnt = class_cnt = 0
        elif language in ("javascript", "typescript"):
            func_cnt = len(re.findall(r'(?:function\s+\w+|const\s+\w+\s*=\s*(?:async\s*)?\(|=>)', code))
            class_cnt = len(re.findall(r'class\s+\w+', code))
        elif language in ("java", "cpp", "csharp"):
            func_cnt = len(re.findall(r'(?:public|private|protected)?\s*(?:\w+)\s+\w+\s*\([^)]*\)', code))
            class_cnt = len(re.findall(r'(?:class|struct|interface)\s+\w+', code))
        elif language == "go":
            func_cnt = len(re.findall(r'func\s+', code))
            class_cnt = len(re.findall(r'type\s+\w+\s+struct', code))
        elif language == "rust":
            func_cnt = len(re.findall(r'fn\s+', code))
            class_cnt = len(re.findall(r'(?:struct|enum|trait)\s+', code))
        elif language == "ruby":
            func_cnt = len(re.findall(r'def\s+', code))
            class_cnt = len(re.findall(r'class\s+', code))
        elif language == "php":
            func_cnt = len(re.findall(r'function\s+', code))
            class_cnt = len(re.findall(r'(?:class|interface|trait)\s+', code))
        else:
            func_cnt = len(re.findall(r'def\s+\w+|function\s+\w+', code))
            class_cnt = len(re.findall(r'class\s+\w+', code))
        
        return {"lines_of_code": loc, "functions": func_cnt, "classes": class_cnt}
