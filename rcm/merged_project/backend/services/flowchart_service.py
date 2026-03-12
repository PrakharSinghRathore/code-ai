"""Flowchart generation service for Python code."""

import ast


class FlowchartService:
    """Service for generating flowcharts from Python code."""
    
    @staticmethod
    def generate(code: str) -> dict:
        """Generate flowchart from Python code."""
        try:
            tree = ast.parse(code)
        except Exception as e:
            return {'error': f'Parse error: {e}'}
        
        lines = ['flowchart TD']
        node_id = 0
        
        def next_id():
            nonlocal node_id
            node_id += 1
            return f'N{node_id}'
        
        prev = None
        for node in tree.body:
            nid = next_id()
            if isinstance(node, ast.FunctionDef):
                label = f'Function {node.name}'
            elif isinstance(node, ast.If):
                label = 'If condition'
            elif isinstance(node, ast.For):
                label = 'For loop'
            elif isinstance(node, ast.While):
                label = 'While loop'
            elif isinstance(node, ast.ClassDef):
                label = f'Class {node.name}'
            else:
                label = type(node).__name__
            
            lines.append(f'    {nid}[{label}]')
            if prev:
                lines.append(f'    {prev} --> {nid}')
            prev = nid
        
        return {'flowchart': '\n'.join(lines)}
