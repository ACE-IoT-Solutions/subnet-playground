"""
Module 4: BBMD Architecture
Interactive BBMD configuration and message routing demonstration
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ace_subnet_playground.subnet_calcs import calculate_subnet_info, is_ip_in_subnet
from ace_subnet_playground.branding import get_ace_brand_css, get_ace_footer

# Page config
st.set_page_config(
    page_title="BBMD Architecture | BACnet Academy",
    page_icon="🌉",
    layout="wide"
)

# Apply ACE IoT Solutions Brand
st.markdown(get_ace_brand_css(), unsafe_allow_html=True)
st.markdown("""
<style>
    .bbmd-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .bdt-entry {
        background-color: #E8F4F8; color: #1a1a1a;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4A90E2;
        margin: 0.5rem 0;
    }
    .routing-step {
        background-color: #F8F9FA; color: #1a1a1a;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🌉 Module 4: BBMD Architecture")
st.markdown("**Master BACnet Broadcast Management Device configuration and routing**")
st.markdown("---")

# Learning Objectives
with st.expander("🎯 Learning Objectives", expanded=False):
    st.markdown("""
    By the end of this module, you will understand:
    - What a BBMD is and why it's needed
    - How BBMDs enable cross-subnet BACnet communication
    - Broadcast Distribution Table (BDT) configuration
    - Foreign Device Table (FDT) management
    - How BBMDs route Who-Is broadcasts across subnets
    """)

# Section 1: What is a BBMD?
st.header("1️⃣ What is a BBMD?")

st.markdown("""
<div class="bbmd-box">
    <h3>🌉 BACnet Broadcast Management Device</h3>
    <p>A <strong>BBMD</strong> is a special BACnet device that forwards broadcasts between different IP subnets.</p>
    <p><strong>The Problem:</strong> Routers block broadcasts → BACnet devices on different subnets can't discover each other</p>
    <p><strong>The Solution:</strong> BBMD converts broadcasts to unicast, sends across router, re-broadcasts on remote subnet</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Without BBMD")
    st.markdown("""
    ```
    Subnet A: 192.168.1.0/24
    ├── Device A: 192.168.1.10
    └── Sends Who-Is to 192.168.1.255

    [ROUTER] ← Blocks broadcast! ❌

    Subnet B: 10.0.2.0/24
    ├── Device B: 10.0.2.20
    └── Never receives Who-Is 😞
    ```

    **Result:** Devices can't discover each other
    """)

with col2:
    st.subheader("With BBMD")
    st.markdown("""
    ```
    Subnet A: 192.168.1.0/24
    ├── Device A: 192.168.1.10
    ├── BBMD-A: 192.168.1.1 ✓
    └── Sends Who-Is to 192.168.1.255

    [BBMD-A forwards via BDT] ✅
    ↓ Unicast to BBMD-B

    Subnet B: 10.0.2.0/24
    ├── BBMD-B: 10.0.2.1 ✓
    ├── Re-broadcasts to 10.0.2.255
    └── Device B receives Who-Is! 😊
    ```

    **Result:** Cross-subnet discovery works!
    """)

# Section 2: BBMD Operation
st.markdown("---")
st.header("2️⃣ How BBMD Works")

st.markdown("""
BBMDs operate using two key tables:
1. **BDT (Broadcast Distribution Table)**: List of other BBMDs to forward broadcasts to
2. **FDT (Foreign Device Table)**: Devices on remote subnets that register with this BBMD
""")

# Detailed operation flow
st.subheader("Step-by-Step Operation")

tabs = st.tabs(["1. Receive Broadcast", "2. Check BDT", "3. Forward", "4. Re-broadcast", "5. Reverse Path"])

with tabs[0]:
    st.markdown("""
    ### Step 1: BBMD Receives Local Broadcast

    ```
    Device on 192.168.1.0/24 sends:
    - Source IP: 192.168.1.50
    - Destination: 192.168.1.255 (broadcast)
    - Port: 47808
    - Message: Who-Is
    ```

    **BBMD-A (192.168.1.1) receives this broadcast** because it's on the same subnet.

    The BBMD recognizes this as a BACnet broadcast that needs to be forwarded.
    """)

with tabs[1]:
    st.markdown("""
    ### Step 2: BBMD Checks Broadcast Distribution Table (BDT)

    **BBMD-A's BDT:**

    | BBMD Address | Port | Subnet |
    |--------------|------|--------|
    | 10.0.2.1 | 47808 | 10.0.2.0/24 |
    | 10.0.3.1 | 47808 | 10.0.3.0/24 |

    BBMD-A sees it needs to forward to:
    - BBMD-B at 10.0.2.1
    - BBMD-C at 10.0.3.1
    """)

with tabs[2]:
    st.markdown("""
    ### Step 3: BBMD Forwards as Unicast

    BBMD-A wraps the original broadcast in a "Forwarded-NPDU" message and sends **unicast** (not broadcast):

    ```
    Message 1:
    - Source: 192.168.1.1 (BBMD-A)
    - Destination: 10.0.2.1 (BBMD-B) ← UNICAST!
    - Port: 47808
    - Content: Forwarded-NPDU containing original Who-Is

    Message 2:
    - Source: 192.168.1.1 (BBMD-A)
    - Destination: 10.0.3.1 (BBMD-C) ← UNICAST!
    - Port: 47808
    - Content: Forwarded-NPDU containing original Who-Is
    ```

    **Key Point:** Routers allow unicast packets through! ✅
    """)

with tabs[3]:
    st.markdown("""
    ### Step 4: Remote BBMD Re-broadcasts

    **BBMD-B receives the forwarded message:**

    1. Unwraps the Forwarded-NPDU
    2. Extracts the original Who-Is message
    3. **Re-broadcasts on local subnet 10.0.2.0/24**

    ```
    BBMD-B sends:
    - Source: 10.0.2.1
    - Destination: 10.0.2.255 (local broadcast)
    - Port: 47808
    - Message: Who-Is (original message)
    ```

    Now all devices on 10.0.2.0/24 receive the Who-Is!
    """)

with tabs[4]:
    st.markdown("""
    ### Step 5: Response (Reverse Path)

    When Device B (10.0.2.20) responds with I-Am:

    1. BBMD-B receives the I-Am broadcast
    2. Checks BDT, forwards to BBMD-A via unicast
    3. BBMD-A re-broadcasts on 192.168.1.0/24
    4. Original Device A receives the I-Am response

    **The path works in both directions - BUT requires symmetric BDT configuration!**

    ⚠️ **Critical**: BBMD-A having BBMD-B in its BDT does NOT automatically mean
    BBMD-B will forward to BBMD-A. Each BBMD must explicitly have the other in
    its BDT for bidirectional communication to work.
    """)

# Section 3: Interactive BDT Builder
st.markdown("---")
st.header("3️⃣ Interactive BDT Builder")

st.markdown("""
Configure a BBMD's Broadcast Distribution Table (BDT) to connect multiple subnets.
""")

# Initialize session state for BDT
if 'bdt_entries' not in st.session_state:
    st.session_state.bdt_entries = [
        {"bbmd_ip": "10.0.2.1", "port": 47808, "subnet": "10.0.2.0/24", "description": "Floor 2"},
        {"bbmd_ip": "10.0.3.1", "port": 47808, "subnet": "10.0.3.0/24", "description": "Floor 3"}
    ]

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("BBMD Configuration")

    # This BBMD's info
    this_bbmd_ip = st.text_input("This BBMD IP", value="192.168.1.1", key="this_bbmd")
    this_subnet = st.text_input("This Subnet", value="192.168.1.0/24", key="this_subnet")

    st.markdown("---")
    st.subheader("Add BDT Entry")

    new_bbmd_ip = st.text_input("Remote BBMD IP", value="", key="new_bbmd_ip")
    new_port = st.number_input("Port", value=47808, min_value=1, max_value=65535, key="new_port")
    new_subnet = st.text_input("Remote Subnet", value="", key="new_subnet")
    new_description = st.text_input("Description", value="", key="new_desc")

    if st.button("➕ Add Entry", type="primary"):
        if new_bbmd_ip and new_subnet:
            st.session_state.bdt_entries.append({
                "bbmd_ip": new_bbmd_ip,
                "port": new_port,
                "subnet": new_subnet,
                "description": new_description
            })
            st.success(f"Added {new_bbmd_ip}")
            st.rerun()
        else:
            st.error("Please enter BBMD IP and subnet")

with col2:
    st.subheader("Broadcast Distribution Table (BDT)")

    if st.session_state.bdt_entries:
        df_bdt = pd.DataFrame(st.session_state.bdt_entries)
        st.dataframe(df_bdt, use_container_width=True, hide_index=True)

        if st.button("🗑️ Clear All Entries"):
            st.session_state.bdt_entries = []
            st.rerun()

        # Network diagram visualization
        st.markdown("---")
        st.subheader("Network Topology")

        # Create network diagram
        fig = go.Figure()

        # This BBMD (center)
        fig.add_trace(go.Scatter(
            x=[0],
            y=[0],
            mode='markers+text',
            marker=dict(size=40, color='#4A90E2'),
            text=[f"BBMD\n{this_bbmd_ip}"],
            textposition="bottom center",
            name="This BBMD",
            showlegend=False
        ))

        # Remote BBMDs (arranged in circle)
        import math
        n_remote = len(st.session_state.bdt_entries)
        for i, entry in enumerate(st.session_state.bdt_entries):
            angle = (2 * math.pi * i) / n_remote
            x = 2 * math.cos(angle)
            y = 2 * math.sin(angle)

            # Add remote BBMD
            fig.add_trace(go.Scatter(
                x=[x],
                y=[y],
                mode='markers+text',
                marker=dict(size=30, color='#9B59B6'),
                text=[f"{entry['description']}<br>{entry['bbmd_ip']}"],
                textposition="top center",
                showlegend=False
            ))

            # Add connection line
            fig.add_trace(go.Scatter(
                x=[0, x],
                y=[0, y],
                mode='lines',
                line=dict(color='#27AE60', width=2, dash='dash'),
                showlegend=False
            ))

        fig.update_layout(
            title="BBMD Network Connections",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=400,
            hovermode='closest'
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No BDT entries configured. Add entries using the form on the left.")

# Section 4: Message Routing Simulator
st.markdown("---")
st.header("4️⃣ Message Routing Simulator")

st.markdown("Simulate a Who-Is broadcast traveling through BBMDs:")

if len(st.session_state.bdt_entries) > 0:
    # Source device selection
    sim_col1, sim_col2 = st.columns(2)

    with sim_col1:
        st.subheader("Source Device")
        source_ip = st.text_input("Device IP", value="192.168.1.50", key="sim_source")
        source_instance = st.number_input("Device Instance", value=100, key="sim_source_inst")

    with sim_col2:
        st.subheader("Target Subnet")
        target_options = [entry['subnet'] for entry in st.session_state.bdt_entries]
        target_subnet = st.selectbox("Which subnet should receive?", target_options, key="sim_target")

    if st.button("📡 Simulate Who-Is Broadcast", type="primary"):
        st.markdown("---")
        st.subheader("Message Flow")

        # Find target BBMD
        target_entry = next((e for e in st.session_state.bdt_entries if e['subnet'] == target_subnet), None)

        if target_entry:
            # Step 1: Local broadcast
            st.markdown(f"""
            <div class="routing-step">
            <strong>Step 1: Local Broadcast</strong><br>
            Device ({source_ip}) → Broadcast ({this_subnet.split('/')[0].rsplit('.', 1)[0]}.255)<br>
            Message: Who-Is<br>
            ✅ BBMD ({this_bbmd_ip}) receives broadcast
            </div>
            """, unsafe_allow_html=True)

            # Step 2: BDT lookup
            st.markdown(f"""
            <div class="routing-step">
            <strong>Step 2: BDT Lookup</strong><br>
            BBMD checks BDT table...<br>
            Found entry: {target_entry['bbmd_ip']} ({target_entry['description']})<br>
            ✅ Prepare to forward
            </div>
            """, unsafe_allow_html=True)

            # Step 3: Unicast forward
            st.markdown(f"""
            <div class="routing-step">
            <strong>Step 3: Unicast Forward</strong><br>
            BBMD ({this_bbmd_ip}) → BBMD ({target_entry['bbmd_ip']}) [UNICAST]<br>
            Message: Forwarded-NPDU containing Who-Is<br>
            ✅ Crosses router successfully (unicast allowed)
            </div>
            """, unsafe_allow_html=True)

            # Step 4: Re-broadcast
            broadcast_addr = target_subnet.split('/')[0].rsplit('.', 1)[0] + '.255'
            st.markdown(f"""
            <div class="routing-step">
            <strong>Step 4: Re-broadcast on Remote Subnet</strong><br>
            BBMD ({target_entry['bbmd_ip']}) → Broadcast ({broadcast_addr})<br>
            Message: Who-Is (original message)<br>
            ✅ All devices on {target_subnet} receive Who-Is!
            </div>
            """, unsafe_allow_html=True)

            st.success(f"""
            ✅ **Success!**

            The Who-Is broadcast successfully traveled from {this_subnet} to {target_subnet} via BBMD routing.

            Devices on {target_subnet} can now respond with I-Am messages, which will follow the reverse path.
            """)
else:
    st.warning("⚠️ Add some BDT entries first to simulate message routing!")

# Section 5: Foreign Device Table (FDT)
st.markdown("---")
st.header("5️⃣ Foreign Device Table (FDT)")

st.markdown("""
The **Foreign Device Table (FDT)** manages devices that are on remote networks but want to receive broadcasts from this BBMD.

**Use Cases:**
- VPN-connected devices
- Cloud-based monitoring systems
- Remote edge controllers
- Devices behind NAT
""")

# FDT example
st.subheader("FDT Registration Process")

fdt_cols = st.columns(2)

with fdt_cols[0]:
    st.markdown("""
    **Foreign Device Registration:**

    1. Remote device sends "Register-Foreign-Device" to BBMD
    2. Includes Time-to-Live (TTL) in seconds
    3. BBMD adds device to FDT
    4. BBMD forwards broadcasts to foreign device
    5. Device must re-register before TTL expires
    """)

with fdt_cols[1]:
    st.markdown("""
    **Example FDT Entry:**

    ```
    IP Address:    203.0.113.50
    Port:          47808
    TTL:           300 seconds (5 minutes)
    Remaining:     245 seconds
    ```

    Registration must be renewed every 5 minutes.
    """)

# Sample FDT table
st.subheader("Sample Foreign Device Table")

fdt_data = [
    {"IP Address": "203.0.113.50", "Port": 47808, "TTL": "300s", "Remaining": "245s", "Type": "Cloud Gateway"},
    {"IP Address": "198.51.100.10", "Port": 47808, "TTL": "600s", "Remaining": "580s", "Type": "VPN Edge Device"},
    {"IP Address": "192.0.2.100", "Port": 47808, "TTL": "120s", "Remaining": "95s", "Type": "Mobile App"},
]

df_fdt = pd.DataFrame(fdt_data)
st.dataframe(df_fdt, use_container_width=True, hide_index=True)

# Section 6: Split Horizon Architecture
st.markdown("---")
st.header("6️⃣ Split Horizon Architecture Pattern")

st.markdown("""
**Split Horizon** is a BACnet network architecture pattern that uses a **hub-and-spoke** topology to prevent broadcast loops while enabling multi-subnet communication.
""")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🔄 The Pattern")
    st.info("""
    **Split Horizon Hub-and-Spoke:**

    - **Central "Supervisory" subnet** with a hub BBMD
    - **Hub BBMD** has BDT entries for all spoke BBMDs
    - **Spoke BBMDs** only have the hub in their BDT
    - **Spokes do NOT have each other** in their BDTs

    This creates a star topology where all communication flows through the hub.
    """)

with col2:
    st.subheader("⚠️ Why It Works")
    st.success("""
    **Benefits of Split Horizon:**

    - No loops possible (spokes can't forward to each other)
    - Centralized management at supervisory subnet
    - Scalable - easy to add new spoke subnets
    - Simplified troubleshooting
    - Reduced broadcast traffic
    """)

# Split Horizon Scenario
st.subheader("Split Horizon Architecture Example")

st.markdown("""
Consider a multi-building campus with a central management building:
""")

split_scenario = st.radio(
    "Select Architecture",
    ["Split Horizon (Hub-and-Spoke)", "Full Mesh (Potential Loops)"],
    horizontal=True
)

if split_scenario == "Split Horizon (Hub-and-Spoke)":
    st.success("""
    **✅ Split Horizon Architecture (Safe & Scalable):**

    ```
                    Management Building (Hub)
                    Subnet: 192.168.0.0/24
                    BBMD-Hub (192.168.0.1)
                    BDT: [BBMD-A, BBMD-B, BBMD-C]
                            │
            ┌───────────────┼───────────────┐
            │               │               │
        Building A      Building B      Building C
      10.1.0.0/24      10.2.0.0/24      10.3.0.0/24
      BBMD-A           BBMD-B           BBMD-C
      BDT: [Hub]       BDT: [Hub]       BDT: [Hub]
    ```

    **Key Characteristics:**
    - Hub BBMD knows about all spoke BBMDs (A, B, C)
    - Each spoke BBMD only knows about Hub
    - Spokes do NOT list each other in their BDTs

    **Discovery Flow (Building A → Building B):**
    1. Device in Building A sends Who-Is broadcast (10.1.0.255)
    2. BBMD-A receives, checks BDT, forwards to Hub only
    3. Hub receives from BBMD-A, checks BDT, forwards to B and C
    4. BBMD-B receives from Hub, re-broadcasts on 10.2.0.0/24
    5. Devices in Building B respond
    6. **No loops possible** - BBMD-B only forwards back to Hub, not to C

    **Discovery Flow (Hub → Building A):**
    1. Device in Management sends Who-Is broadcast (192.168.0.255)
    2. Hub BBMD receives, checks BDT, forwards to A, B, and C
    3. All spoke BBMDs re-broadcast on their local subnets
    4. All field devices respond

    **Why It's Safe:**
    - Spokes cannot create loops (don't know about each other)
    - Hub is single point of broadcast distribution
    - Easy to add new buildings (update Hub BDT only)
    - Supervisory devices on hub subnet see all field devices
    """)

    st.markdown("**Real-World Use Case:** This is ideal for campus-style deployments with central management/monitoring.")

else:  # Full Mesh
    st.info("""
    **Full Mesh BDT Configuration (More Complex):**

    ```
                    Management Building
                    Subnet: 192.168.0.0/24
                    BBMD-Hub (192.168.0.1)
                    BDT: [BBMD-A, BBMD-B, BBMD-C]
                            │
            ┌───────────────┼───────────────┐
            │               │               │
        Building A      Building B      Building C
      10.1.0.0/24      10.2.0.0/24      10.3.0.0/24
      BBMD-A           BBMD-B           BBMD-C
      BDT: [Hub,B,C]   BDT: [Hub,A,C]   BDT: [Hub,A,B]
    ```

    **Key Characteristics:**
    - Every BBMD has every other BBMD in its BDT
    - Creates a full mesh topology
    - Broadcasts propagate across entire network

    **Tradeoffs:**
    - **More broadcast traffic** - Each broadcast is forwarded to all BBMDs
    - More complex configuration (N² BDT entries)
    - Adding a new building requires updating all BDTs
    - Harder to troubleshoot due to multiple paths

    **When Full Mesh Might Be Used:**
    - Buildings need direct communication without hub relay
    - Redundancy requirement if hub fails
    - Network latency concerns through hub

    **Note on Loop Prevention:**
    Modern BACnet BBMDs implement loop prevention by not re-forwarding broadcasts
    received from other BBMDs. However, increased broadcast traffic across all paths
    is unavoidable with full mesh topology.
    """)

# Practical Implementation
st.markdown("---")
st.subheader("💻 Implementation Recommendations")

impl_col1, impl_col2 = st.columns(2)

with impl_col1:
    st.markdown("""
    **Setting Up Split Horizon:**

    1. **Identify supervisory subnet** (management/HMI location)
    2. **Configure hub BBMD** with all spoke BBMDs in BDT
    3. **Configure each spoke BBMD** with only hub in BDT
    4. **Test discovery** from each subnet
    5. **Verify no loops** with packet capture
    6. **Document BDT configuration** for maintenance
    """)

with impl_col2:
    st.markdown("""
    **Scaling Split Horizon:**

    - **Adding new building:** Only update hub BDT
    - **Maximum spokes:** Limited by hub BBMD capacity (~50-100 typically)
    - **Hub redundancy:** Can use secondary hub with load balancing
    - **Monitoring:** Hub subnet ideal for monitoring tools
    - **Maintenance:** Central point for firmware updates
    """)

# Key Takeaways
st.markdown("---")
st.header("🎓 Key Takeaways")

st.markdown("""
<div style="background-color: #FFF4CC; color: #1a1a1a; padding: 1.5rem; border-radius: 8px; border: 2px solid #FFD700;">
    <h4>Remember These Important Points:</h4>
    <ol>
        <li><strong>BBMD Purpose</strong>: Enables BACnet communication across subnet boundaries</li>
        <li><strong>BDT (Broadcast Distribution Table)</strong>: Lists other BBMDs to forward broadcasts to</li>
        <li><strong>Broadcast → Unicast → Broadcast</strong>: BBMDs convert broadcasts to unicast for routing</li>
        <li><strong>Symmetric BDT Required</strong>: Each BBMD must have the other in its BDT for bidirectional communication</li>
        <li><strong>BDT Entries Are Directional</strong>: BBMD-A having B in its BDT ≠ automatic forwarding from B to A</li>
        <li><strong>FDT (Foreign Device Table)</strong>: Manages remote devices that register for broadcasts</li>
        <li><strong>Critical for Multi-Subnet</strong>: Without BBMD, cross-subnet discovery fails</li>
    </ol>
</div>
""", unsafe_allow_html=True)

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("⬅️ Back to BACnet", use_container_width=True):
        st.switch_page("pages/3_BACnet_Overview.py")
with col3:
    if st.button("Broadcast Storms ➡️", use_container_width=True, type="primary"):
        st.switch_page("pages/5_Broadcast_Storms.py")
