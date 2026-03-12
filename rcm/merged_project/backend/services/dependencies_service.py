"""Dependencies extraction service."""

import re
import ast


class DependenciesService:
    """Service for extracting code dependencies/imports."""
    
    @staticmethod
    def extract(code: str, language: str) -> dict:
        """Extract import statements from code."""
        imports = []
        
        if language == "python":
            try:
                tree = ast.parse(code)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        module = node.module or ''
                        for alias in node.names:
                            imports.append(f"{module}.{alias.name}" if module else alias.name)
            except:
                pass
        elif language in ("javascript", "typescript"):
            imports = re.findall(r'import\s+(?:{[^}]+}|\w+)\s+from\s+[\'"]([^\'"]+)[\'"]', code)
            imports.extend(re.findall(r'require\([\'"]([^\'"]+)[\'"]\)', code))
        elif language == "java":
            imports = re.findall(r'import\s+([\w.]+);', code)
        elif language == "cpp":
            imports = re.findall(r'#include\s+[<"]([^>"]+)[>"]', code)
        elif language == "csharp":
            imports = re.findall(r'using\s+([\w.]+);', code)
        elif language == "go":
            import_list = []
            for imp in re.findall(r'import\s+\(([^)]+)\)', code, re.DOTALL):
                import_list.extend(re.findall(r'"([^"]+)"', imp))
            import_list.extend(re.findall(r'import\s+"([^"]+)"', code))
            imports = import_list
        elif language == "rust":
            imports = re.findall(r'use\s+([^;]+);', code)
        elif language == "ruby":
            imports = re.findall(r'require\s+["\']([^"\']+)["\']', code)
        elif language == "php":
            imports = re.findall(r'use\s+([^;]+);', code)
        else:
            imports = re.findall(r'import\s+["\']([^"\']+)["\']', code)
        
        return {"imports": imports}
