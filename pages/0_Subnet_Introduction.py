"""
Module 0: Subnet Introduction
Visual introduction to subnets using restaurant table analogy
"""

import streamlit as st
import plotly.graph_objects as go
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ace_subnet_playground.branding import get_ace_brand_css, get_ace_footer

# Page config
st.set_page_config(
    page_title="Subnet Introduction | BACnet Academy",
    page_icon="🍽️",
    layout="wide"
)

# Apply ACE IoT Solutions Brand
st.markdown(get_ace_brand_css(), unsafe_allow_html=True)

# Header
st.title("🍽️ Module 0: Understanding Subnets")
st.markdown("**A Simple Analogy: The Restaurant**")
st.markdown("---")

# Introduction
st.markdown("""
Imagine a **restaurant** where people are seated at different tables. This is similar to how a **network** is divided into **subnets**!

### The Restaurant Analogy

- **🏢 Restaurant** = Your entire network
- **🪑 Tables** = Individual subnets
- **👥 People at a table** = Devices on the same subnet
- **🍷 Toast to the whole table** = Broadcast message
- **🧑‍🍳 Waiter** = Router (connects different tables)
""")

# Key Concept
st.info("""
**💡 Key Concept**: People sitting at the **same table** can talk directly to each other.
If you want to talk to someone at a **different table**, you need the **waiter (router)** to relay your message!
""")

st.markdown("---")

# Interactive Table Configuration
st.header("1️⃣ Interactive Restaurant Layout")

st.markdown("""
Use the slider below to see how we can arrange the same restaurant (network) with different table sizes (subnet configurations).
""")

# Configuration slider
table_config = st.select_slider(
    "Restaurant Configuration",
    options=[
        "One Big Table",
        "Two Large Tables",
        "Four Medium Tables",
        "Eight Small Tables",
        "Sixteen Two-Tops"
    ],
    value="Four Medium Tables",
    help="Different ways to divide up the same space"
)

# Map configurations to subnet details
config_details = {
    "One Big Table": {
        "tables": 1,
        "seats_per": 254,
        "cidr": "/24",
        "description": "Everyone can talk to everyone directly. Maximum flexibility, but can get noisy!",
        "layout": [(127, 127, 254)]  # x, y, size
    },
    "Two Large Tables": {
        "tables": 2,
        "seats_per": 126,
        "cidr": "/25",
        "description": "Two groups. Good for separating departments (e.g., HVAC vs. Lighting).",
        "layout": [(85, 127, 126), (169, 127, 126)]
    },
    "Four Medium Tables": {
        "tables": 4,
        "seats_per": 62,
        "cidr": "/26",
        "description": "Four groups. Common for multi-floor buildings (one subnet per floor).",
        "layout": [(64, 85, 62), (190, 85, 62), (64, 169, 62), (190, 169, 62)]
    },
    "Eight Small Tables": {
        "tables": 8,
        "seats_per": 30,
        "cidr": "/27",
        "description": "Eight groups. Good for isolating different zones or systems.",
        "layout": [
            (42, 64, 30), (127, 64, 30), (212, 64, 30),
            (42, 127, 30), (212, 127, 30),
            (42, 190, 30), (127, 190, 30), (212, 190, 30)
        ]
    },
    "Sixteen Two-Tops": {
        "tables": 16,
        "seats_per": 14,
        "cidr": "/28",
        "description": "Many small tables. Maximum isolation, but requires more routers to connect.",
        "layout": [
            (32, 42, 14), (85, 42, 14), (138, 42, 14), (191, 42, 14),
            (32, 85, 14), (85, 85, 14), (138, 85, 14), (191, 85, 14),
            (32, 138, 14), (85, 138, 14), (138, 138, 14), (191, 138, 14),
            (32, 191, 14), (85, 191, 14), (138, 191, 14), (191, 191, 14)
        ]
    }
}

details = config_details[table_config]

# Display configuration details
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Number of Tables", details["tables"])
with col2:
    st.metric("Seats per Table", details["seats_per"])
with col3:
    st.metric("Subnet Mask (CIDR)", details["cidr"])
with col4:
    st.metric("Total Capacity", details["tables"] * details["seats_per"])

st.markdown(f"**💭 {details['description']}**")

# Visualize the restaurant layout
fig = go.Figure()

# Draw tables as circles
for i, (x, y, size) in enumerate(details['layout']):
    # Table circle
    fig.add_trace(go.Scatter(
        x=[x],
        y=[y],
        mode='markers',
        marker=dict(
            size=size * 2,  # Scale for visibility
            color='rgba(192, 210, 1, 0.3)',  # ACE lime with transparency
            line=dict(color='#c0d201', width=3)
        ),
        name=f'Table {i+1}',
        hovertemplate=f'<b>Table {i+1}</b><br>{size} seats<extra></extra>',
        showlegend=False
    ))

    # Table label
    fig.add_annotation(
        x=x, y=y,
        text=f"Table {i+1}<br>{size} seats",
        showarrow=False,
        font=dict(size=10, color='#1a1a1a'),
        bgcolor='rgba(255, 255, 255, 0.8)',
        borderpad=4
    )

