"""
BACnet Subnet & BBMD Educational Academy
Entry point using st.navigation for proper page naming
"""

import streamlit as st

# Define pages with custom names
overview_page = st.Page("overview.py", title="Overview", icon="🌐", default=True)
subnet_basics = st.Page("pages/1_Subnet_Basics.py", title="Subnet Basics", icon="🔢")
binary_ops = st.Page("pages/2_Binary_Operations.py", title="Binary Operations", icon="⚙️")
bacnet_overview = st.Page("pages/3_BACnet_Overview.py", title="BACnet Overview", icon="🏢")
bbmd_arch = st.Page("pages/4_BBMD_Architecture.py", title="BBMD Architecture", icon="🔀")
broadcast_storms = st.Page("pages/5_Broadcast_Storms.py", title="Broadcast Storms", icon="⚡")
network_scenarios = st.Page("pages/6_Network_Scenarios.py", title="Network Scenarios", icon="🗺️")

# Create navigation
pg = st.navigation([
    overview_page,
    subnet_basics,
    binary_ops,
    bacnet_overview,
    bbmd_arch,
    broadcast_storms,
    network_scenarios
])

# Run the selected page
pg.run()
