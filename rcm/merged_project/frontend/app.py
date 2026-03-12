"""
RCM - Code Visualizer & Diagram Generator
Main Streamlit Application
"""

import streamlit as st

from services import APIService
from utils import LANGUAGE_CONFIG, get_language_highlight, apply_theme, render_mermaid_diagram, download_svg_link, render_diagram_with_fallback


def _get_theme():
    """Safely get theme from session_state with a default."""
    try:
        return st.session_state.get("theme", "dark")
    except Exception:
        return "dark"


# Initialize theme before any other Streamlit commands
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

apply_theme(_get_theme())

st.set_page_config(
    page_title="Code Visualizer & Diagram Generator",
    page_icon="",
    layout="wide"
)


def render_code_visualizer():
    """Render the code visualizer tab."""
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Code Input")
        
        lang_options = {k: v["name"] for k, v in LANGUAGE_CONFIG.items()}
        
        selected_lang = st.selectbox(
            "Language",
            options=list(lang_options.keys()),
            format_func=lambda x: lang_options[x],
            index=0,
            key="code_lang"
        )
        
        default_code = '''def calculate_factorial(n):
    """Calculate factorial of a number."""
    if n <= 1:
        return 1
    return n * calculate_factorial(n - 1)

class MathOperations:
    def __init__(self, name):
        self.name = name
    
    def add(self, a, b):
        return a + b
    
    def multiply(self, a, b):
        return a * b

import math
import random
'''
        
        code_input = st.text_area(
            "Enter your code",
            height=300,
            value=default_code,
            key="code_input"
        )
        
        col_analyze1, col_analyze2 = st.columns(2)
        with col_analyze1:
            analyze_btn = st.button("Analyze", type="primary", key="analyze_btn")
        with col_analyze2:
            dryrun_btn = st.button("Full Analysis", key="dryrun_btn")
    
    with col2:
        st.markdown("### Analysis Results")
        
        if "analysis_results" not in st.session_state:
            st.session_state.analysis_results = None
        
        if analyze_btn and code_input:
            with st.spinner("Analyzing code..."):
                parsed = APIService.parse_code(code_input, selected_lang)
                metrics = APIService.get_metrics(code_input, selected_lang)
                deps = APIService.get_dependencies(code_input, selected_lang)
                
                st.session_state.analysis_results = {
                    "parsed": parsed,
                    "metrics": metrics,
                    "dependencies": deps
                }
        
        if dryrun_btn and code_input:
            with st.spinner("Running full analysis..."):
                try:
                    import requests
                    resp = requests.post(f"http://localhost:5000/api/dryrun", json={"code": code_input, "language": selected_lang}, timeout=60)
                    if resp.ok:
                        st.session_state.analysis_results = resp.json()
                except Exception as e:
                    st.error(f"Error: {e}")
        
        if st.session_state.analysis_results:
            results = st.session_state.analysis_results
            
            m = results.get("metrics", {})
            if m and not m.get("error"):
                mc1, mc2, mc3 = st.columns(3)
                with mc1:
                    st.markdown(f'<div class="metric-card"><div class="metric-value">{m.get("lines_of_code", 0)}</div><div class="metric-label">Lines of Code</div></div>', unsafe_allow_html=True)
                with mc2:
                    st.markdown(f'<div class="metric-card"><div class="metric-value">{m.get("functions", 0)}</div><div class="metric-label">Functions</div></div>', unsafe_allow_html=True)
                with mc3:
                    st.markdown(f'<div class="metric-card"><div class="metric-value">{m.get("classes", 0)}</div><div class="metric-label">Classes</div></div>', unsafe_allow_html=True)
            
            deps = results.get("dependencies", {})
            if deps and deps.get("imports"):
                with st.expander("Dependencies / Imports", expanded=True):
                    for imp in deps.get("imports", []):
                        st.code(imp, language=get_language_highlight(selected_lang))
            
            parsed = results.get("parsed", {})
            if parsed and not parsed.get("error"):
                if parsed.get("classes"):
                    with st.expander("Classes", expanded=True):
                        for cls in parsed.get("classes", []):
                            st.markdown(f"**{cls.get('name', '?')}**")
                            methods = cls.get("methods", [])
                            for m in methods:
                                st.markdown(f"  - `{m.get('name', '?')}({', '.join(m.get('args', []))})`")
                
                if parsed.get("functions"):
                    with st.expander("Functions", expanded=True):
                        for func in parsed.get("functions", []):
                            args = func.get("args", [])
                            st.markdown(f"- `{func.get('name', '?')}({', '.join(args)})`")
                
                if parsed.get("tables"):
                    with st.expander("Database Tables", expanded=True):
                        for t in parsed.get("tables", []):
                            st.markdown(f"- **{t.get('name', '?')}**")
            
            flowchart = results.get("flowchart", {})
            if flowchart and flowchart.get("flowchart"):
                with st.expander("Flowchart", expanded=True):
                    render_mermaid_diagram(flowchart["flowchart"], height=500, theme=_get_theme())
        
        st.markdown("### Code Diagram")
        
        if "diagram_code" not in st.session_state:
            st.session_state.diagram_code = None
        
        generate_diagram_btn = st.button("Generate Diagram", key="gen_diagram_btn")
        
        if generate_diagram_btn and code_input:
            with st.spinner("Generating diagram..."):
                result = APIService.visualize_code(code_input, selected_lang)
                if result.get("error"):
                    st.markdown(f'<div class="error-box">Error: {result["error"]}</div>', unsafe_allow_html=True)
                else:
                    mermaid_code = result.get("mermaid_code")
                    if not mermaid_code:
                        st.error("No mermaid code returned!")
                    elif not isinstance(mermaid_code, str):
                        st.error(f"mermaid_code is not a string: {type(mermaid_code)}")
                    else:
                        st.session_state.diagram_code = mermaid_code
        
        if st.session_state.diagram_code:
            svg = APIService.render_mermaid(st.session_state.diagram_code)
            
            # Render diagram
            st.markdown('<div class="diagram-preview-container">', unsafe_allow_html=True)
            diagram_code = st.session_state.diagram_code or ""
            render_diagram_with_fallback(diagram_code, svg, height=500, theme=_get_theme())
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Export section
            st.markdown("---")
            col_export1, col_export2 = st.columns([1, 2])
            with col_export1:
                st.markdown(download_svg_link(diagram_code, "code_diagram.svg"), unsafe_allow_html=True)
            with col_export2:
                st.markdown("**Source Code**")
                with st.expander("View Mermaid Code"):
                    st.code(diagram_code, language="mermaid")