fig.update_layout(
    title=f"Restaurant Layout: {table_config}",
    xaxis=dict(range=[0, 254], showgrid=False, zeroline=False, showticklabels=False, title=""),
    yaxis=dict(range=[0, 254], showgrid=False, zeroline=False, showticklabels=False, title=""),
    height=500,
    plot_bgcolor='#f5f5f5',
    hovermode='closest',
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# Broadcast explanation
st.markdown("---")
st.header("2️⃣ The Toast (Broadcast Message)")

st.markdown("""
Imagine someone at **Table 2** wants to make a toast 🥂 to everyone at **their table**:

- ✅ **Everyone at Table 2** hears the toast (receives the broadcast)
- ❌ **Other tables** don't hear it (broadcasts don't cross subnet boundaries)
- 🧑‍🍳 The **waiter (router)** doesn't relay toasts to other tables

This is exactly how **broadcast messages** work in networks!
""")

col1, col2 = st.columns(2)

with col1:
    st.success("""
    **✅ Same Table (Same Subnet)**

    ```
    Device A: "Who-Is?" (broadcast)
    Device B: "I-Am device 100!"
    Device C: "I-Am device 101!"
    Device D: "I-Am device 102!"
    ```

    All devices on the subnet receive and respond.
    """)

with col2:
    st.error("""
    **❌ Different Table (Different Subnet)**

    ```
    Device A: "Who-Is?" (broadcast)
    Router: (blocks broadcast)
    Device X: (never hears the message)
    Device Y: (never hears the message)
    ```

    Broadcast doesn't cross the router boundary.
    """)

# BACnet connection
st.markdown("---")
st.header("3️⃣ Why This Matters for BACnet")

st.markdown("""
**BACnet/IP relies heavily on broadcast messages** for device discovery and communication:

- **Who-Is**: Broadcasts to discover devices on the network
- **I-Am**: Broadcast response announcing device presence
- **Who-Has**: Broadcast to find objects by name
- **I-Have**: Broadcast response with object information

### The Problem

If your BACnet devices are on **different subnets** (different tables), they **cannot discover each other** through broadcasts!

This is why understanding subnets is **critical** for BACnet network design.
""")

st.info("""
**💡 Solution Preview**: In Module 4, you'll learn about **BBMDs (BACnet Broadcast Management Devices)** -
think of them as special waiters who *do* relay toasts between tables! This allows BACnet broadcasts
to cross subnet boundaries.
""")

# Real-world example
st.markdown("---")
st.header("4️⃣ Real-World Example")

st.markdown("""
### Multi-Floor Office Building

Imagine a **4-floor office building** with BACnet devices:

- **Floor 1**: HVAC controllers (Subnet 1 - "Table 1")
- **Floor 2**: Lighting controllers (Subnet 2 - "Table 2")
- **Floor 3**: Access control (Subnet 3 - "Table 3")
- **Floor 4**: Management system (Subnet 4 - "Table 4")

**Without proper configuration**:
- Floor 1 HVAC can't discover Floor 2 lighting
- Floor 4 management system can't see Floor 1-3 devices
- Each floor is isolated (separate tables)

**With BBMDs** (covered in Module 4):
- All floors can discover each other
- Management system sees all devices
- System functions as one integrated network
""")

# Key Takeaways
st.markdown("---")
st.header("🎓 Key Takeaways")

st.markdown("""
<div class="highlight-box">
    <h4>Remember These Important Points:</h4>
    <ol>
        <li><strong>Subnet = Table</strong>: Devices on the same subnet can communicate directly</li>
        <li><strong>Router = Waiter</strong>: Needed to pass messages between different subnets</li>
        <li><strong>Broadcast = Toast</strong>: Only reaches devices on the same subnet/table</li>
        <li><strong>BACnet Uses Broadcasts</strong>: Device discovery relies on broadcasts (Who-Is/I-Am)</li>
        <li><strong>Subnet Design Matters</strong>: Poor subnet design = devices can't find each other</li>
    </ol>
</div>
""", unsafe_allow_html=True)

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("**Next Module**: Subnet Basics (Calculator) ➡️")
    if st.button("Continue to Subnet Calculator", type="primary", use_container_width=True):
        st.switch_page("pages/1_Subnet_Basics.py")

# Footer
st.markdown("---")
st.markdown(get_ace_footer(), unsafe_allow_html=True)
