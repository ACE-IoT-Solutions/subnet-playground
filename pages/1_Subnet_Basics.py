"""
Module 1: Subnet Basics
Interactive subnet mask calculator and educational visualizations
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ace_subnet_playground.subnet_calcs import (
    calculate_subnet_info,
    cidr_to_netmask,
    ip_to_binary,
    get_network_class,
    is_private_network
)
from ace_subnet_playground.branding import get_ace_brand_css, get_ace_footer

# Page config
st.set_page_config(
    page_title="Subnet Basics | BACnet Academy",
    page_icon="🔢",
    layout="wide"
)

# Apply ACE IoT Solutions Brand
st.markdown(get_ace_brand_css(), unsafe_allow_html=True)
st.markdown("""
<style>
    .metric-card {
        background-color: var(--ace-light-gray);
        color: var(--ace-dark);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid var(--ace-lime);
    }
    .binary-network {
        color: #2196F3;
        font-weight: bold;
    }
    .binary-host {
        color: #4CAF50;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🔢 Module 1: Subnet Basics")
st.markdown("**Learn subnet mask calculations, CIDR notation, and network fundamentals**")
st.markdown("---")

# Learning Objectives
with st.expander("🎯 Learning Objectives", expanded=False):
    st.markdown("""
    By the end of this module, you will be able to:
    - Understand IP addressing and subnet mask fundamentals
    - Calculate network and host portions from CIDR notation
    - Determine usable IP addresses in any subnet
    - Convert between decimal and binary representations
    - Apply subnet calculations to BACnet networks
    """)

# Section 1: Interactive Subnet Calculator
st.header("1️⃣ Interactive Subnet Calculator")

st.markdown("""
A **subnet mask** divides an IP address into **network** and **host** portions.
The CIDR (Classless Inter-Domain Routing) notation uses a slash followed by the number of network bits.
""")

col1, col2 = st.columns([2, 3])

with col1:
    st.subheader("Configuration")

    # IP Address input
    ip_address = st.text_input(
        "IP Address",
        value="192.168.1.100",
        help="Enter an IP address in dotted decimal notation"
    )

    # CIDR Slider
    cidr = st.slider(
        "CIDR Prefix Length",
        min_value=8,
        max_value=32,
        value=24,
        help="Number of network bits (lower = larger network)"
    )

    # Calculate subnet info
    subnet_str = f"{ip_address}/{cidr}"
    info = calculate_subnet_info(subnet_str)

    if 'error' not in info:
        st.success(f"✅ Valid subnet: `{subnet_str}`")

        # Network class
        network_class = get_network_class(subnet_str)
        is_private = is_private_network(subnet_str)

        st.markdown(f"""
        - **Network Class**: {network_class}
        - **Private Network**: {'Yes' if is_private else 'No'}
        """)
    else:
        st.error(f"❌ {info['error']}")

with col2:
    st.subheader("Subnet Information")

    if 'error' not in info:
        # Display key metrics in columns
        metric_col1, metric_col2, metric_col3 = st.columns(3)

        with metric_col1:
            st.metric(
                "Network Address",
                info['network_address'],
                delta=None
            )
            st.metric(
                "Subnet Mask",
                info['netmask'],
                delta=None
            )

        with metric_col2:
            st.metric(
                "Broadcast Address",
                info['broadcast_address'],
                delta=None
            )
            st.metric(
                "Wildcard Mask",
                info['wildcard_mask'],
                delta=None
            )

        with metric_col3:
            st.metric(
                "Total Addresses",
                f"{info['total_addresses']:,}",
                delta=None
            )
            st.metric(
                "Usable Hosts",
                f"{info['usable_hosts']:,}",
                delta=None
            )

# Visual representation of address space
if 'error' not in info:
    st.subheader("Address Space Visualization")

    # Network vs Host bits bar
    network_bits = info['network_bits']
    host_bits = info['host_bits']
    network_pct = (network_bits / 32) * 100
    host_pct = (host_bits / 32) * 100

    st.markdown(f"""
    <div style="width: 100%; height: 60px; display: flex; margin: 20px 0; border: 2px solid #ccc; border-radius: 8px; overflow: hidden;">
        <div style="width: {network_pct}%; background-color: #2196F3; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 16px;">
            Network: {network_bits} bits
        </div>
        <div style="width: {host_pct}%; background-color: #4CAF50; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 16px;">
            Host: {host_bits} bits
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Usable IP range
    st.markdown(f"""
    **Usable IP Range**: `{info['first_usable']}` to `{info['last_usable']}`

    - **First usable**: Network address + 1
    - **Last usable**: Broadcast address - 1
    - **Reserved**: Network address (`{info['network_address']}`) and Broadcast address (`{info['broadcast_address']}`)
    """)

# Section 2: Binary Representation
st.markdown("---")
st.header("2️⃣ Binary Representation")

st.markdown("""
Computers process IP addresses and subnet masks in **binary** (base 2). Understanding binary is essential for subnet calculations.
""")

if 'error' not in info:
    # Convert IP and netmask to binary
    ip_binary = ip_to_binary(ip_address)
    netmask_binary = ip_to_binary(info['netmask'])
    network_binary = ip_to_binary(info['network_address'])

    if ip_binary and netmask_binary and network_binary:
        # Create binary visualization
        binary_data = []

        # IP Address
        ip_octets = ip_binary.split('.')
        ip_network_part = '.'.join(ip_octets[:network_bits//8])
        if network_bits % 8:
            ip_network_part += '.' + ip_octets[network_bits//8][:network_bits%8]

        st.subheader("IP Address in Binary")
        st.code(f"Decimal:  {ip_address}\nBinary:   {ip_binary}", language="text")

        st.subheader("Subnet Mask in Binary")
        st.code(f"Decimal:  {info['netmask']}\nBinary:   {netmask_binary}\nCIDR:     /{cidr}", language="text")

        st.subheader("Network Address in Binary")
        st.code(f"Decimal:  {info['network_address']}\nBinary:   {network_binary}", language="text")

        # Explanation
        st.markdown("""
        **How it works:**
        - Network bits (in blue) identify the network
        - Host bits (in green) identify specific devices
        - Subnet mask has all 1s for network bits, all 0s for host bits
        """)

# Section 3: Common Subnet Masks
st.markdown("---")
st.header("3️⃣ Common Subnet Masks Reference")

st.markdown("""
Here are the most common subnet masks used in BACnet/IP networks:
""")

# Common masks table
common_masks = [
    {"CIDR": "/8", "Mask": "255.0.0.0", "Hosts": "16,777,214", "Use Case": "Class A networks (very large)"},
    {"CIDR": "/16", "Mask": "255.255.0.0", "Hosts": "65,534", "Use Case": "Large campus or enterprise"},
    {"CIDR": "/20", "Mask": "255.255.240.0", "Hosts": "4,094", "Use Case": "Medium-large building"},
    {"CIDR": "/22", "Mask": "255.255.252.0", "Hosts": "1,022", "Use Case": "Medium building"},
    {"CIDR": "/23", "Mask": "255.255.254.0", "Hosts": "510", "Use Case": "Small-medium building"},
    {"CIDR": "/24", "Mask": "255.255.255.0", "Hosts": "254", "Use Case": "Standard BACnet network ⭐"},
    {"CIDR": "/25", "Mask": "255.255.255.128", "Hosts": "126", "Use Case": "Small network segment"},
    {"CIDR": "/26", "Mask": "255.255.255.192", "Hosts": "62", "Use Case": "Very small segment"},
    {"CIDR": "/27", "Mask": "255.255.255.224", "Hosts": "30", "Use Case": "Tiny network"},
    {"CIDR": "/30", "Mask": "255.255.255.252", "Hosts": "2", "Use Case": "Point-to-point links"},
]

df = pd.DataFrame(common_masks)
st.dataframe(df, use_container_width=True, hide_index=True)

st.info("💡 **BACnet Best Practice**: Most BACnet/IP networks use `/24` (255.255.255.0), providing 254 usable addresses - perfect for most building automation systems.")

# Section 4: Interactive Practice
st.markdown("---")
st.header("4️⃣ Practice Exercise")

st.markdown("Test your understanding by calculating subnet information:")

practice_col1, practice_col2 = st.columns(2)

with practice_col1:
    practice_network = st.text_input(
        "Enter a network in CIDR notation",
        value="10.0.0.0/16",
        help="Example: 192.168.10.0/24"
    )

    if st.button("Calculate", type="primary"):
        practice_info = calculate_subnet_info(practice_network)

        if 'error' not in practice_info:
            st.session_state['practice_result'] = practice_info
        else:
            st.error(practice_info['error'])

with practice_col2:
    if 'practice_result' in st.session_state:
        result = st.session_state['practice_result']
        st.success("✅ Calculation Complete!")
        st.json(result)

# Key Takeaways
st.markdown("---")
st.header("🎓 Key Takeaways")

st.markdown("""
<div class="highlight-box">
    <h4>Remember These Important Points:</h4>
    <ol>
        <li><strong>CIDR Notation</strong>: The /XX number indicates how many network bits (e.g., /24 = 24 network bits, 8 host bits)</li>
        <li><strong>Usable Addresses</strong>: Total addresses minus 2 (network and broadcast)</li>
        <li><strong>Network Bits</strong>: Higher CIDR = more network bits = smaller network</li>
        <li><strong>Subnet Mask</strong>: Has 1s for network bits, 0s for host bits</li>
        <li><strong>BACnet Standard</strong>: Most BACnet/IP networks use /24 for simplicity</li>
    </ol>
</div>
""", unsafe_allow_html=True)

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("**Next Module**: Binary Operations ➡️")
    if st.button("Continue to Binary Operations", type="primary", use_container_width=True):
        st.switch_page("pages/2_Binary_Operations.py")
