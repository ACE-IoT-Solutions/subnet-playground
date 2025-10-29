"""
Module 2: Binary Operations
Interactive bitwise AND tutorial and packet processing simulation
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ace_subnet_playground.subnet_calcs import ip_to_binary, calculate_subnet_info, is_ip_in_subnet
from ace_subnet_playground.branding import get_ace_brand_css, get_ace_footer

# Page config
st.set_page_config(
    page_title="Binary Operations | BACnet Academy",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ Module 2: Binary Operations")
st.markdown("**Master bitwise AND operations and packet processing logic**")
st.markdown("---")

# Learning Objectives
with st.expander("🎯 Learning Objectives", expanded=False):
    st.markdown("""
    By the end of this module, you will understand:
    - How bitwise AND operations work
    - How devices determine packet destinations
    - The mathematical foundation of subnet masks
    - Why broadcasts don't cross subnets
    """)

# Section 1: Bitwise AND Tutorial
st.header("1️⃣ Bitwise AND Operation")

st.markdown("""
The **bitwise AND** operation compares two binary values bit-by-bit:
- `1 AND 1 = 1`
- `1 AND 0 = 0`
- `0 AND 1 = 0`
- `0 AND 0 = 0`

**Result is 1 only when BOTH bits are 1**
""")

# Truth table
st.subheader("AND Truth Table")
truth_table = pd.DataFrame({
    "Bit A": ["0", "0", "1", "1"],
    "Bit B": ["0", "1", "0", "1"],
    "A AND B": ["0", "0", "0", "1"]
})
st.table(truth_table)

# Interactive AND calculator
st.markdown("---")
st.subheader("Interactive AND Calculator")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Input Values** (8 bits each)")
    value_a = st.text_input(
        "Value A (binary)",
        value="11001010",
        max_chars=8,
        help="Enter 8 binary digits (0 or 1)"
    )
    value_b = st.text_input(
        "Value B (binary)",
        value="11110000",
        max_chars=8,
        help="Enter 8 binary digits (0 or 1)"
    )

with col2:
    # Validate and calculate
    if len(value_a) == 8 and len(value_b) == 8 and all(c in '01' for c in value_a + value_b):
        result = ''.join(['1' if value_a[i] == '1' and value_b[i] == '1' else '0' for i in range(8)])

        st.markdown("**Results**")
        st.code(f"""
Value A:    {value_a}  (decimal: {int(value_a, 2)})
Value B:    {value_b}  (decimal: {int(value_b, 2)})
            --------
A AND B:    {result}  (decimal: {int(result, 2)})
        """, language="text")
    else:
        st.warning("⚠️ Please enter exactly 8 binary digits (0 or 1) for each value")

# Section 2: Packet Processing Simulation
st.markdown("---")
st.header("2️⃣ How Devices Process Packets")

st.markdown("""
When a device receives a network packet, it uses **bitwise AND** to determine if the packet is for its subnet:

**Process:**
1. Device calculates its network address: `Device IP AND Subnet Mask`
2. Device calculates packet's destination network: `Packet Destination AND Subnet Mask`
3. Device compares the two network addresses
   - **Match** → Process the packet
   - **No match** → Ignore the packet
""")

# Interactive packet processor
st.subheader("Interactive Packet Processing Simulator")

st.markdown("Configure a device and send it a packet:")

config_col1, config_col2 = st.columns(2)

with config_col1:
    st.markdown("**Device Configuration**")
    device_ip = st.text_input("Device IP Address", value="192.168.1.50")
    device_cidr = st.slider("Device Subnet Mask (CIDR)", 8, 32, 24, key="device_cidr")
    device_subnet = f"{device_ip}/{device_cidr}"

with config_col2:
    st.markdown("**Incoming Packet**")
    packet_dest = st.text_input("Packet Destination IP", value="192.168.1.100")

# Calculate and display results
if st.button("🔍 Process Packet", type="primary"):
    device_info = calculate_subnet_info(device_subnet)
    packet_in_subnet = is_ip_in_subnet(packet_dest, device_subnet)

    if 'error' not in device_info:
        # Get binary representations
        device_ip_bin = ip_to_binary(device_ip)
        device_mask_bin = ip_to_binary(device_info['netmask'])
        device_network_bin = ip_to_binary(device_info['network_address'])
        packet_dest_bin = ip_to_binary(packet_dest)

        # Calculate packet network
        packet_subnet = f"{packet_dest}/{device_cidr}"
        packet_info = calculate_subnet_info(packet_subnet)
        packet_network_bin = ip_to_binary(packet_info['network_address'])

        st.markdown("---")
        st.subheader("Step-by-Step Analysis")

        # Step 1
        with st.expander("**Step 1: Calculate Device's Network Address**", expanded=True):
            st.markdown("**Bitwise AND: Device IP & Subnet Mask**")
            st.code(f"""
Device IP:      {device_ip:<15} = {device_ip_bin}
Subnet Mask:    {device_info['netmask']:<15} = {device_mask_bin}
                                        {''.join(['--' for _ in range(36)])}
