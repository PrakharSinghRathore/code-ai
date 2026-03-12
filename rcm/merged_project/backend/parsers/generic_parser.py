"""Generic regex-based parser for multiple languages."""

import re
from typing import Dict, Any, List, Tuple
from .base import BaseParser


class GenericParser(BaseParser):
    """Generic parser using regex patterns for various languages."""
    
    def __init__(self, language: str, patterns: Dict[str, List[str]]):
        self.language = language
        self.patterns = patterns
    
    def get_language(self) -> str:
        return self.language
    
    def parse(self, code: str) -> Dict[str, Any]:
        result = {"language": self.language, "line_count": len(code.splitlines())}
        
        for key, pattern_list in self.patterns.items():
            matches = []
            for pattern in pattern_list:
                found = re.findall(pattern, code, re.MULTILINE)
                matches.extend(found)
            
            if matches:
                if all(isinstance(m, str) for m in matches):
                    result[key] = [{"name": m} for m in matches]
                else:
                    result[key] = matches
        
        return result


def create_java_parser() -> GenericParser:
    return GenericParser("java", {
        "packages": [r'package\s+([\w.]+);'],
        "imports": [r'import\s+([\w.]+);'],
        "classes": [r'(?:public\s+)?class\s+(\w+)'],
        "interfaces": [r'interface\s+(\w+)'],
        "methods": [r'(?:public|private|protected)?\s*(?:\w+)\s+(\w+)\s*\([^)]*\)'],
    })


def create_cpp_parser() -> GenericParser:
    return GenericParser("cpp", {
        "includes": [r'#include\s+[<"]([^>"]+)[>"]'],
        "classes": [r'class\s+(\w+)'],
        "structs": [r'struct\s+(\w+)'],
        "functions": [r'(?:void|int|bool|float|double|string|auto)\s+(\w+)\s*\([^)]*\)'],
    })


def create_csharp_parser() -> GenericParser:
    return GenericParser("csharp", {
        "namespaces": [r'namespace\s+([\w.]+)'],
        "imports": [r'using\s+([\w.]+);'],
        "classes": [r'(?:public|private|internal)?\s*class\s+(\w+)'],
        "interfaces": [r'interface\s+(\w+)'],
        "methods": [r'(?:public|private|protected)?\s*(?:async\s*)?(?:\w+)\s+(\w+)\s*\([^)]*\)'],
    })


def create_go_parser() -> GenericParser:
    return GenericParser("go", {
        "packages": [r'package\s+(\w+)'],
        "imports": [r'import\s+"([^"]+)"'],
        "functions": [r'func\s+(?:\(\w+\s+\*?\w+\)\s+)?(\w+)\s*\('],
        "structs": [r'type\s+(\w+)\s+struct'],
        "interfaces": [r'type\s+(\w+)\s+interface'],
    })


def create_rust_parser() -> GenericParser:
    return GenericParser("rust", {
        "imports": [r'use\s+([^;]+);'],
        "structs": [r'struct\s+(\w+)'],
        "impls": [r'impl\s+(?:<[^>]+>\s+)?(\w+)'],
        "functions": [r'fn\s+(\w+)'],
        "enums": [r'enum\s+(\w+)'],
        "traits": [r'trait\s+(\w+)'],
    })


def create_ruby_parser() -> GenericParser:
    return GenericParser("ruby", {
        "requires": [r'require\s+["\']([^"\']+)["\']'],
        "includes": [r'include\s+(\w+)'],
        "classes": [r'class\s+(\w+)'],
        "modules": [r'module\s+(\w+)'],
        "methods": [r'def\s+(?:self\.)?(\w+)'],
    })


def create_php_parser() -> GenericParser:
    return GenericParser("php", {
        "namespaces": [r'namespace\s+([\w\\]+)'],
        "uses": [r'use\s+([^;]+);'],
        "classes": [r'(?:class|interface|trait)\s+(\w+)'],
        "functions": [r'function\s+(\w+)'],
        "methods": [r'(?:public|private|protected)?\s*function\s+(\w+)'],
    })