def render_diagram_generator():
    """Render the AI diagram generator tab."""
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Create Your Diagram")
        
        diagram_types = APIService.get_diagram_types()
        type_options = {t.get("id", ""): t.get("name", "") for t in diagram_types}
        
        selected_type = st.selectbox(
            "Diagram Type",
            options=list(type_options.keys()),
            format_func=lambda x: type_options[x],
            index=0,
            key="diagram_type"
        )
        
        with st.expander("Diagram Type Info"):
            for t in diagram_types:
                if t.get("id") == selected_type:
                    st.write(t.get("description", ""))
        
        prompt = st.text_area(
            "Describe your diagram",
            height=150,
            placeholder="Example: User logs in, views dashboard, creates new project",
            key="diagram_prompt"
        )
        
        examples = {
            "flowchart": ["User registration flow", "E-commerce checkout", "Password reset"],
            "sequence": ["User login flow", "API request", "Bank transfer"],
            "erd": ["E-commerce database", "Social media schema", "Library system"],
            "class": ["Vehicle hierarchy", "Banking system", "Shape classes"],
            "state": ["Order fulfillment", "User lifecycle", "Document workflow"],
            "architecture": ["Three-tier app", "Microservices", "AWS infrastructure"]
        }
        
        st.markdown("#### Quick Examples")
        for ex in examples.get(selected_type, []):
            if st.button(ex, key=f"ex_{ex}"):
                st.session_state.example_prompt = ex
        
        if "example_prompt" in st.session_state:
            prompt = st.session_state.get("example_prompt", prompt)
        
        generate_btn = st.button("Generate Diagram", type="primary", key="gen_btn")

    with col2:
        st.markdown("### Diagram Preview")
        
        if "mermaid_code" not in st.session_state:
            st.session_state.mermaid_code = None
        if "svg_content" not in st.session_state:
            st.session_state.svg_content = None
        if "ai_used_fallback" not in st.session_state:
            st.session_state.ai_used_fallback = False
        
        if generate_btn and prompt:
            with st.spinner("Generating diagram..."):
                result = APIService.generate_diagram(prompt, selected_type)
                
                if result.get("error"):
                    st.markdown(f'<div class="error-box">Error: {result["error"]}</div>', unsafe_allow_html=True)
                else:
                    st.session_state.mermaid_code = result.get("mermaid_code", "")
                    st.session_state.svg_content = result.get("svg")
                    st.session_state.ai_used_fallback = bool(result.get("fallback"))
                    st.success("Diagram generated successfully!")
        
        if st.session_state.get("mermaid_code"):
            # Render diagram in the preview area
            st.markdown('<div class="diagram-preview-container">', unsafe_allow_html=True)
            svg = st.session_state.get("svg_content")
            mermaid_code = st.session_state.mermaid_code or ""
            render_diagram_with_fallback(mermaid_code, svg, height=500, theme=_get_theme())
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Export section below the diagram
            st.markdown("---")
            col_export1, col_export2 = st.columns([1, 2])
            with col_export1:
                st.markdown(download_svg_link(st.session_state.mermaid_code, "diagram.svg"), unsafe_allow_html=True)
            with col_export2:
                st.markdown(f"**Type:** {st.session_state.get('diagram_type', 'Unknown').title()}")
                if st.session_state.get("ai_used_fallback"):
                    st.caption("Using safe fallback output for this prompt.")
        else:
            st.markdown("""
            <div style="display: flex; align-items: center; justify-content: center; height: 300px; color: #8b949e; border: 2px dashed #30363d; border-radius: 8px;">
                <div style="text-align: center;">
                    <p>Enter a description and click Generate</p>
                </div>
            </div>
            """, unsafe_allow_html=True)


