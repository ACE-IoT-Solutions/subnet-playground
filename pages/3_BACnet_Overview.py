"""
Module 3: BACnet Overview
Introduction to BACnet/IP protocol and device discovery
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ace_subnet_playground.subnet_calcs import calculate_subnet_info
from ace_subnet_playground.branding import get_ace_brand_css, get_ace_footer

# Page config
st.set_page_config(
    page_title="BACnet Overview | BACnet Academy",
    page_icon="🏢",
    layout="wide"
)

# Apply ACE IoT Solutions Brand
st.markdown(get_ace_brand_css(), unsafe_allow_html=True)
st.markdown("""
<style>
    .protocol-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .device-card {
        background-color: #F8F9FA; color: #1a1a1a;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #4A90E2;
        margin: 1rem 0;
    }
    .message-flow {
        background-color: #E8F4F8; color: #1a1a1a;
        padding: 1rem;
        border-radius: 8px;
        font-family: monospace;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🏢 Module 3: BACnet Overview")
st.markdown("**Learn BACnet/IP protocol fundamentals and device discovery mechanisms**")
st.markdown("---")

# Learning Objectives
with st.expander("🎯 Learning Objectives", expanded=False):
    st.markdown("""
    By the end of this module, you will understand:
    - What BACnet is and why it's used in building automation
    - How BACnet/IP works on networks
    - The Who-Is/I-Am discovery mechanism
    - BACnet device instances and network numbers
    - Why subnet configuration matters for BACnet
    """)

# Section 1: What is BACnet?
st.header("1️⃣ What is BACnet?")

st.markdown("""
<div class="protocol-box">
    <h3>🏢 Building Automation and Control Networks</h3>
    <p><strong>BACnet</strong> is a data communication protocol for building automation and control systems.</p>
    <p>It's the international standard (ASHRAE Standard 135, ISO 16484-5) for connecting:</p>
    <ul>
        <li>HVAC equipment (chillers, air handlers, VAVs)</li>
        <li>Lighting systems</li>
        <li>Security and access control</li>
        <li>Fire safety systems</li>
        <li>Energy meters and sensors</li>
    </ul>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Why BACnet?")
    st.markdown("""
    **Interoperability**: Different manufacturers' devices can communicate

    **Standardization**: Common language for building systems

    **Flexibility**: Supports multiple network types (IP, MS/TP, Ethernet)

    **Scalability**: From small buildings to large campuses

    **Cost Savings**: Avoid vendor lock-in, easier integration
    """)

with col2:
    st.subheader("Common BACnet Devices")

    devices_data = [
        {"Device Type": "JACE (Edge Controller)", "Typical Instance": "100-999"},
        {"Device Type": "VAV Controller", "Typical Instance": "1000-9999"},
        {"Device Type": "AHU Controller", "Typical Instance": "10000-19999"},
        {"Device Type": "Chiller Controller", "Typical Instance": "20000-29999"},
        {"Device Type": "Lighting Controller", "Typical Instance": "30000-39999"},
    ]

    df = pd.DataFrame(devices_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

# Section 2: BACnet/IP Protocol
st.markdown("---")
st.header("2️⃣ BACnet/IP Protocol")

st.markdown("""
**BACnet/IP** runs BACnet over standard IP networks using **UDP port 47808** (BAC0 in hexadecimal).

This allows BACnet devices to communicate over:
- Standard Ethernet networks
- WiFi networks
- IP-based VPNs
- The Internet (with proper security)
""")

# BACnet message structure
st.subheader("BACnet Message Structure")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    **Protocol Stack Layers:**

    ```
    ┌─────────────────────────────┐
    │  Application Layer (APDU)   │  ← Who-Is, I-Am, Read, Write
    ├─────────────────────────────┤
    │  Network Layer (NPDU)       │  ← Routing, Network Numbers
    ├─────────────────────────────┤
    │  BACnet Virtual Link (BVLL) │  ← UDP port 47808
    ├─────────────────────────────┤
    │  IP Layer                   │  ← IPv4 addressing
    ├─────────────────────────────┤
    │  Link Layer (Ethernet)      │  ← MAC addresses
    └─────────────────────────────┘
    ```
    """)

with col2:
    st.markdown("""
    **Key BACnet Services:**

    - **Who-Is**: Discover devices on network
    - **I-Am**: Announce device presence
    - **Read-Property**: Get device data
    - **Write-Property**: Set device values
    - **Subscribe-COV**: Monitor changes
    - **Who-Has**: Find objects
    - **I-Have**: Announce objects
    """)

# Section 3: Device Discovery (Who-Is/I-Am)
st.markdown("---")
st.header("3️⃣ Device Discovery: Who-Is & I-Am")

st.markdown("""
The **Who-Is/I-Am** mechanism is how BACnet devices find each other on a network.
""")

# Interactive discovery simulator
st.subheader("Interactive Discovery Simulator")

sim_col1, sim_col2 = st.columns([1, 1])

with sim_col1:
    st.markdown("**Network Configuration**")

    network_cidr = st.text_input("Network CIDR", value="192.168.1.0/24", key="discovery_net")

    # Device configurations
    st.markdown("**Device A (Initiator)**")
    device_a_ip = st.text_input("Device A IP", value="192.168.1.10", key="dev_a_ip")
    device_a_instance = st.number_input("Device A Instance", value=100, key="dev_a_inst")

    st.markdown("**Device B (Responder)**")
    device_b_ip = st.text_input("Device B IP", value="192.168.1.20", key="dev_b_ip")
    device_b_instance = st.number_input("Device B Instance", value=200, key="dev_b_inst")

    same_subnet = False
    if network_cidr:
        info = calculate_subnet_info(network_cidr)
        if 'error' not in info:
            from ace_subnet_playground.subnet_calcs import is_ip_in_subnet
            a_in = is_ip_in_subnet(device_a_ip, network_cidr)
            b_in = is_ip_in_subnet(device_b_ip, network_cidr)
            same_subnet = a_in and b_in

with sim_col2:
    st.markdown("**Discovery Process**")

    if st.button("🔍 Run Who-Is Discovery", type="primary"):
        if same_subnet:
            st.success("✅ **Devices are on the same subnet - Discovery will work!**")

            # Show discovery flow
            st.markdown("---")
            st.markdown("**Step-by-Step Discovery:**")

            # Step 1
            st.markdown(f"""
            <div class="message-flow">
            <strong>1. Who-Is Broadcast</strong><br>
            Device A ({device_a_ip}) sends:<br>
            → Destination: {info['broadcast_address']} (broadcast)<br>
            → Port: 47808 (BACnet/IP)<br>
            → Message: "Who-Is" (all devices)
            </div>
            """, unsafe_allow_html=True)

            # Step 2
            st.markdown(f"""
            <div class="message-flow">
            <strong>2. Broadcast Propagation</strong><br>
            Switch forwards to ALL devices on VLAN<br>
            → Device B ({device_b_ip}) receives broadcast<br>
            → All other devices on {network_cidr} receive it
            </div>
            """, unsafe_allow_html=True)

            # Step 3
            st.markdown(f"""
            <div class="message-flow">
            <strong>3. I-Am Response</strong><br>
            Device B ({device_b_ip}) responds:<br>
            → Destination: {info['broadcast_address']} (or Device A)<br>
            → Port: 47808<br>
            → Message: "I-Am" (Device Instance: {device_b_instance})
            </div>
            """, unsafe_allow_html=True)

            # Step 4
            st.markdown(f"""
            <div class="message-flow">
            <strong>4. Discovery Complete</strong><br>
            Device A now knows:<br>
            → Device Instance: {device_b_instance}<br>
            → IP Address: {device_b_ip}<br>
            → Can now send Read/Write commands
            </div>
            """, unsafe_allow_html=True)

        else:
            st.error("❌ **Devices are NOT on the same subnet - Discovery will fail!**")
            st.warning("""
            **Why it fails:**
            - Who-Is uses broadcast to subnet broadcast address
            - Routers don't forward broadcasts between subnets
            - Device B never receives the Who-Is message

            **Solution:** Use BBMD (covered in Module 4!)
            """)

# Section 4: Device Instances
st.markdown("---")
st.header("4️⃣ BACnet Device Instances")

st.markdown("""
Every BACnet device must have a **unique Device Instance** number (0 - 4,194,303).

Think of it like a building's apartment number system - each unit needs a unique number.
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Device Instance Rules:**

    ✅ **Must be unique** on the network
    ❌ No two devices can share the same instance
    🔢 Range: 0 to 4,194,303
    📝 Convention: Group by device type (e.g., VAVs = 1000-1999)
    """)

with col2:
    st.markdown("""
    **Example Numbering Scheme:**

    ```
    Building Controllers:    100-199
    Floor Controllers:       200-299
    VAV Controllers:        1000-1999
    AHU Controllers:       10000-10999
    Chiller Controllers:   20000-20999
    Lighting Controllers:  30000-30999
    ```
    """)

# Interactive instance checker
st.subheader("Device Instance Conflict Checker")

check_col1, check_col2 = st.columns(2)

with check_col1:
    instances_input = st.text_area(
        "Enter device instances (one per line)",
        value="100\n200\n1050\n1051\n10000",
        height=150
    )

with check_col2:
    if st.button("Check for Conflicts", type="primary"):
        try:
            instances = [int(line.strip()) for line in instances_input.split('\n') if line.strip()]

            # Check for duplicates
            duplicates = [x for x in instances if instances.count(x) > 1]
            unique_duplicates = list(set(duplicates))

            if unique_duplicates:
                st.error(f"❌ **Conflict Found!**\n\nDuplicate instances: {unique_duplicates}")
            else:
                st.success(f"✅ **No conflicts!**\n\nAll {len(instances)} device instances are unique.")

            # Show summary
            st.info(f"""
            **Summary:**
            - Total devices: {len(instances)}
            - Unique instances: {len(set(instances))}
            - Range: {min(instances)} - {max(instances)}
            """)

        except ValueError:
            st.error("Invalid input. Please enter numeric device instances only.")

# Section 5: Network Numbers
st.markdown("---")
st.header("5️⃣ BACnet Network Numbers")

st.markdown("""
**BACnet Network Numbers** identify different BACnet networks in a multi-network system.

- Range: 0 - 65,535
- Network 0 = local network only (no routing)
- Each physical network segment gets a unique network number
- Used for routing between networks
""")

# Example network diagram
st.subheader("Example: Three-Floor Building")

network_example = """
```
Floor 3: Network 3000
├── 10.0.3.0/24
├── JACE-3 (Device 103, IP: 10.0.3.10)
├── VAV-301 (Device 3001, IP: 10.0.3.101)
└── VAV-302 (Device 3002, IP: 10.0.3.102)

Floor 2: Network 2000
├── 10.0.2.0/24
├── JACE-2 (Device 102, IP: 10.0.2.10)
├── VAV-201 (Device 2001, IP: 10.0.2.101)
└── VAV-202 (Device 2002, IP: 10.0.2.102)

Floor 1: Network 1000
├── 10.0.1.0/24
├── JACE-1 (Device 101, IP: 10.0.1.10)
├── VAV-101 (Device 1001, IP: 10.0.1.101)
└── VAV-102 (Device 1002, IP: 10.0.1.102)
```
"""

st.markdown(network_example)

st.warning("""
⚠️ **Common Mistake:**

Using the **same network number** (e.g., 1000) on all floors creates conflicts!

✅ **Correct:** Each floor gets unique network number (1000, 2000, 3000)
""")

# Section 6: Why Subnets Matter
st.markdown("---")
st.header("6️⃣ Why Subnet Configuration Matters for BACnet")

reasons = [
    {
        "Reason": "Discovery",
        "Issue": "Who-Is broadcasts don't cross routers",
        "Impact": "Devices on different subnets can't find each other",
        "Solution": "Use BBMD or keep devices on same subnet"
    },
    {
        "Reason": "Performance",
        "Issue": "Too many devices = broadcast storms",
        "Impact": "Network congestion, slow responses",
        "Solution": "Segment into multiple /24 subnets with BBMDs"
    },
    {
        "Reason": "IP Conflicts",
        "Issue": "Duplicate private IP ranges across sites",
        "Impact": "VPN connections fail, wrong device responds",
        "Solution": "Unique IP subnets per site"
    },
    {
        "Reason": "Network Numbers",
        "Issue": "Same network number on different subnets",
        "Impact": "Routing confusion, device conflicts",
        "Solution": "Unique network number per subnet"
    }
]

df_reasons = pd.DataFrame(reasons)
st.dataframe(df_reasons, use_container_width=True, hide_index=True)

# Key Takeaways
st.markdown("---")
st.header("🎓 Key Takeaways")

st.markdown("""
<div style="background-color: #FFF4CC; color: #1a1a1a; padding: 1.5rem; border-radius: 8px; border: 2px solid #FFD700;">
    <h4>Remember These Important Points:</h4>
    <ol>
        <li><strong>BACnet/IP</strong>: Runs on UDP port 47808, uses standard IP networks</li>
        <li><strong>Who-Is/I-Am</strong>: Discovery mechanism using broadcasts (only works on same subnet)</li>
        <li><strong>Device Instances</strong>: Must be unique across entire BACnet internetwork</li>
        <li><strong>Network Numbers</strong>: Identify different BACnet networks for routing</li>
        <li><strong>Subnet Design</strong>: Critical for BACnet discovery and performance</li>
        <li><strong>Broadcast Limitation</strong>: Routers block broadcasts → need BBMD for multi-subnet</li>
    </ol>
</div>
""", unsafe_allow_html=True)

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("⬅️ Back to Binary Ops", use_container_width=True):
        st.switch_page("pages/2_Binary_Operations.py")
with col3:
    if st.button("Continue to BBMD ➡️", use_container_width=True, type="primary"):
        st.switch_page("pages/4_BBMD_Architecture.py")
