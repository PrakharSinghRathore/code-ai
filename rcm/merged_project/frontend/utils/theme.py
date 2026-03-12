"""Theme configuration."""

DARK_THEME = """
<style>
    .main { background-color: #0e1117; }
    .stApp { background-color: #0e1117; }
    .title { font-size: 2.5rem !important; font-weight: bold !important; color: #ff4b4b !important; text-align: center; margin-bottom: 2rem !important; }
    .subtitle { text-align: center; color: #8b949e; margin-bottom: 2rem; }
    .success-box { padding: 1rem; background-color: rgba(46, 160, 67, 0.2); border-radius: 0.5rem; border: 1px solid #2ea043; }
    .error-box { padding: 1rem; background-color: rgba(248, 81, 73, 0.2); border-radius: 0.5rem; border: 1px solid #f85149; }
    .code-block { background-color: #161b22; padding: 1rem; border-radius: 0.5rem; font-family: 'Courier New', monospace; overflow-x: auto; }
    div.stButton > button:first-child { background-color: #ff4b4b; color: white; font-weight: bold; }
    .diagram-container { background-color: #161b22; padding: 1rem; border-radius: 0.5rem; min-height: 400px; }
    .metric-card { background-color: #161b22; padding: 1rem; border-radius: 0.5rem; text-align: center; }
    .metric-value { font-size: 2rem; font-weight: bold; color: #ff4b4b; }
    .metric-label { color: #8b949e; font-size: 0.9rem; }
    .tab-content { padding: 1rem; }
    .stTextArea textarea { background-color: #161b22; color: #e6edf3; }
    .sidebar-content { background-color: #161b22; }
</style>
"""

LIGHT_THEME = """
<style>
    .main { background-color: #ffffff; }
    .stApp { background-color: #ffffff; }
    .title { font-size: 2.5rem !important; font-weight: bold !important; color: #ff4b4b !important; text-align: center; margin-bottom: 2rem !important; }
    .subtitle { text-align: center; color: #656d76; margin-bottom: 2rem; }
    .success-box { padding: 1rem; background-color: rgba(46, 160, 67, 0.1); border-radius: 0.5rem; border: 1px solid #2ea043; }
    .error-box { padding: 1rem; background-color: rgba(248, 81, 73, 0.1); border-radius: 0.5rem; border: 1px solid #f85149; }
    .code-block { background-color: #f6f8fa; padding: 1rem; border-radius: 0.5rem; font-family: 'Courier New', monospace; overflow-x: auto; }
    div.stButton > button:first-child { background-color: #ff4b4b; color: white; font-weight: bold; }
    .diagram-container { background-color: #f6f8fa; padding: 1rem; border-radius: 0.5rem; min-height: 400px; }
    .metric-card { background-color: #f6f8fa; padding: 1rem; border-radius: 0.5rem; text-align: center; }
    .metric-value { font-size: 2rem; font-weight: bold; color: #ff4b4b; }
    .metric-label { color: #656d76; font-size: 0.9rem; }
    .tab-content { padding: 1rem; }
    .stTextArea textarea { background-color: #f6f8fa; color: #24292f; }
</style>
"""


def apply_theme(theme: str):
    """Apply the selected theme."""
    import streamlit as st
    if theme == 'dark':
        st.markdown(DARK_THEME, unsafe_allow_html=True)
    else:
        st.markdown(LIGHT_THEME, unsafe_allow_html=True)
