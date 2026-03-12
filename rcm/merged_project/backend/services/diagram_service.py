"""Diagram generation service."""

import base64
import os
import re
import requests
from typing import Optional


class DiagramService:
    """Service for generating Mermaid diagrams."""
    
    SYSTEM_PROMPT = """You are an expert diagram generator. Your task is to convert natural language descriptions into valid Mermaid diagram code.

RULES:
1. Always output valid Mermaid syntax
2. Include proper diagram type declaration at the start
3. Use simple node shapes: [Box] for processes, ((Circle)) for start/end
4. Keep the diagram clean and readable
5. Do NOT use special shapes like [/text/] as they break parsing
6. Generate ONLY the Mermaid diagram code:"""
    
    DIAGRAM_TYPES = {
        "flowchart": "flowchart TD",
        "sequence": "sequenceDiagram",
        "erd": "erDiagram",
        "class": "classDiagram",
        "state": "stateDiagram-v2",
        "architecture": "flowchart TD",
    }
    
    @staticmethod
    def generate_from_code(parsed_code: dict, language: str) -> str:
        """Generate diagram from parsed code."""
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            return DiagramService._generate_fallback(parsed_code, language)
        
        summary = f"Language: {language}\nLine Count: {parsed_code.get('line_count', 0)}\n"
        
        if parsed_code.get("imports"):
            summary += "\nImports:\n"
            for imp in parsed_code["imports"][:10]:
                summary += f"  - {imp.get('name', 'unknown')}\n"
        
        if parsed_code.get("classes"):
            summary += "\nClasses:\n"
            for cls in parsed_code["classes"][:10]:
                methods = cls.get("methods", [])
                method_names = [m.get("name", "?") for m in methods[:5]]
                summary += f"  - {cls.get('name', '?')} has {', '.join(method_names)}\n"
        
        if parsed_code.get("functions"):
            summary += "\nFunctions:\n"
            for func in parsed_code["functions"][:10]:
                args = func.get("args", [])
                summary += f"  - {func.get('name', '?')}({', '.join(args)})\n"
        
        if parsed_code.get("tables"):
            summary += "\nDatabase Tables:\n"
            for table in parsed_code["tables"][:10]:
                summary += f"  - {table.get('name', '?')}\n"

        # Simpler prompt that won't generate problematic syntax
        prompt = f"""Generate a simple Mermaid flowchart showing this {language} code structure.

{summary}

Use ONLY these safe shapes:
- [Process Name] for rectangles
- ((Start)) and ((End)) for circles
- Use --> for arrows

Example:
flowchart TD
    start[Start]
    proc[Process Data]
    finish[End]
    start --> proc
    proc --> finish

Generate ONLY valid Mermaid code:"""

        try:
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/anomalyco/opencode",
                "X-Title": "Code Visualizer"
            }
            payload = {
                "model": os.getenv("OPENROUTER_MODEL", "openai/gpt-4o"),
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
                "max_tokens": 1500,
            }
            
            resp = requests.post(url, headers=headers, json=payload, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            
            return DiagramService._extract_and_sanitize(content)
        except Exception:
            return DiagramService._generate_fallback(parsed_code, language)
    
    @staticmethod
    def generate_from_text(prompt: str, diagram_type: str) -> dict:
        """Generate diagram from text description."""
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            return {"error": "OpenRouter API key not set. Add OPENROUTER_API_KEY to .env"}

        diagram_syntax = DiagramService.DIAGRAM_TYPES.get(diagram_type, "flowchart TD")

        full_prompt = f"""{DiagramService.SYSTEM_PROMPT}

User wants a {diagram_type} diagram.
Description: {prompt}

IMPORTANT: Use ONLY simple shapes:
- [Box] for rectangles
- ((Circle)) for circles
- NO parallelogram shapes like [/text/]

Generate the Mermaid {diagram_type} diagram code:"""

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/anomalyco/opencode",
            "X-Title": "AI Diagram Generator"
        }
        payload = {
            "model": os.getenv("OPENROUTER_MODEL", "openai/gpt-4o"),
            "messages": [{"role": "user", "content": full_prompt}],
            "temperature": 0.2,
            "max_tokens": 2000,
        }

        try:
            print(f"Calling OpenRouter API with model: {payload['model']}")
            resp = requests.post(url, headers=headers, json=payload, timeout=60)
            print(f"Response status: {resp.status_code}")
            if resp.status_code != 200:
                print(f"Response body: {resp.text[:500]}")
            resp.raise_for_status()
            data = resp.json()
            content = data["choices"][0]["message"]["content"]

            mermaid_code = DiagramService._extract_and_sanitize(content)
            if not mermaid_code:
                return {"error": "Failed to extract Mermaid code from response", "raw": content}

            svg = DiagramService.render_to_svg(mermaid_code)
            if not svg:
                fallback = DiagramService._generate_text_fallback(diagram_type, prompt)
                return {
                    "mermaid_code": fallback,
                    "svg": DiagramService.render_to_svg(fallback),
                    "error": None,
                    "fallback": True,
                }

            return {"mermaid_code": mermaid_code, "svg": svg, "error": None}
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            if e.response.status_code == 401:
                print(f"API Key invalid (401). Using fallback diagram.")
                fallback = DiagramService._generate_text_fallback(diagram_type, prompt)
                return {
                    "mermaid_code": fallback,
                    "svg": DiagramService.render_to_svg(fallback),
                    "error": None,
                    "fallback": True,
                }
            return {"error": f"API Error: {str(e)}"}
        except Exception as e:
            print(f"Diagram generation error: {str(e)}")
            fallback = DiagramService._generate_text_fallback(diagram_type, prompt)
            return {
                "mermaid_code": fallback,
                "svg": DiagramService.render_to_svg(fallback),
                "error": None,
                "fallback": True,
            }
    
    @staticmethod
    def render_to_svg(mermaid_code: str) -> Optional[str]:
        """Render Mermaid code to SVG."""
        if not mermaid_code:
            return None
        try:
            encoded = DiagramService._encode_for_mermaid_ink(mermaid_code)
            url = f"https://mermaid.ink/svg/{encoded}"
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200:
                svg_text = resp.text
                # Validate that it's actually SVG content
                if svg_text and '<svg' in svg_text:
                    return svg_text
        except Exception as e:
            print(f"SVG render error: {e}")
        return None

    @staticmethod
    def _encode_for_mermaid_ink(mermaid_code: str) -> str:
        """Encode Mermaid code for mermaid.ink using URL-safe base64 without padding."""
        encoded = base64.urlsafe_b64encode(mermaid_code.encode("utf-8")).decode("ascii")
        return encoded.rstrip("=")
    
    @staticmethod
    def _generate_text_fallback(diagram_type: str, prompt: str) -> str:
        """Generate a simple fallback diagram when AI fails."""
        # Use ONLY simple safe syntax
        diagram_starts = {
            "flowchart": """flowchart TD
    start[Start]
    process[Process]
    decision{Decision?}
    yes[Yes Action]
    no[No Action]
    finish[End]
    start --> process
    process --> decision
    decision -->|Yes| yes
    decision -->|No| no
    yes --> finish
    no --> finish""",
            "sequence": """sequenceDiagram
    participant User
    participant System
    User->>System: Request
    System-->>User: Response""",
            "erd": """erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ ITEM : contains
    USER {string name}
    ORDER {int id}""",
            "class": """classDiagram
    class User {
        +String name
        +login()
    }
    class Order {
        +int id
        +create()
    }
    User <-- Order""",
            "state": """stateDiagram-v2
    [*] --> Idle
    Idle --> Processing
    Processing --> Complete
    Complete --> [*]""",
            "architecture": """flowchart TD
    User((User)) --> Frontend[Frontend]
    Frontend --> Backend[Backend API]
    Backend --> DB[(Database)]
    Backend --> Cache[Cache]
    DB --> Backend
    Cache --> Backend
    Backend --> Frontend
    Frontend --> User"""
        }
        return diagram_starts.get(diagram_type, diagram_starts["flowchart"])

    @staticmethod
    def _generate_fallback(parsed_code: dict, language: str) -> str:
        """Generate fallback diagram without AI using ONLY safe Mermaid syntax."""
        lines = ["flowchart TD"]
        
        # Start node - use box shape [Text] instead of ((Circle))
        lines.append("    start[Start]")
        prev_node = "start"
        
        if parsed_code.get("imports"):
            for i, imp in enumerate(parsed_code.get("imports", [])[:5], 1):
                # Completely sanitize - remove any special chars
                name = imp.get("name", "?")
                name = re.sub(r'[^a-zA-Z0-9_]', '_', name.split('.')[-1])
                name = name[:20]  # Truncate long names
                lines.append(f"    imp{i}[Import {name}]")
                lines.append(f"    {prev_node} --> imp{i}")
                prev_node = f"imp{i}"
        
        if parsed_code.get("classes"):
            lines.append("    subgraph Classes")
            for i, cls in enumerate(parsed_code.get("classes", [])[:5], 1):
                name = cls.get("name", "?")
                name = re.sub(r'[^a-zA-Z0-9_]', '_', name)[:20]
                lines.append(f"    cls{i}[Class {name}]")
                methods = cls.get("methods", [])
                if methods:
                    method_names = [re.sub(r'[^a-zA-Z0-9_]', '_', m.get("name", "?"))[:15] for m in methods[:3]]
                    lines.append(f"    cls{i} --> m{i}[{', '.join(method_names)}]")
            lines.append("    end")
            lines.append(f"    {prev_node} --> cls1")
            prev_node = "cls1"
        
        if parsed_code.get("functions"):
            lines.append("    subgraph Functions")
            for i, func in enumerate(parsed_code.get("functions", [])[:5], 1):
                name = func.get("name", "?")
                name = re.sub(r'[^a-zA-Z0-9_]', '_', name)[:20]
                args = func.get("args", [])
                safe_args = [re.sub(r'[^a-zA-Z0-9_]', '_', str(a))[:10] for a in args]
                lines.append(f"    func{i}[{name}({', '.join(safe_args)})]")
            lines.append("    end")
            lines.append(f"    {prev_node} --> func1")
            prev_node = "func1"
        
        # End node
        lines.append("    finish[End]")
        if prev_node != "start":
            lines.append(f"    {prev_node} --> finish")
        else:
            lines.append("    start --> finish")
        
        return '\n'.join(lines)
    
    @staticmethod
    def _extract_and_sanitize(content: str) -> str:
        """Extract and sanitize Mermaid code from AI response."""
        lines = content.strip().split('\n')
        code_lines = []
        in_block = False
        
        for line in lines:
            if '```mermaid' in line:
                in_block = True
                continue
            elif '```' in line and in_block:
                break
            elif in_block:
                code_lines.append(line)
        
        if not code_lines:
            for line in lines:
                if line.strip().startswith(('flowchart', 'sequenceDiagram', 'graph', 'classDiagram', 'erDiagram', 'stateDiagram', 'C4')):
                    code_lines.append(line)
                elif code_lines and line.strip():
                    code_lines.append(line)
        
        mermaid_code = '\n'.join(code_lines).strip()
        
        # Comprehensive sanitization
        mermaid_code = DiagramService._sanitize_mermaid(mermaid_code)
        
        return mermaid_code
    
    @staticmethod
    def _sanitize_mermaid(code: str) -> str:
        """Sanitize Mermaid code to fix common AI generation issues."""
        if not code:
            return code
            
        lines = code.split('\n')
        sanitized = []
        
        for line in lines:
            # Remove any problematic parallelogram shapes [/text/] or [\text\]
            # Replace with safe box shape [text]
            line = re.sub(r'\[\s*/([^/]+)/\s*\]', r'[\1]', line)
            line = re.sub(r'\[\s*\\([^\\]+)\\\s*\]', r'[\1]', line)
            
            # Remove colons from node definitions that might break parsing
            # But keep colons in labels like A-->|label|B
            # Match node definitions: A[Label: sublabel] -> A[Label sublabel]
            line = re.sub(r'\[([^:\]]+):([^\]]+)\]', r'[\1 \2]', line)
            
            # Remove any remaining slashes in square brackets
            line = re.sub(r'\[[^\]]*/[^\]]*\]', lambda m: m.group(0).replace('/', '-').replace('\\', '-'), line)

            # Keep box labels conservative so mermaid.ink accepts fallback/code-generated diagrams.
            line = re.sub(
                r'\[([^\]]+)\]',
                lambda m: "[" + re.sub(r"[^a-zA-Z0-9 _-]", " ", m.group(1)).strip() + "]",
                line,
            )
            
            sanitized.append(line)
        
        result = '\n'.join(sanitized)
        
        # Final validation - if still contains problematic patterns, return safe fallback
        if '[/' in result or '/]' in result or '\\' in result:
            result = """flowchart TD
    start[Start]
    process[Process Data]
    finish[End]
    start --> process
    process --> finish"""
        
        return result
