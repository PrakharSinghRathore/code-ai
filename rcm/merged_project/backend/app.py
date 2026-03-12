"""
RCM - Code Visualizer & Diagram Generator
Main Flask Application
"""

import os
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from parsers import get_parser
from services import (
    MetricsService,
    DependenciesService,
    DiagramService,
    FlowchartService,
)
from utils import get_languages, get_diagram_types, SUPPORTED_LANGUAGES

load_dotenv(Path(__file__).with_name(".env"))

app = Flask(__name__)
CORS(app)


@app.route("/api/parse", methods=["POST"])
def parse():
    """Parse code and return structure."""
    data = request.get_json(force=True)
    code = data.get("code", "")
    language = data.get("language", "python")
    
    if not code:
        return jsonify({"error": "Code is required"}), 400
    
    parser = get_parser(language)
    if not parser:
        return jsonify({"error": f"Language '{language}' parsing not implemented"}), 400
    
    result = parser.parse(code)
    return jsonify(result)


@app.route("/api/visualize", methods=["POST"])
def visualize():
    """Parse code and generate diagram."""
    data = request.get_json(force=True)
    code = data.get("code", "")
    language = data.get("language", "python")
    
    if not code:
        return jsonify({"error": "Code is required"}), 400
    
    parser = get_parser(language)
    if not parser:
        return jsonify({"error": f"Language '{language}' parsing not implemented"}), 400
    
    parsed = parser.parse(code)
    if parsed.get("error"):
        return jsonify(parsed), 400
    
    mermaid_code = DiagramService.generate_from_code(parsed, language)
    svg = DiagramService.render_to_svg(mermaid_code)
    
    return jsonify({
        "parsed": parsed,
        "mermaid_code": mermaid_code,
        "svg": svg
    })


@app.route("/api/metrics", methods=["POST"])
def metrics():
    """Get code metrics."""
    data = request.get_json(force=True)
    code = data.get("code", "")
    language = data.get("language", "python")
    
    result = MetricsService.compute(code, language)
    return jsonify(result)


@app.route("/api/dependencies", methods=["POST"])
def dependencies():
    """Get code dependencies."""
    data = request.get_json(force=True)
    code = data.get("code", "")
    language = data.get("language", "python")
    
    result = DependenciesService.extract(code, language)
    return jsonify(result)


@app.route("/api/flowchart", methods=["POST"])
def flowchart():
    """Generate flowchart from Python code."""
    data = request.get_json(force=True)
    code = data.get("code", "")
    
    result = FlowchartService.generate(code)
    return jsonify(result)


@app.route("/api/dryrun", methods=["POST"])
def dryrun():
    """Run all analysis on code."""
    data = request.get_json(force=True)
    code = data.get("code", "")
    language = data.get("language", "python")
    
    parser = get_parser(language)
    if not parser:
        return jsonify({"error": f"Language '{language}' parsing not implemented"}), 400
    
    parsed = parser.parse(code) if parser else {}
    metrics = MetricsService.compute(code, language)
    deps = DependenciesService.extract(code, language)
    flowchart = FlowchartService.generate(code) if language == "python" else {"flowchart": "flowchart TD\n    start[Start]"}
    
    return jsonify({
        "ast": parsed,
        "metrics": metrics,
        "dependencies": deps,
        "flowchart": flowchart,
    })


@app.route("/api/diagram-types", methods=["GET"])
def diagram_types():
    """Get list of available diagram types."""
    return jsonify({"types": get_diagram_types()})


@app.route("/api/generate", methods=["POST"])
def generate():
    """Generate diagram from prompt."""
    data = request.get_json(force=True)
    prompt = data.get("prompt", "")
    diagram_type = data.get("diagram_type", "flowchart")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    result = DiagramService.generate_from_text(prompt, diagram_type)

    if result.get("error"):
        return jsonify(result), 400

    mermaid_code = result["mermaid_code"]
    svg = result.get("svg")
    if not svg:
        svg = DiagramService.render_to_svg(mermaid_code)

    return jsonify({
        "mermaid_code": mermaid_code,
        "svg": svg,
        "diagram_type": diagram_type,
        "fallback": bool(result.get("fallback"))
    })


@app.route("/api/render", methods=["POST"])
def render():
    """Render Mermaid code to SVG."""
    import traceback
    data = request.get_json(force=True)
    mermaid_code = data.get("mermaid_code", "")

    if not mermaid_code:
        return jsonify({"error": "Mermaid code is required"}), 400

    try:
        svg = DiagramService.render_to_svg(mermaid_code)
        if not svg:
            # Return a placeholder or error message that frontend can handle
            return jsonify({
                "error": "Failed to render diagram from mermaid.ink",
                "mermaid_code": mermaid_code,
                "svg": None
            }), 200
        return jsonify({"svg": svg, "mermaid_code": mermaid_code})
    except Exception as e:
        print(f"Render error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            "error": str(e),
            "mermaid_code": mermaid_code,
            "svg": None
        }), 500


@app.route("/api/languages", methods=["GET"])
def languages():
    """Get supported languages."""
    return jsonify({"languages": get_languages()})


@app.route("/api/health", methods=["GET"])
def health():
    """Health check."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    return jsonify({
        "status": "ok",
        "ai_enabled": bool(api_key),
        "languages": len(SUPPORTED_LANGUAGES)
    })


@app.route("/")
def home():
    return jsonify({
        "name": "RCM - Code Visualizer & Diagram Generator API",
        "endpoints": {
            "POST /api/parse": "Parse code and return structure",
            "POST /api/visualize": "Parse code and generate diagram",
            "POST /api/metrics": "Get code metrics",
            "POST /api/dependencies": "Get code dependencies",
            "POST /api/flowchart": "Generate flowchart (Python)",
            "POST /api/dryrun": "Run all analysis",
            "POST /api/generate": "Generate diagram from prompt",
            "POST /api/render": "Render Mermaid to SVG",
            "GET /api/languages": "List supported languages",
            "GET /api/diagram-types": "List diagram types",
            "GET /api/health": "Health check"
        }
    })


if __name__ == "__main__":
    print("=" * 50)
    print("RCM - Code Visualizer & Diagram Generator")
    print("=" * 50)
    print(f"Supported Languages: {len(SUPPORTED_LANGUAGES)}")
    print("Server running on http://localhost:5000")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=True)
