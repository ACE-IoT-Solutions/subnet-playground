"""
ACE IoT Solutions Brand Styling
Shared CSS and branding utilities for consistent visual identity
"""

# ACE IoT Brand Colors
ACE_LIME = "#c0d201"
ACE_DARK = "#2b2b2b"
ACE_GRAY = "#5a5a5a"
ACE_LIGHT_GRAY = "#f5f5f5"
ACE_WHITE = "#ffffff"

def get_ace_brand_css() -> str:
    """Returns the ACE IoT branded CSS for Streamlit apps"""
    return """
<style>
    /* ACE IoT Brand Colors */
    :root {
        --ace-lime: #c0d201;
        --ace-dark: #2b2b2b;
        --ace-gray: #5a5a5a;
        --ace-light-gray: #f5f5f5;
    }

    /* Headers */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: var(--ace-dark);
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: var(--ace-gray);
        margin-bottom: 1rem;
    }
    .ace-brand {
        color: var(--ace-lime);
        font-weight: bold;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }

    /* Content Boxes */
    .feature-box {
        background-color: var(--ace-light-gray);
        color: var(--ace-dark);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid var(--ace-lime);
        margin: 1rem 0;
    }
    .feature-box h3, .feature-box h4 {
        color: var(--ace-dark);
    }

    .protocol-box {
        background: linear-gradient(135deg, var(--ace-dark) 0%, var(--ace-gray) 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-top: 4px solid var(--ace-lime);
    }
    .protocol-box h3 {
        color: var(--ace-lime);
    }

    .device-card {
        background-color: var(--ace-light-gray);
        color: var(--ace-dark);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid var(--ace-lime);
        margin: 1rem 0;
    }

    .message-flow {
        background-color: var(--ace-light-gray);
        color: var(--ace-dark);
        padding: 1rem;
        border-radius: 8px;
        font-family: monospace;
        margin: 0.5rem 0;
        border-left: 3px solid var(--ace-lime);
    }

    .highlight-box {
        background-color: #FFF4CC;
        color: var(--ace-dark);
        padding: 1.5rem;
        border-radius: 8px;
        border: 2px solid var(--ace-lime);
        margin: 1rem 0;
    }

    .metric-box {
        background-color: var(--ace-light-gray);
        color: var(--ace-dark);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid var(--ace-lime);
        margin: 0.5rem 0;
    }

    .safe-box {
        background-color: #E8F8F5;
        color: var(--ace-dark);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid var(--ace-lime);
    }

    .storm-warning {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* Buttons */
    .stButton>button {
        background-color: var(--ace-lime) !important;
        color: var(--ace-dark) !important;
        border: none !important;
        font-weight: bold !important;
    }
    .stButton>button:hover {
        background-color: #a8b801 !important;
        color: var(--ace-dark) !important;
    }

    /* Radio buttons */
    .stRadio > label {
        color: var(--ace-dark);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] button {
        color: var(--ace-gray);
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: var(--ace-lime);
        border-bottom-color: var(--ace-lime);
    }

    /* Sidebar */
    .css-1d391kg {
        background-color: var(--ace-light-gray);
    }

    /* Key takeaways */
    div[style*="background-color: #FFF4CC"] {
        border-left: 4px solid var(--ace-lime) !important;
    }
</style>
"""

def get_ace_footer() -> str:
    """Returns ACE IoT branded footer HTML"""
    return """
<div style="text-align: center; margin-top: 3rem; padding: 2rem; border-top: 2px solid #c0d201; color: #5a5a5a;">
    <strong style="color: #c0d201;">ACE IoT Solutions</strong><br>
    Building Automation • IoT Integration • BACnet Expertise<br>
    <a href="https://aceiotsolutions.com" target="_blank" style="color: #c0d201; text-decoration: none;">aceiotsolutions.com</a>
</div>
"""
