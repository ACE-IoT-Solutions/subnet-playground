"""
Module 6: Network Scenarios
Real-world BACnet network configurations and troubleshooting
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ace_subnet_playground.subnet_calcs import calculate_subnet_info, check_subnet_overlap
from ace_subnet_playground.branding import get_ace_brand_css, get_ace_footer

# Page config
st.set_page_config(
    page_title="Network Scenarios | BACnet Academy",
    page_icon="🗺️",
    layout="wide"
)

# Apply ACE IoT Solutions Brand
st.markdown(get_ace_brand_css(), unsafe_allow_html=True)
st.markdown("""
<style>
    .scenario-box {
        background-color: #F8F9FA; color: #1a1a1a;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #3498DB;
        margin: 1rem 0;
    }
    .problem-box {
        background-color: #FFEBEE; color: #1a1a1a;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #E74C3C;
        margin: 1rem 0;
    }
    .solution-box {
        background-color: #E8F8F5; color: #1a1a1a;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #27AE60;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🗺️ Module 6: Real-World Network Scenarios")
st.markdown("**Apply your knowledge to practical BACnet networking challenges**")
st.markdown("---")

# Learning Objectives
with st.expander("🎯 Learning Objectives", expanded=False):
    st.markdown("""
    By the end of this module, you will be able to:
    - Diagnose common BACnet network problems
    - Design multi-subnet BACnet networks
    - Configure BBMDs for campus networks
    - Troubleshoot NAT and VPN issues
    - Apply best practices to real scenarios
    """)

# Scenario selector
st.header("📋 Select a Scenario")

scenarios = [
    "🏢 Three-Floor Office Building",
    "🏭 Industrial Campus Network",
    "🏥 Hospital with Multiple Buildings",
    "🌐 Multi-Site VPN Network",
    "⚠️ Troubleshooting: Discovery Failure",
    "⚠️ Troubleshooting: IP Conflicts"
]

selected_scenario = st.selectbox("Choose a scenario to explore:", scenarios)

# Scenario 1: Three-Floor Office Building
if selected_scenario == "🏢 Three-Floor Office Building":
    st.markdown("---")
    st.header("🏢 Scenario: Three-Floor Office Building")

    st.markdown("""
    **Background:**
    A 3-story office building with HVAC equipment on each floor needs a BACnet network.
    Each floor has approximately 50 BACnet devices (VAVs, sensors, controllers).
    """)

    tab1, tab2, tab3, tab4 = st.tabs(["Requirements", "Design", "Configuration", "Validation"])

    with tab1:
        st.subheader("Network Requirements")
        st.markdown("""
        **Physical Layout:**
        - Floor 3: Penthouse with rooftop AHUs (20 devices)
        - Floor 2: Office space with VAVs (40 devices)
        - Floor 1: Lobby with lighting and security (30 devices)
        - Basement: Mechanical room with chillers (15 devices)

        **Management Requirements:**
        - Central monitoring system in data room (Floor 2)
        - Web-based access for building managers
        - Historical trending and alarms

        **Technical Constraints:**
        - Existing network infrastructure (managed switches)
        - IPv4 addressing only
        - All devices BACnet/IP capable
        """)

    with tab2:
        st.subheader("Recommended Network Design")

        st.markdown("""
        **Subnet Allocation:**
        - Floor 3: `10.100.3.0/24` (Network 3000)
        - Floor 2: `10.100.2.0/24` (Network 2000)
        - Floor 1: `10.100.1.0/24` (Network 1000)
        - Basement: `10.100.0.0/24` (Network 500)
        - Management: `10.100.254.0/24`

        **BBMD Configuration:**
        - Place BBMD on each floor
        - All BBMDs in BDT of all others
        - Management system connects to Floor 2 BBMD
        """)

        # Network diagram
        st.markdown("**Network Topology:**")
        st.code("""
Floor 3 (10.100.3.0/24, Network 3000)
├── BBMD-3: 10.100.3.1
├── AHU-301: 10.100.3.10 (Device 3010)
├── AHU-302: 10.100.3.11 (Device 3011)
└── Rooftop Sensors...

Floor 2 (10.100.2.0/24, Network 2000) [DATA ROOM]
├── BBMD-2: 10.100.2.1
├── Management Server: 10.100.2.10
├── VAV-201 to VAV-240: 10.100.2.21-60 (Device 2001-2040)
└── Floor Sensors...

Floor 1 (10.100.1.0/24, Network 1000)
├── BBMD-1: 10.100.1.1
├── Lighting-101 to 115: 10.100.1.11-25 (Device 1001-1015)
├── Access Control...
└── Lobby Sensors...

Basement (10.100.0.0/24, Network 500)
├── BBMD-0: 10.100.0.1
├── Chiller-1: 10.100.0.10 (Device 501)
├── Chiller-2: 10.100.0.11 (Device 502)
└── Mechanical Equipment...
        """, language="text")

    with tab3:
        st.subheader("BBMD Configuration Details")

        st.markdown("**BBMD-2 (Floor 2) Configuration:**")

        st.markdown("""
        ```ini
        [BBMD Configuration]
        IP Address: 10.100.2.1
        Port: 47808
        Network Number: 2000

        [Broadcast Distribution Table]
        Entry 1: 10.100.3.1:47808  # Floor 3
        Entry 2: 10.100.1.1:47808  # Floor 1
        Entry 3: 10.100.0.1:47808  # Basement

        [Foreign Device Table]
        # None needed - all devices on local subnets
        ```
        """)

        st.info("""
        💡 **Design Notes:**
        - Each BBMD has identical BDT (all other BBMDs listed)
        - **Symmetric BDT entries required**: Each BBMD must list all others
        - Example: BBMD-2's BDT = [BBMD-3, BBMD-1, BBMD-0]
        - No circular loops (only ONE BBMD per subnet)
        - Management server uses BBMD-2 for discovery
        - Each floor is a separate broadcast domain
        """)

    with tab4:
        st.subheader("Network Validation Checklist")

        validation_checks = [
            {"Check": "Unique IP addresses", "Method": "IP conflict scan", "Status": "✅"},
            {"Check": "Unique device instances", "Method": "BACnet discovery", "Status": "✅"},
            {"Check": "Unique network numbers", "Method": "Configuration review", "Status": "✅"},
            {"Check": "BDT entries correct", "Method": "Ping each BBMD", "Status": "✅"},
            {"Check": "Cross-subnet discovery", "Method": "Who-Is from each floor", "Status": "✅"},
            {"Check": "Broadcast rates normal", "Method": "Switch statistics", "Status": "✅"},
            {"Check": "Read/Write operations", "Method": "Test from management", "Status": "✅"},
        ]

        df_validation = pd.DataFrame(validation_checks)
        st.dataframe(df_validation, use_container_width=True, hide_index=True)

# Scenario 2: Industrial Campus
elif selected_scenario == "🏭 Industrial Campus Network":
    st.markdown("---")
    st.header("🏭 Scenario: Industrial Campus Network")

    st.markdown("""
    **Background:**
    Manufacturing campus with 5 buildings spread across 200 acres.
    Each building has dedicated mechanical systems and production equipment.
    Central energy management system monitors all facilities.
    """)

    st.subheader("Network Requirements")
    st.markdown("""
    - Building 1: Administration (10.50.1.0/24)
    - Building 2: Production A (10.50.2.0/24)
    - Building 3: Production B (10.50.3.0/24)
    - Building 4: Warehouse (10.50.4.0/24)
    - Building 5: Central Plant (10.50.5.0/24)
    - Fiber optic backbone connecting all buildings
    """)

    st.subheader("Recommended Design")

    st.markdown("""
    **Key Considerations:**
    1. **High Availability**
       - Redundant BBMDs per building
       - Spanning Tree Protocol enabled
       - Backup routes through fiber ring

    2. **Security**
       - VLANs separate BACnet from IT traffic
       - Firewall between production and administration
       - BACnet traffic inspection

    3. **Scalability**
       - /24 subnets allow growth to 250+ devices per building
       - Reserved IP ranges for future expansion
       - Modular BBMD architecture

    4. **Performance**
       - QoS prioritization for BACnet traffic
       - Broadcast storm control enabled
       - Network monitoring on all links
    """)

# Scenario 3: Hospital
elif selected_scenario == "🏥 Hospital with Multiple Buildings":
    st.markdown("---")
    st.header("🏥 Scenario: Hospital with Multiple Buildings")

    st.markdown("""
    **Background:**
    Healthcare campus with critical infrastructure requiring 24/7 reliability.
    Strict regulatory compliance (HIPAA) and life safety considerations.
    """)

    st.subheader("Special Requirements")

    critical_systems = [
        {"System": "Life Safety", "Network": "10.200.1.0/24", "VLAN": "100", "Priority": "Critical"},
        {"System": "HVAC/Comfort", "Network": "10.200.2.0/24", "VLAN": "110", "Priority": "High"},
        {"System": "Energy Management", "Network": "10.200.3.0/24", "VLAN": "120", "Priority": "Medium"},
        {"System": "Access Control", "Network": "10.200.4.0/24", "VLAN": "130", "Priority": "High"},
    ]

    df_critical = pd.DataFrame(critical_systems)
    st.dataframe(df_critical, use_container_width=True, hide_index=True)

    st.markdown("""
    **Critical Design Elements:**

    1. **Network Segmentation**
       - Life safety systems on dedicated VLAN
       - Air-gapped from general IT network
       - Dedicated firewall rules

    2. **Redundancy**
       - Dual BBMDs per building (primary/backup)
       - Redundant fiber paths
       - Automatic failover configuration

    3. **Monitoring**
       - 24/7 network monitoring
       - Alert on any broadcast anomaly
       - Automated backup of configurations

    4. **Compliance**
       - Network access logs retained 7 years
       - BACnet traffic encrypted where possible
       - Regular security audits
    """)

# Scenario 4: Multi-Site VPN
elif selected_scenario == "🌐 Multi-Site VPN Network":
    st.markdown("---")
    st.header("🌐 Scenario: Multi-Site VPN Network")

    st.markdown("""
    **Background:**
    Corporate portfolio management company monitors 30 office buildings across the country.
    Each building has local BACnet network with edge controller.
    Central NOC provides 24/7 monitoring and optimization.
    """)

    st.subheader("The NAT Problem")

    st.markdown("""
    <div class="problem-box">
    <h4>❌ Problem: Many sites use same private IP range</h4>

    **Common Scenario:**
    - Site A: 192.168.1.0/24
    - Site B: 192.168.1.0/24  ← CONFLICT!
    - Site C: 192.168.1.0/24  ← CONFLICT!

    **Why it happens:**
    - Default router configuration
    - Local integrator didn't coordinate
    - Each site built independently

    **Impact:**
    - VPN connections conflict
    - Wrong building responds to commands
    - Can't distinguish between sites
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Traditional Solution: NAT")

    st.markdown("""
    **1:1 NAT Mapping:**

    | Site | Local Network | VPN Network | NAT Device |
    |------|---------------|-------------|------------|
    | A | 192.168.1.0/24 | 10.1.0.0/24 | Tosibox/VPN |
    | B | 192.168.1.0/24 | 10.2.0.0/24 | Tosibox/VPN |
    | C | 192.168.1.0/24 | 10.3.0.0/24 | Tosibox/VPN |
    """)

    st.markdown("""
    <div class="problem-box">
    <h4>❌ Problem: NAT breaks BACnet broadcasts</h4>

    **Why broadcasts fail through NAT:**
    1. Device sends Who-Is to 192.168.1.255 (local broadcast)
    2. NAT sees destination as 192.168.1.255
    3. NAT translates to... 10.1.0.255? No mapping for broadcast!
    4. Broadcast is dropped or sent to wrong address
    5. Remote monitoring system never receives Who-Is
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Modern Solution: Edge Devices")

    st.markdown("""
    <div class="solution-box">
    <h4>✅ Solution: Edge Controller Architecture</h4>

    **How it works:**
    1. Edge controller (JACE, Niagara, etc.) on site's local network
    2. Edge discovers all local BACnet devices (Layer 2 broadcasts work!)
    3. Edge stores device data in internal database
    4. Edge exposes data via HTTPS API to cloud/NOC
    5. Central system reads from edge API, not direct BACnet

    **Benefits:**
    - No NAT issues (HTTPS works through NAT)
    - No IP conflicts (edge uses API, not BACnet routing)
    - Better security (firewall-friendly)
    - Local autonomy (edge continues if WAN fails)
    - Reduced bandwidth (edge aggregates data)
    </div>
    """, unsafe_allow_html=True)

# Scenario 5: Troubleshooting Discovery
elif selected_scenario == "⚠️ Troubleshooting: Discovery Failure":
    st.markdown("---")
    st.header("⚠️ Troubleshooting: BACnet Discovery Failure")

    st.markdown("""
    **Symptom:** Management system can't discover BACnet devices

    **Interactive Troubleshooting Guide:**
    """)

    # Troubleshooting flowchart
    st.subheader("Step 1: Verify Network Connectivity")

    check1 = st.checkbox("Can you ping the device's IP address?")

    if check1:
        st.success("✅ Network layer connectivity is working")

        st.subheader("Step 2: Check Subnet Configuration")

        mgmt_ip = st.text_input("Management System IP", value="192.168.1.10")
        mgmt_subnet = st.text_input("Management System Subnet", value="192.168.1.0/24")
        device_ip = st.text_input("Device IP", value="10.0.2.50")

        if st.button("Check Subnet Match"):
            from ace_subnet_playground.subnet_calcs import is_ip_in_subnet

            mgmt_in_subnet = is_ip_in_subnet(mgmt_ip, mgmt_subnet)
            device_in_subnet = is_ip_in_subnet(device_ip, mgmt_subnet)

            if device_in_subnet:
                st.success("✅ Device is on same subnet - should work!")
                st.info("**Next Check:** Verify BACnet port 47808 is open")
            else:
                st.error("❌ Device is on different subnet!")
                st.warning("""
                **Problem Identified:** Cross-subnet communication

                **Solutions:**
                1. Configure BBMD on both subnets
                2. **Add symmetric BDT entries**: BBMD-A lists BBMD-B, BBMD-B lists BBMD-A
                3. Verify no firewall blocking UDP 47808
                4. Remember: BDT entries are directional, both sides must be configured!
                """)
    else:
        st.error("❌ No ping response - fix network connectivity first!")
        st.info("""
        **Common causes:**
        - Wrong IP address
        - Device powered off
        - Network cable unplugged
        - Firewall blocking ICMP
        - Wrong VLAN assignment
        """)

# Scenario 6: IP Conflicts
elif selected_scenario == "⚠️ Troubleshooting: IP Conflicts":
    st.markdown("---")
    st.header("⚠️ Troubleshooting: IP Address Conflicts")

    st.markdown("""
    **Symptom:** Device intermittently responds or responds with wrong data

    **Common Cause:** Multiple devices with same IP address
    """)

    st.subheader("IP Conflict Detector")

    st.markdown("Enter device IPs found in your network discovery:")

    devices_input = st.text_area(
        "Device IPs (one per line)",
        value="192.168.1.10\n192.168.1.20\n192.168.1.10\n192.168.1.30\n192.168.1.20",
        height=150
    )

    if st.button("Check for Conflicts", type="primary"):
        ips = [line.strip() for line in devices_input.split('\n') if line.strip()]

        # Find duplicates
        duplicates = {}
        for ip in set(ips):
            count = ips.count(ip)
            if count > 1:
                duplicates[ip] = count

        if duplicates:
            st.error(f"❌ **Conflicts Found!**")

            for ip, count in duplicates.items():
                st.markdown(f"""
                <div class="problem-box">
                <strong>{ip}</strong> appears {count} times!

                **Impact:**
                - Random device responds to requests
                - Data from wrong device
                - Discovery confusion
                - ARP cache poisoning

                **Solution:**
                1. Identify all devices with this IP (check MAC addresses)
                2. Assign unique IPs to each device
                3. Update device configurations
                4. Clear ARP caches: `arp -d` or reboot switches
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success(f"✅ No conflicts! All {len(ips)} IP addresses are unique.")

# Best Practices Summary
st.markdown("---")
st.header("✅ BACnet Network Design Best Practices")

best_practices = [
    {
        "Category": "IP Addressing",
        "Best Practice": "Use unique /24 subnets per floor/building",
        "Why": "Clear segmentation, easy troubleshooting, 254 devices per subnet"
    },
    {
        "Category": "Device Instances",
        "Best Practice": "Group by type: VAVs=1000-1999, AHUs=2000-2999",
        "Why": "Easy identification, scalable, consistent across sites"
    },
    {
        "Category": "Network Numbers",
        "Best Practice": "Match to subnet third octet: 10.0.X.0/24 → Network X000",
        "Why": "Intuitive mapping, prevents duplicates, easy documentation"
    },
    {
        "Category": "BBMD Placement",
        "Best Practice": "One BBMD per subnet, symmetric BDT entries (each lists all others)",
        "Why": "Full mesh connectivity, bidirectional discovery, no single point of failure"
    },
    {
        "Category": "Broadcast Control",
        "Best Practice": "Enable storm control: 500 pps limit",
        "Why": "Prevents broadcast storms from taking down network"
    },
    {
        "Category": "Monitoring",
        "Best Practice": "Track broadcast rate, CPU, bandwidth continuously",
        "Why": "Early warning of problems, historical baseline"
    },
    {
        "Category": "Documentation",
        "Best Practice": "Maintain network diagram with all IPs, instances, BBMDs",
        "Why": "Essential for troubleshooting, adds, moves, changes"
    },
]

df_best = pd.DataFrame(best_practices)
st.dataframe(df_best, use_container_width=True, hide_index=True)

# Key Takeaways
st.markdown("---")
st.header("🎓 Key Takeaways")

st.markdown("""
<div style="background-color: #E8F4F8; color: #1a1a1a; padding: 1.5rem; border-radius: 8px; border: 2px solid #3498DB;">
    <h4>Critical Points for Real-World Networks:</h4>
    <ol>
        <li><strong>Plan IP Addressing</strong>: Unique subnets prevent future conflicts</li>
        <li><strong>BBMD is Essential</strong>: Required for multi-subnet BACnet networks</li>
        <li><strong>Avoid NAT for BACnet</strong>: Use edge device architecture instead</li>
        <li><strong>Monitor Continuously</strong>: Broadcast storms can appear suddenly</li>
        <li><strong>Document Everything</strong>: Network diagrams save hours of troubleshooting</li>
        <li><strong>Test Discovery</strong>: Verify cross-subnet Who-Is/I-Am works</li>
        <li><strong>Implement Redundancy</strong>: For critical systems, plan for failures</li>
    </ol>
</div>
""", unsafe_allow_html=True)

# Completion
st.markdown("---")
st.success("""
🎉 **Congratulations!**

You've completed all 6 modules of the BACnet Subnet & BBMD Academy!

You now have the knowledge to:
- Design robust BACnet networks
- Configure BBMDs for multi-subnet communication
- Troubleshoot common network issues
- Prevent and mitigate broadcast storms
- Apply best practices to real-world scenarios

**Keep learning and apply these concepts to your projects!**
""")

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("⬅️ Back to Broadcast Storms", use_container_width=True):
        st.switch_page("pages/5_Broadcast_Storms.py")
with col3:
    if st.button("🏠 Return to Home", use_container_width=True, type="primary"):
        st.switch_page("app.py")
