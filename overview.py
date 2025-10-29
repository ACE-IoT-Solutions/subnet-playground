"""
BACnet Subnet & BBMD Educational Academy
Main Streamlit Application

Interactive educational tool for learning subnet architecture,
BACnet protocol concepts, and BBMD broadcast management.
"""

import streamlit as st
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from ace_subnet_playground.branding import get_ace_brand_css, get_ace_footer

# Page configuration
st.set_page_config(
    page_title="Overview | BACnet Academy",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply ACE IoT Solutions Brand
st.markdown(get_ace_brand_css(), unsafe_allow_html=True)
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        text-align: center;
    }
    .sub-header {
        font-size: 1.5rem;
        text-align: center;
    }
    .ace-brand {
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .module-card {
        background: linear-gradient(135deg, #2b2b2b 0%, #5a5a5a 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-top: 4px solid var(--ace-lime);
    }
    .module-card h3 {
        color: var(--ace-lime);
        margin-top: 0;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<div class="main-header">🌐 BACnet Subnet & BBMD Academy</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Master Subnet Architecture and BACnet Broadcast Management</div>', unsafe_allow_html=True)
st.markdown('<div class="ace-brand">Powered by ACE IoT Solutions</div>', unsafe_allow_html=True)

# Welcome section
st.markdown("---")
st.markdown("## Welcome to Your Interactive Learning Journey")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-box">
        <h3>📚 Interactive Learning</h3>
        <p>Hands-on demonstrations and real-time visualizations help you understand complex networking concepts.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <h3>🔬 Live Simulations</h3>
        <p>Experiment with subnet configurations, broadcast propagation, and BBMD routing in a safe environment.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-box">
        <h3>🎯 BACnet Focus</h3>
        <p>Learn subnet concepts specifically applied to BACnet/IP networks and building automation systems.</p>
    </div>
    """, unsafe_allow_html=True)

# Learning modules
st.markdown("---")
st.markdown("## 📖 Learning Modules")

st.info("👈 **Select a module from the sidebar to begin your learning journey**")

# Module overview
modules = [
    {
        "title": "0. Subnet Introduction",
        "icon": "🍽️",
        "page": "pages/0_Subnet_Introduction.py",
        "description": "Learn subnet concepts through an intuitive restaurant/table analogy.",
        "topics": ["Restaurant table analogy", "Hub-and-spoke patterns", "Broadcast as 'toast to table'", "BACnet broadcast context"]
    },
    {
        "title": "1. Subnet Basics",
        "icon": "🔢",
        "page": "pages/1_Subnet_Basics.py",
        "description": "Master subnet mask calculations, CIDR notation, and network/host bit concepts.",
        "topics": ["IP addressing fundamentals", "Enhanced network class detection", "Binary representation", "CIDR notation", "Boundary validation"]
    },
    {
        "title": "2. Binary Operations",
        "icon": "⚙️",
        "page": "pages/2_Binary_Operations.py",
        "description": "Understand bitwise AND operations and how devices process packets.",
        "topics": ["Bitwise AND tutorial", "Packet processing logic", "Subnet membership decisions", "Interactive calculators"]
    },
    {
        "title": "3. BACnet Overview",
        "icon": "🏢",
        "page": "pages/3_BACnet_Overview.py",
        "description": "Introduction to BACnet protocol, device discovery, and network architecture.",
        "topics": ["BACnet/IP protocol basics", "Who-Is/I-Am discovery", "Network numbers", "Device addressing"]
    },
    {
        "title": "4. BBMD Architecture",
        "icon": "🌉",
        "page": "pages/4_BBMD_Architecture.py",
        "description": "Learn how BBMDs enable BACnet communication across subnet boundaries.",
        "topics": ["BBMD functionality", "Broadcast Distribution Table (BDT)", "Foreign Device Table (FDT)", "Split horizon pattern", "Full mesh vs hub-spoke"]
    },
    {
        "title": "5. Broadcast Storms",
        "icon": "⚡",
        "page": "pages/5_Broadcast_Storms.py",
        "description": "Visualize broadcast storm propagation and learn mitigation strategies.",
        "topics": ["Storm causes and effects", "Interactive topology builder", "Split horizon architecture", "Detection and prevention", "Full mesh analysis"]
    },
    {
        "title": "6. Network Scenarios",
        "icon": "🗺️",
        "page": "pages/6_Network_Scenarios.py",
        "description": "Explore real-world BACnet network scenarios and troubleshooting.",
        "topics": ["Multi-subnet BACnet networks", "NAT challenges", "Edge device solutions", "Best practices"]
    }
]

for i, module in enumerate(modules):
    if i % 2 == 0:
        cols = st.columns(2)

    with cols[i % 2]:
        st.markdown(f"""
        <div class="module-card">
            <h3>{module['icon']} {module['title']}</h3>
            <p>{module['description']}</p>
            <ul>
                {''.join([f'<li>{topic}</li>' for topic in module['topics']])}
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Start Module {module['icon']}", key=f"btn_{i}", use_container_width=True):
            st.switch_page(module['page'])

# Getting started
st.markdown("---")
st.markdown("## 🚀 Getting Started")

st.markdown("""
This educational platform is designed to help you master subnet architecture and BACnet network concepts through:

1. **Progressive Learning**: Start with fundamentals and build to advanced topics
2. **Hands-On Practice**: Interactive tools and simulators for experimentation
3. **Visual Demonstrations**: Animated visualizations of network behavior
4. **Real-World Application**: BACnet-specific examples from building automation

**Ready to start?** Use the sidebar navigation to select your first module!
""")

# Tips and resources
with st.expander("💡 Tips for Success"):
    st.markdown("""
    - **Take your time**: Understanding subnet concepts takes practice
    - **Experiment freely**: All simulations are safe and non-destructive
    - **Use the interactive tools**: Hands-on learning is most effective
    - **Review binary operations**: They're fundamental to subnet masking
    - **Apply to real scenarios**: Think about your own network environments
    """)

with st.expander("📚 Additional Resources"):
    st.markdown("""
    - **BACnet Protocol Specification**: ASHRAE Standard 135
    - **IPv4 Addressing**: RFC 791
    - **CIDR Notation**: RFC 4632
    - **Subnetting Guides**: Multiple online calculators and reference materials
    - **BACnet/IP**: Annex J of ASHRAE Standard 135
    """)

# Footer
st.markdown(get_ace_footer(), unsafe_allow_html=True)