st.markdown('<p class="title">RCM - Code Visualizer & Diagram Generator</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Analyze code structure and generate diagrams using AI</p>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Code Visualizer", "AI Diagram Generator"])

with tab1:
    render_code_visualizer()

with tab2:
    render_diagram_generator()

if st.session_state.get("mermaid_code"):
    st.markdown("---")
    with st.expander("View Mermaid Source Code"):
        st.code(st.session_state.mermaid_code, language="mermaid")

with st.sidebar:
    st.markdown("### Theme")
    theme_col1, theme_col2 = st.columns(2)
    with theme_col1:
        if st.button("Dark"):
            st.session_state.theme = 'dark'
            st.rerun()
    with theme_col2:
        if st.button("Light"):
            st.session_state.theme = 'light'
            st.rerun()
    
    st.markdown("### Configuration")
    
    health = APIService.health_check()
    if health:
        if health.get("ai_enabled"):
            st.success("API Connected - AI Enabled")
        else:
            st.warning("API key not configured")
        st.markdown(f"**Languages:** {health.get('languages', 0)}")
    else:
        st.error("Backend not running")
    
    st.markdown("### About")
    st.info("""
    - **Code Visualizer**: Parse code structure
    - **AI Diagram Generator**: Text to diagrams
    
    Set `OPENROUTER_API_KEY` in `.env` for AI.
    """)