Network Addr:   {device_info['network_address']:<15} = {device_network_bin}
            """, language="text")

        # Step 2
        with st.expander("**Step 2: Calculate Packet's Destination Network**", expanded=True):
            st.markdown("**Bitwise AND: Packet Destination & Subnet Mask**")
            st.code(f"""
Packet Dest:    {packet_dest:<15} = {packet_dest_bin}
Subnet Mask:    {device_info['netmask']:<15} = {device_mask_bin}
                                        {''.join(['--' for _ in range(36)])}
Network Addr:   {packet_info['network_address']:<15} = {packet_network_bin}
            """, language="text")

        # Step 3
        with st.expander("**Step 3: Compare Network Addresses**", expanded=True):
            st.code(f"""
Device Network:   {device_info['network_address']}
Packet Network:   {packet_info['network_address']}
            """, language="text")

            if packet_in_subnet:
                st.success(f"✅ **MATCH!** Networks are the same.")
                st.info("**Decision**: Device will PROCESS this packet")
            else:
                st.error(f"❌ **NO MATCH!** Networks are different.")
                st.info("**Decision**: Device will IGNORE this packet")

        # Summary
        st.markdown("---")
        if packet_in_subnet:
            st.success(f"""
            ### ✅ Packet Processed

            The device at `{device_ip}` will **accept and process** this packet because:
            - Both device and packet are on network `{device_info['network_address']}/{device_cidr}`
            - This is a **local delivery** (same subnet)
            """)
        else:
            st.error(f"""
            ### ❌ Packet Ignored

            The device at `{device_ip}` will **ignore** this packet because:
            - Device is on network `{device_info['network_address']}/{device_cidr}`
            - Packet destination is on network `{packet_info['network_address']}/{device_cidr}`
            - This requires **routing** (different subnets)
            """)

# Section 3: Why Broadcasts Don't Cross Routers
st.markdown("---")
st.header("3️⃣ Why Broadcasts Don't Cross Subnet Boundaries")

st.markdown("""
A **broadcast** is sent to the subnet's broadcast address (all host bits = 1).

Example: For subnet `192.168.1.0/24`:
- Network address: `192.168.1.0`
- Broadcast address: `192.168.1.255`

**Layer 2 (Switches)**:
- Switches see broadcast destination
- Forward to ALL ports on the VLAN
- Devices receive and process

**Layer 3 (Routers)**:
- Routers perform subnet matching (bitwise AND)
- Broadcast address belongs to source subnet only
- Router doesn't forward to other subnets
- **Result**: Broadcasts are contained within their subnet
""")

# Example demonstration
st.subheader("Example: BACnet Who-Is Broadcast")

example_col1, example_col2 = st.columns(2)

with example_col1:
    st.markdown("**Scenario 1: Same Subnet (Works)**")
    st.code("""
Device A: 192.168.1.10/24
Device B: 192.168.1.20/24
Broadcast: 192.168.1.255

1. Device A sends Who-Is to 192.168.1.255
2. Switch forwards to all ports
3. Device B receives broadcast
4. Device B sends I-Am response
✅ Discovery works!
    """, language="text")

with example_col2:
    st.markdown("**Scenario 2: Different Subnets (Fails)**")
    st.code("""
Device A: 192.168.1.10/24
Device B: 10.0.2.20/24
Router between subnets

1. Device A sends Who-Is to 192.168.1.255
2. Broadcast reaches router
3. Router: "Destination is 192.168.1.0/24 network"
4. Router: "Don't forward to 10.0.2.0/24"
❌ Device B never sees broadcast!
    """, language="text")

st.info("""
💡 **This is why BBMDs are needed**: They convert broadcasts to unicast messages that CAN cross routers!
We'll explore this in Module 4.
""")

# Key Takeaways
st.markdown("---")
st.header("🎓 Key Takeaways")

st.markdown("""
<div style="background-color: #FFF4CC; color: #1a1a1a; padding: 1.5rem; border-radius: 8px; border: 2px solid #FFD700;">
    <h4>Remember These Important Points:</h4>
    <ol>
        <li><strong>Bitwise AND</strong>: Result is 1 only when BOTH bits are 1</li>
        <li><strong>Subnet Matching</strong>: Devices use AND to determine if packets are local</li>
        <li><strong>Network Address</strong>: IP AND Subnet Mask = Network Address</li>
        <li><strong>Broadcast Limitation</strong>: Routers don't forward broadcasts between subnets</li>
        <li><strong>BACnet Impact</strong>: Who-Is broadcasts only work within one subnet (without BBMD)</li>
    </ol>
</div>
""", unsafe_allow_html=True)

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("⬅️ Back to Subnet Basics", use_container_width=True):
        st.switch_page("pages/1_Subnet_Basics.py")
with col3:
    if st.button("Continue to BACnet ➡️", use_container_width=True, type="primary"):
        st.switch_page("pages/3_BACnet_Overview.py")
