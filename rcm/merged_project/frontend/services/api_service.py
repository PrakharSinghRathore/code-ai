"""API client service."""

import requests

API_URL = "http://localhost:5000/api"


class APIService:
    """Service for making API calls to backend."""
    
    @staticmethod
    def get_languages():
        try:
            resp = requests.get(f"{API_URL}/languages", timeout=10)
            if resp.ok:
                return resp.json().get("languages", [])
        except:
            pass
        return [
            {"id": "python", "name": "Python"},
            {"id": "javascript", "name": "JavaScript"},
            {"id": "typescript", "name": "TypeScript"},
            {"id": "java", "name": "Java"},
            {"id": "cpp", "name": "C++"},
            {"id": "csharp", "name": "C#"},
            {"id": "go", "name": "Go"},
            {"id": "rust", "name": "Rust"},
            {"id": "ruby", "name": "Ruby"},
            {"id": "php", "name": "PHP"},
            {"id": "sql", "name": "SQL"},
        ]
    
    @staticmethod
    def get_diagram_types():
        try:
            resp = requests.get(f"{API_URL}/diagram-types", timeout=10)
            if resp.ok:
                return resp.json().get("types", [])
        except:
            pass
        return [
            {"id": "flowchart", "name": "Flowchart"},
            {"id": "sequence", "name": "Sequence Diagram"},
            {"id": "erd", "name": "ER Diagram"},
            {"id": "class", "name": "Class Diagram"},
            {"id": "state", "name": "State Diagram"},
            {"id": "architecture", "name": "Architecture"},
        ]
    
    @staticmethod
    def parse_code(code: str, language: str):
        try:
            resp = requests.post(f"{API_URL}/parse", json={"code": code, "language": language}, timeout=30)
            if resp.ok:
                return resp.json()
            return {"error": resp.text}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def get_metrics(code: str, language: str):
        try:
            resp = requests.post(f"{API_URL}/metrics", json={"code": code, "language": language}, timeout=30)
            if resp.ok:
                return resp.json()
            return {"error": resp.text}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def get_dependencies(code: str, language: str):
        try:
            resp = requests.post(f"{API_URL}/dependencies", json={"code": code, "language": language}, timeout=30)
            if resp.ok:
                return resp.json()
            return {"error": resp.text}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def get_flowchart(code: str):
        try:
            resp = requests.post(f"{API_URL}/flowchart", json={"code": code}, timeout=30)
            if resp.ok:
                return resp.json()
            return {"error": resp.text}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def visualize_code(code: str, language: str):
        try:
            resp = requests.post(f"{API_URL}/visualize", json={"code": code, "language": language}, timeout=60)
            if resp.ok:
                return resp.json()
            return {"error": resp.text}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def generate_diagram(prompt: str, diagram_type: str):
        try:
            resp = requests.post(f"{API_URL}/generate", json={"prompt": prompt, "diagram_type": diagram_type}, timeout=60)
            if resp.ok:
                return resp.json()
            return {"error": resp.text}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def render_mermaid(mermaid_code: str):
        try:
            resp = requests.post(f"{API_URL}/render", json={"mermaid_code": mermaid_code}, timeout=30)
            if resp.ok:
                return resp.json().get("svg")
        except:
            pass
        return None
    
    @staticmethod
    def health_check():
        try:
            resp = requests.get(f"{API_URL}/health", timeout=5)
            if resp.ok:
                return resp.json()
        except:
            pass
        return None
