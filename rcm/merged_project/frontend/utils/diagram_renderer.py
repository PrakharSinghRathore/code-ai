"""Diagram rendering utilities."""

import base64
from typing import Optional


def render_mermaid_diagram(mermaid_code: str, height: int = 600, theme: str = "dark") -> None:
    """Render a Mermaid diagram using a plain image URL."""
    if not mermaid_code:
        return

    import streamlit as st

    st.image(_get_mermaid_ink_url(mermaid_code), use_container_width=True)


def download_svg_link(mermaid_code: Optional[str], filename: str = "diagram.svg") -> str:
    """Generate a download link for the diagram as SVG using mermaid.ink API."""
    if not mermaid_code:
        return ""
    
    try:
        encoded = _encode_for_mermaid_ink(mermaid_code)
        svg_url = f"https://mermaid.ink/svg/{encoded}"
        
        href = f'''<a href="{svg_url}" target="_blank" download="{filename}" 
                    style="padding: 0.5rem 1rem; background-color: #ff4b4b; color: white; 
                           text-decoration: none; border-radius: 0.5rem; font-weight: bold;
                           display: inline-block; margin-top: 10px;">
                    Download SVG
                 </a>'''
        return href
    except Exception:
        return ""


def render_diagram_with_fallback(mermaid_code: str, svg_content: Optional[str] = None, height: int = 600, theme: str = "dark") -> None:
    """Render diagram with fallback handling."""
    import streamlit as st
    
    if svg_content and len(svg_content) > 100:
        render_svg_diagram(svg_content, height=height, theme=theme)
    elif mermaid_code:
        render_mermaid_diagram(mermaid_code, height=height, theme=theme)
    else:
        st.warning("No diagram code available")


def render_svg_diagram(svg_content: str, height: int = 600, theme: str = "dark") -> None:
    """Render backend-generated SVG as a plain image data URL."""
    import streamlit as st

    if svg_content:
        st.image(_svg_to_data_url(svg_content), use_container_width=True)


def _encode_for_mermaid_ink(mermaid_code: str) -> str:
    """Encode Mermaid code for mermaid.ink using URL-safe base64 without padding."""
    encoded = base64.urlsafe_b64encode(mermaid_code.encode("utf-8")).decode("ascii")
    return encoded.rstrip("=")


def _get_mermaid_ink_url(mermaid_code: str) -> str:
    """Build the mermaid.ink SVG URL for a Mermaid source string."""
    return f"https://mermaid.ink/svg/{_encode_for_mermaid_ink(mermaid_code)}"


def _svg_to_data_url(svg_content: str) -> str:
    """Encode SVG text as a data URL for Streamlit image rendering."""
    encoded = base64.b64encode(svg_content.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"
