"""Base AST Parser class."""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Optional, cast
from dataclasses import dataclass, field
from enum import Enum


class NodeType(str, Enum):
    """Node types for AST."""
    FUNCTION = "function"
    CLASS = "class"
    VARIABLE = "variable"
    IMPORT = "import"
    CONDITIONAL = "conditional"
    LOOP = "loop"
    EXPRESSION = "expression"
    STATEMENT = "statement"
    DECORATOR = "decorator"
    PARAMETER = "parameter"
    RETURN = "return"
    ASYNC_FUNCTION = "async_function"
    INTERFACE = "interface"
    ENUM = "enum"
    TYPE_ALIAS = "type_alias"


@dataclass
class ASTNode:
    """Base AST Node representation."""
    type: NodeType
    name: str
    line_start: int
    line_end: int
    column_start: int
    column_end: int
    parent: Optional[ASTNode] = None
    # Use factories to avoid mutable defaults and to satisfy static type checkers.
    children: list[ASTNode] = field(  # type: ignore[assignment]
        default_factory=lambda: cast(list[ASTNode], [])
    )
    metadata: dict[str, Any] = field(  # type: ignore[assignment]
        default_factory=lambda: cast(dict[str, Any], {})
    )
    
    def to_dict(self) -> dict[str, Any]:
        """Convert node to dictionary."""
        return {
            'type': self.type.value,
            'name': self.name,
            'line_start': self.line_start,
            'line_end': self.line_end,
            'column_start': self.column_start,
            'column_end': self.column_end,
            'children': [child.to_dict() for child in self.children],
            'metadata': self.metadata,
        }


class BaseASTParser(ABC):
    """Base parser for all languages."""
    
    def __init__(self, language: str):
        self.language = language
        self.root: Optional[ASTNode] = None
        self.source_code = ""
        self.lines: list[str] = []
    
    @abstractmethod
    def parse(self, source_code: str) -> ASTNode:
        """Parse source code and return AST."""
        pass
    
    @abstractmethod
    def _build_tree(self) -> ASTNode:
        """Build AST tree from parsed structure."""
        pass
    
    def get_tree_dict(self) -> dict[str, Any]:
        """Get AST as dictionary."""
        if self.root is None:
            return {}
        return self.root.to_dict()
    
    def find_node_by_position(self, line: int, column: int) -> Optional[ASTNode]:
        """Find AST node at given position."""
        def search(node: ASTNode) -> Optional[ASTNode]:
            if (node.line_start <= line <= node.line_end and
                node.column_start <= column <= node.column_end):
                for child in node.children:
                    result = search(child)
                    if result:
                        return result
                return node
            return None
        
        if self.root:
            return search(self.root)
        return None
    
    def get_node_scope(self, node: ASTNode) -> dict[str, Any]:
        """Get scope information for a node."""
        return {
            'node': node.name,
            'type': node.type.value,
            'line_range': (node.line_start, node.line_end),
            'metadata': node.metadata,
        }
