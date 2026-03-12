"""Python parser using AST."""

import ast
from typing import Dict, Any
from .base import BaseParser


class PythonParser(BaseParser):
    """Parser for Python code using AST."""
    
    def get_language(self) -> str:
        return "python"
    
    def parse(self, code: str) -> Dict[str, Any]:
        try:
            tree = ast.parse(code)
            
            imports = []
            functions = []
            classes = []
            variables = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append({"name": alias.name, "alias": alias.asname})
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    for alias in node.names:
                        imports.append({"name": f"{module}.{alias.name}", "alias": alias.asname})
                elif isinstance(node, ast.FunctionDef):
                    args = [arg.arg for arg in node.args.args]
                    functions.append({
                        "name": node.name,
                        "args": args,
                        "line": node.lineno,
                        "decorators": [d.id if isinstance(d, ast.Name) else str(d) for d in node.decorator_list]
                    })
                elif isinstance(node, ast.AsyncFunctionDef):
                    args = [arg.arg for arg in node.args.args]
                    functions.append({
                        "name": node.name,
                        "args": args,
                        "line": node.lineno,
                        "async": True
                    })
                elif isinstance(node, ast.ClassDef):
                    methods = []
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            methods.append({
                                "name": item.name,
                                "args": [arg.arg for arg in item.args.args]
                            })
                    classes.append({
                        "name": node.name,
                        "line": node.lineno,
                        "methods": methods
                    })
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            variables.append({"name": target.id, "line": node.lineno})
            
            return {
                "language": "python",
                "imports": imports,
                "functions": functions,
                "classes": classes,
                "variables": variables,
                "line_count": len(code.splitlines())
            }
        except SyntaxError as e:
            return {"error": f"Syntax Error: {e.msg} at line {e.lineno}"}
        except Exception as e:
            return {"error": str(e)}
