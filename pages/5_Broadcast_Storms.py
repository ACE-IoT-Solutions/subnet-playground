"""
Module 5: Broadcast Storms
Interactive broadcast storm simulation and visualization
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import networkx as nx
import time
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Page config
st.set_page_config(
    page_title="Broadcast Storms | BACnet Academy",
    page_icon="⚡",
    layout="wide"
)

# Apply ACE IoT Solutions Brand
st.markdown(get_ace_brand_css(), unsafe_allow_html=True)
st.markdown("""
<style>
    .storm-warning {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-box {
        background-color: #F8F9FA; color: #1a1a1a;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #E74C3C;
        margin: 0.5rem 0;
    }
    .safe-box {
        background-color: #E8F8F5; color: #1a1a1a;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #27AE60;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("⚡ Module 5: Broadcast Storms")
st.markdown("**Understand, visualize, and prevent broadcast storm catastrophes**")
st.markdown("---")

# Learning Objectives
with st.expander("🎯 Learning Objectives", expanded=False):
    st.markdown("""
    By the end of this module, you will understand:
    - What broadcast storms are and why they occur
    - How network topology affects storm severity
    - Visualizing broadcast propagation in real-time
    - Detection methods and warning signs
    - Prevention and mitigation strategies
    """)

# Section 1: What is a Broadcast Storm?
st.header("1️⃣ What is a Broadcast Storm?")

st.markdown("""
<div class="storm-warning">
    <h3>⚡ Network Catastrophe</h3>
    <p>A <strong>broadcast storm</strong> occurs when broadcast packets multiply uncontrollably on a network, consuming all available bandwidth and CPU resources.</p>
    <p><strong>Result:</strong> Network becomes completely unusable, devices crash, systems fail</p>
    <p><strong>Severity:</strong> Can take down entire building automation systems in seconds</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Common Causes")
    st.markdown("""
    1. **BBMD Loops**
       - BDT entries create circular references
       - Broadcast bounces forever between BBMDs

    2. **Switch Loops**
       - Physical loop in switch connections
       - No Spanning Tree Protocol (STP)

    3. **Misconfigured Devices**
       - Device sending continuous broadcasts
       - Malfunctioning controller
       - No rate limiting

    4. **ARP Storms**
       - Duplicate IP addresses
       - Broadcast ARP requests multiplying
    """)

with col2:
    st.subheader("Warning Signs")
    st.markdown("""
    ⚠️ **Network slowing to a crawl**
    - Response times >10 seconds
    - Timeouts on all requests

    ⚠️ **High CPU usage on network devices**
    - Switches at 90-100% CPU
    - Devices overheating

    ⚠️ **Broadcast packet rate spiking**
    - Normal: <100 broadcasts/sec
    - Storm: >10,000 broadcasts/sec

    ⚠️ **Devices becoming unreachable**
    - Random disconnections
    - Services failing
    """)

# Section 2: Interactive Storm Simulator
st.markdown("---")
st.header("2️⃣ Interactive Broadcast Storm Simulator")

st.markdown("Build a network topology and watch broadcast propagation:")

# Initialize session state
if 'network_topology' not in st.session_state:
    st.session_state.network_topology = "normal"

# Topology selection
topology_col1, topology_col2 = st.columns([1, 2])

with topology_col1:
    st.subheader("Network Topology")

    topology = st.radio(
        "Select Network Type",
        ["Normal (Safe)", "BBMD Loop (Storm!)", "BBMD Correct (Safe)", "Triangle Loop (Storm!)", "Mesh Network"],
        key="topology_selector"
    )

    st.markdown("---")
    st.subheader("Storm Parameters")

    max_hops = st.slider("Max Broadcast Hops", 1, 20, 10, help="How many times can a broadcast be forwarded?")
    initial_devices = st.slider("Number of Devices", 3, 15, 8)

with topology_col2:
    st.subheader("Network Visualization")

    # Create network graph based on topology
    G = nx.Graph()
    node_subnets = {}  # Track which subnet each node belongs to
    subnet_colors = {
        "192.168.1.0/24": "#E8F4F8",
        "10.0.2.0/24": "#FEF5E7",
        "10.0.3.0/24": "#F4ECF7"
    }

    if topology == "Normal (Safe)":
        # Linear topology - no loops
        st.session_state.network_topology = "normal"
        nodes = [f"Device{i}" for i in range(1, initial_devices + 1)]
        G.add_nodes_from(nodes)
        for i in range(len(nodes) - 1):
            G.add_edge(nodes[i], nodes[i+1])
        # All on same subnet
        for node in nodes:
            node_subnets[node] = "192.168.1.0/24"

    elif topology == "BBMD Loop (Storm!)":
        # Multiple BBMDs on same subnet - MISCONFIGURED (creates ping-pong loop)
        st.session_state.network_topology = "loop"
        nodes = ["BBMD-A\n192.168.1.1", "BBMD-B\n192.168.1.2", "BBMD-C\n10.0.2.1",
                 "Dev-1\n192.168.1.10", "Dev-2\n192.168.1.11", "Dev-3\n10.0.2.10"]
        G.add_nodes_from(nodes)
        # BBMD-A and BBMD-B are on SAME subnet (192.168.1.0/24) - BAD!
        # Both have BDT entries pointing to BBMD-C
        # BBMD-C has entry pointing back to one of them
        G.add_edges_from([("BBMD-A\n192.168.1.1", "BBMD-C\n10.0.2.1"),
                         ("BBMD-B\n192.168.1.2", "BBMD-C\n10.0.2.1")])
        # Show that BBMD-A and BBMD-B are on same subnet (local connection)
        G.add_edge("BBMD-A\n192.168.1.1", "BBMD-B\n192.168.1.2")
        # Add devices to their BBMDs
        G.add_edges_from([("BBMD-A\n192.168.1.1", "Dev-1\n192.168.1.10"),
                         ("BBMD-B\n192.168.1.2", "Dev-2\n192.168.1.11"),
                         ("BBMD-C\n10.0.2.1", "Dev-3\n10.0.2.10")])
        # Assign subnets - NOTE: BBMD-A and BBMD-B share same subnet!
        node_subnets["BBMD-A\n192.168.1.1"] = "192.168.1.0/24"
        node_subnets["BBMD-B\n192.168.1.2"] = "192.168.1.0/24"  # DUPLICATE SUBNET!
        node_subnets["Dev-1\n192.168.1.10"] = "192.168.1.0/24"
        node_subnets["Dev-2\n192.168.1.11"] = "192.168.1.0/24"
        node_subnets["BBMD-C\n10.0.2.1"] = "10.0.2.0/24"
        node_subnets["Dev-3\n10.0.2.10"] = "10.0.2.0/24"

    elif topology == "BBMD Correct (Safe)":
        # Properly configured BBMD network - NO LOOP
        st.session_state.network_topology = "bbmd_correct"
        nodes = ["BBMD-A\n192.168.1.1", "BBMD-B\n10.0.2.1",
                 "Dev-A1\n192.168.1.10", "Dev-A2\n192.168.1.11",
                 "Dev-B1\n10.0.2.10", "Dev-B2\n10.0.2.11"]
        G.add_nodes_from(nodes)
        # BBMDs connected (but no circular loop!)
        G.add_edge("BBMD-A\n192.168.1.1", "BBMD-B\n10.0.2.1")
        # Devices connected to their BBMDs
        G.add_edges_from([("BBMD-A\n192.168.1.1", "Dev-A1\n192.168.1.10"),
                         ("BBMD-A\n192.168.1.1", "Dev-A2\n192.168.1.11"),
                         ("BBMD-B\n10.0.2.1", "Dev-B1\n10.0.2.10"),
                         ("BBMD-B\n10.0.2.1", "Dev-B2\n10.0.2.11")])
        # Assign subnets
        node_subnets["BBMD-A\n192.168.1.1"] = "192.168.1.0/24"
        node_subnets["Dev-A1\n192.168.1.10"] = "192.168.1.0/24"
        node_subnets["Dev-A2\n192.168.1.11"] = "192.168.1.0/24"
        node_subnets["BBMD-B\n10.0.2.1"] = "10.0.2.0/24"
        node_subnets["Dev-B1\n10.0.2.10"] = "10.0.2.0/24"
        node_subnets["Dev-B2\n10.0.2.11"] = "10.0.2.0/24"

    elif topology == "Triangle Loop (Storm!)":
        # Triangle loop with devices
        st.session_state.network_topology = "triangle"
        nodes = ["Switch-A", "Switch-B", "Switch-C"] + [f"Device{i}" for i in range(1, 6)]
        G.add_nodes_from(nodes)
        # Create triangle loop
        G.add_edges_from([("Switch-A", "Switch-B"), ("Switch-B", "Switch-C"), ("Switch-C", "Switch-A")])
        # Add devices
        G.add_edges_from([("Switch-A", "Device1"), ("Switch-A", "Device2"),
                         ("Switch-B", "Device3"), ("Switch-B", "Device4"),
                         ("Switch-C", "Device5")])
        # All on same subnet
        for node in nodes:
            node_subnets[node] = "192.168.1.0/24"

    else:  # Mesh Network
        st.session_state.network_topology = "mesh"
        nodes = [f"Device{i}" for i in range(1, min(initial_devices, 8) + 1)]
        G.add_nodes_from(nodes)
        # Create mesh - each node connected to 2-3 others
        for i, node in enumerate(nodes):
            for j in range(i+1, min(i+3, len(nodes))):
                G.add_edge(node, nodes[j])
        # All on same subnet
        for node in nodes:
            node_subnets[node] = "192.168.1.0/24"

    # Create network visualization with deterministic layout
    # Choose layout based on topology for clearer visualization
    if st.session_state.network_topology in ["bbmd_correct", "bbmd_loop"]:
        # Use bipartite layout to show subnet separation
        # Separate BBMDs from regular devices, and organize by subnet
        pos = {}
        bbmds = [n for n in G.nodes() if 'BBMD' in n]
        devices = [n for n in G.nodes() if 'BBMD' not in n]

        # Position BBMDs in center
        for i, bbmd in enumerate(bbmds):
            pos[bbmd] = (i * 2, 0)

        # Position devices around BBMDs based on subnet
        subnet_positions = {
            "192.168.1.0/24": -1,
            "10.0.2.0/24": 1,
            "10.0.3.0/24": 3
        }

        device_count_per_subnet = {}
        for device in devices:
            subnet = node_subnets.get(device, "192.168.1.0/24")
            y_base = subnet_positions.get(subnet, 0)
            count = device_count_per_subnet.get(subnet, 0)
            pos[device] = (count * 1.5, y_base)
            device_count_per_subnet[subnet] = count + 1

    elif st.session_state.network_topology == "loop":
        # Circular layout to emphasize the loop
        pos = nx.circular_layout(G)

    elif st.session_state.network_topology == "triangle":
        # Shell layout for triangle
        pos = nx.shell_layout(G)

    elif st.session_state.network_topology == "mesh":
        # Kamada-Kawai for mesh (force-directed but deterministic)
        pos = nx.kamada_kawai_layout(G)

    else:
        # Normal network - hierarchical layout
        pos = nx.spring_layout(G, k=2, iterations=50, seed=42)

    # Extract coordinates
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    node_x = [pos[node][0] for node in G.nodes()]
    node_y = [pos[node][1] for node in G.nodes()]
    node_text = list(G.nodes())

    # Create figure
    fig = go.Figure()

    # Add edges
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='#888'),
        hoverinfo='none',
        mode='lines',
        showlegend=False
    ))

    # Add nodes with subnet-based coloring
    node_colors = []
    node_sizes = []
    hover_texts = []

    for node in G.nodes():
        # Color based on device type and subnet
        if 'BBMD' in node:
            node_colors.append('#E74C3C')  # Red for BBMDs
            node_sizes.append(30)
        elif 'Switch' in node:
            node_colors.append('#E67E22')  # Orange for switches
            node_sizes.append(25)
        else:
            # Color devices by subnet
            subnet = node_subnets.get(node, "192.168.1.0/24")
            if "192.168.1" in subnet:
                node_colors.append('#4A90E2')  # Blue
            elif "10.0.2" in subnet:
                node_colors.append('#9B59B6')  # Purple
            elif "10.0.3" in subnet:
                node_colors.append('#1ABC9C')  # Teal
            else:
                node_colors.append('#95A5A6')  # Gray
            node_sizes.append(20)

        # Create hover text with subnet info
        subnet_info = node_subnets.get(node, "N/A")
        hover_texts.append(f"{node}<br>Subnet: {subnet_info}")

    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        hovertext=hover_texts,
        text=node_text,
        textposition="top center",
        marker=dict(
            size=node_sizes,
            color=node_colors,
            line=dict(width=2, color='white')
        ),
        showlegend=False
    ))

    fig.update_layout(
        title=f"Network Topology: {topology}",
        showlegend=False,
        hovermode='closest',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

    # Show subnet legend
    if node_subnets:
        unique_subnets = list(set(node_subnets.values()))
        if len(unique_subnets) > 1:
            st.markdown("**Subnet Legend:**")
            legend_cols = st.columns(len(unique_subnets))
            subnet_color_map = {
                "192.168.1.0/24": ("🔵 Blue", "#4A90E2"),
                "10.0.2.0/24": ("🟣 Purple", "#9B59B6"),
                "10.0.3.0/24": ("🔷 Teal", "#1ABC9C")
            }
            for i, subnet in enumerate(sorted(unique_subnets)):
                with legend_cols[i]:
                    color_info = subnet_color_map.get(subnet, ("⚪ Gray", "#95A5A6"))
                    st.markdown(f"{color_info[0]}: `{subnet}`")

    # Scenario description boxes
    st.markdown("---")
    st.markdown("**📋 Scenario Description:**")

    if topology == "Normal (Safe)":
        st.info("""
        **Linear Network Topology (Safe)**

        **Configuration:**
        - Devices connected in a chain (Device1 → Device2 → Device3...)
        - All devices on same subnet (192.168.1.0/24)
        - No redundant paths or loops

        **Real-World Example:**
        A small office with devices daisy-chained via Ethernet switches in a row. Each device connects to the next one down the line.

        **Why It's Safe:**
        - Broadcasts propagate linearly along the chain
        - Each device receives the broadcast once
        - No loops = no packet multiplication
        - Hop count doesn't affect total broadcast count

        **Result:** ✅ Safe network configuration
        """)

    elif topology == "BBMD Loop (Storm!)":
        st.error("""
        **BBMD Loop - Multiple BBMDs on Same Subnet (MISCONFIGURED - CREATES STORM!)**

        **Configuration:**
        - Three BBMDs, with TWO on the SAME subnet:
          - BBMD-A: 192.168.1.0/24 (blue subnet) ⚠️
          - BBMD-B: 192.168.1.0/24 (blue subnet) ⚠️ DUPLICATE!
          - BBMD-C: 10.0.2.0/24 (purple subnet)
        - BBMD-A's BDT: → BBMD-C
        - BBMD-B's BDT: → BBMD-C
        - BBMD-C's BDT: → BBMD-A (or BBMD-B)

        **Real-World Example:**
        Multi-building campus where two BBMDs were accidentally placed on the same subnet:
        - Building A has BBMD-A on 192.168.1.0/24
        - Building B has BBMD-B on 192.168.1.0/24 (same subnet! - mistake!)
        - Remote site has BBMD-C on 10.0.2.0/24
        - Both BBMD-A and BBMD-B have BBMD-C in their BDT

        **Why It Causes a Storm:**
        1. Device on 192.168.1.0/24 sends Who-Is broadcast
        2. **Both BBMD-A and BBMD-B receive it** (same subnet!)
        3. BBMD-A forwards to BBMD-C
        4. BBMD-B also forwards to BBMD-C (duplicate!)
        5. BBMD-C forwards to 192.168.1.0/24
        6. Both BBMD-A and BBMD-B receive it AGAIN
        7. Both forward to BBMD-C AGAIN
        8. BBMD-C forwards back AGAIN
        9. Infinite loop - broadcasts multiply forever!

        **Key Problem:**
        - BBMDs won't forward back to the source BBMD they received from
        - BUT when multiple BBMDs exist on the SAME subnet with BDT entries
        - Each BBMD keeps forwarding what the OTHER BBMD sent
        - Creates ping-pong effect between the BBMDs

        **Result:** 🔴 BROADCAST STORM - Never put multiple BBMDs on same subnet with BDT entries!
        """)

    elif topology == "BBMD Correct (Safe)":
        st.success("""
        **Properly Configured BBMD Network (Safe)**

        **Configuration:**
        - Two BBMDs connecting two subnets:
          - BBMD-A: 192.168.1.0/24 (blue subnet)
          - BBMD-B: 10.0.2.0/24 (purple subnet)
        - **BBMD-A has BBMD-B in its BDT** (A forwards to B)
        - **BBMD-B has BBMD-A in its BDT** (B forwards to A)
        - **Symmetric BDT entries required** - forwarding is NOT automatic in both directions!

        **Real-World Example:**
        Two-building campus with correct BBMD configuration:
        - Building A devices can discover Building B devices
        - Building B devices can discover Building A devices
        - Each BBMD explicitly configured to forward to the other
        - No retransmission loops because each subnet has only ONE BBMD

        **Why It's Safe (Discovery from Building A):**
        1. Device in Building A sends Who-Is broadcast to 192.168.1.255
        2. BBMD-A receives it, checks its BDT, forwards to BBMD-B
        3. BBMD-B receives unicast from BBMD-A, broadcasts on 10.0.2.0/24
        4. Devices on subnet B receive broadcast and respond
        5. BBMD-B does NOT forward back to BBMD-A (not in same message path)

        **Why It's Safe (Discovery from Building B):**
        1. Device in Building B sends Who-Is broadcast to 10.0.2.255
        2. BBMD-B receives it, checks its BDT, forwards to BBMD-A
        3. BBMD-A receives unicast from BBMD-B, broadcasts on 192.168.1.0/24
        4. Devices on subnet A receive broadcast and respond

        **Critical Requirement - Symmetric BDT Entries:**
        - **Each BBMD must have the other in its BDT**
        - BDT entries are directional - not bidirectional by default
        - BBMD-A having B in BDT ≠ BBMD-B automatically forwarding to A
        - Both entries required for full bidirectional discovery

        **Key Difference from Loop:**
        - Only ONE BBMD per subnet (no ping-pong between multiple BBMDs)
        - BBMDs track forwarding to prevent loops
        - Symmetric BDT entries enable bidirectional communication

        **Result:** ✅ Cross-subnet BACnet discovery works safely in both directions!
        """)

    elif topology == "Triangle Loop (Storm!)":
        st.error("""
        **Triangle Switch Loop (CREATES STORM!)**

        **Configuration:**
        - Three switches connected in a triangle:
          - Switch-A ↔ Switch-B
          - Switch-B ↔ Switch-C
          - Switch-C ↔ Switch-A (closes the loop!)
        - Devices connected to each switch
        - All on same subnet (192.168.1.0/24)
        - **No Spanning Tree Protocol (STP)** enabled

        **Real-World Example:**
        Network technician creates redundancy for reliability:
        - Connects three switches in a triangle for "backup paths"
        - Forgets to enable Spanning Tree Protocol
        - The redundancy intended to help instead creates a disaster

        **Why It Causes a Storm:**
        1. Any device sends a broadcast
        2. Switch receives it and forwards to its TWO neighbor switches
        3. Each neighbor forwards to their TWO neighbors
        4. Broadcast loops around the triangle indefinitely
        5. Each pass multiplies the packets
        6. Network saturates in seconds

        **Prevention:**
        Enable **Spanning Tree Protocol (STP)** which would:
        - Detect the loop
        - Block one of the connections logically
        - Maintain redundancy without the loop

        **Result:** 🔴 BROADCAST STORM - Enable STP immediately!
        """)

    else:  # Mesh Network
        st.error("""
        **Mesh Network Without STP (CREATES STORM!)**

        **Configuration:**
        - Multiple devices/switches (3-8 devices)
        - Each device connected to 2-3 neighbors
        - Creates a web of interconnected paths
        - All on same subnet (192.168.1.0/24)
        - **No Spanning Tree Protocol (STP)** enabled

        **Real-World Example:**
        Data center or large office with many interconnected switches:
        - Switch-A connects to Switch-B, Switch-C
        - Switch-B connects to Switch-A, Switch-C, Switch-D
        - Switch-C connects to Switch-A, Switch-B, Switch-D
        - Switch-D connects to Switch-B, Switch-C
        - Multiple redundant paths between any two points

        **Why It Causes a Storm:**
        1. Broadcast enters the mesh at any point
        2. Forwarded to multiple neighbors simultaneously
        3. Each neighbor forwards to their multiple neighbors
        4. Broadcast multiplies across ALL redundant paths
        5. Multiple loops = exponential multiplication
        6. More interconnected = faster catastrophic growth

        **The Irony:**
        - Mesh topology created for **reliability** (redundant paths)
        - Without STP, redundancy becomes network's worst enemy
        - More connections = worse storm

        **Prevention:**
        Enable **Spanning Tree Protocol (STP)** which would:
        - Calculate loop-free topology
        - Block redundant paths logically
        - Maintain physical redundancy for failover
        - Allow mesh benefits without broadcast storms

        **Result:** 🔴 SEVERE BROADCAST STORM - Multiple loops amplify the disaster!
        """)


# Storm simulation - automatically calculate and display
st.markdown("---")
st.subheader("Broadcast Propagation Analysis")

# Simulate broadcast propagation
broadcasts_per_hop = {}
broadcast_count = 0

if st.session_state.network_topology in ["normal", "bbmd_correct"]:
    # Normal network or correctly configured BBMD - broadcasts don't multiply
    # Each device receives the broadcast once, regardless of hop count
    # BBMDs forward once to configured peers, no retransmission loops
    total_broadcasts = len(G.nodes())
    for hop in range(max_hops):
        broadcasts_per_hop[hop] = total_broadcasts
    broadcast_count = total_broadcasts
elif st.session_state.network_topology in ["loop", "triangle", "mesh"]:
    # Storm network - exponential growth
    broadcasts_per_hop[0] = 1
    for hop in range(1, max_hops):
        # Each device re-broadcasts to all neighbors
        broadcasts_per_hop[hop] = broadcasts_per_hop[hop-1] * (len(list(G.edges())) // len(G.nodes()) + 1)
        broadcast_count += broadcasts_per_hop[hop]

        # Cap at realistic maximum
        if broadcasts_per_hop[hop] > 1000000:
            broadcasts_per_hop[hop] = 1000000
            break

# Create timeline chart
hops = list(broadcasts_per_hop.keys())
counts = list(broadcasts_per_hop.values())

fig_timeline = go.Figure()
fig_timeline.add_trace(go.Scatter(
    x=hops,
    y=counts,
    mode='lines+markers',
    line=dict(color='#E74C3C' if st.session_state.network_topology in ["loop", "triangle", "mesh"] else '#27AE60', width=3),
    marker=dict(size=8),
    fill='tozeroy',
    fillcolor='rgba(231, 76, 60, 0.3)' if st.session_state.network_topology in ["loop", "triangle", "mesh"] else 'rgba(39, 174, 96, 0.3)'
))

fig_timeline.update_layout(
    title="Broadcast Packet Count Over Time",
    xaxis_title="Hop Number",
    yaxis_title="Broadcast Packets",
    yaxis_type="log" if st.session_state.network_topology in ["loop", "triangle", "mesh"] else "linear",
    height=300
)

st.plotly_chart(fig_timeline, use_container_width=True)

# Show current metrics
metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    st.metric("Total Broadcasts", f"{broadcast_count:,}")

with metric_col2:
    bandwidth = broadcast_count * 64  # bytes
    st.metric("Bandwidth Used", f"{bandwidth/1024:.1f} KB")

with metric_col3:
    packets_per_sec = broadcasts_per_hop.get(len(broadcasts_per_hop)-1, 0) * 10
    st.metric("Packets/Sec", f"{packets_per_sec:,}")

with metric_col4:
    if st.session_state.network_topology in ["normal", "bbmd_correct"]:
        severity = "🟢 Safe"
    else:
        severity = "🔴 CRITICAL"
    st.metric("Severity", severity)

# Storm warning or success message
if st.session_state.network_topology == "bbmd_correct":
    st.success(f"""
    ✅ **PROPERLY CONFIGURED BBMD NETWORK**

    This network has BBMDs connecting two subnets WITHOUT creating a loop.

    **Why it's safe:**
    - BBMD-A forwards to BBMD-B (one direction)
    - BBMD-B can reply back to BBMD-A
    - No circular BDT entries (no A→B→C→A loop)
    - Broadcasts propagate but don't multiply

    **Result:** Cross-subnet discovery works safely!
    """)
elif st.session_state.network_topology != "normal":
    st.error(f"""
    ⚡ **BROADCAST STORM DETECTED!**

    This network topology creates a broadcast storm with exponential packet growth.

    **Impact:**
    - Network bandwidth saturated
    - All devices experiencing high CPU load
    - Normal traffic blocked
    - System failure imminent

    **Action Required:** Break the loop or implement STP!
    """)

# Section 3: Detection Methods
st.markdown("---")
st.header("3️⃣ Storm Detection Methods")

detection_methods = [
    {
        "Method": "Packet Rate Monitoring",
        "Threshold": ">1000 broadcasts/sec",
        "Tool": "Network analyzer, SNMP monitoring",
        "Pros": "Real-time detection",
        "Cons": "Need baseline for comparison"
    },
    {
        "Method": "CPU Usage Monitoring",
        "Threshold": "Switch CPU >80%",
        "Tool": "SNMP, switch management",
        "Pros": "Early warning sign",
        "Cons": "Can have other causes"
    },
    {
        "Method": "Bandwidth Monitoring",
        "Threshold": ">70% link utilization",
        "Tool": "NetFlow, sFlow analysis",
        "Pros": "Shows network impact",
        "Cons": "Delayed detection"
    },
    {
        "Method": "Spanning Tree Events",
        "Threshold": "STP topology changes",
        "Tool": "Syslog, switch logs",
        "Pros": "Prevents many storms",
        "Cons": "Only detects loop-based"
    }
]

df_detection = pd.DataFrame(detection_methods)
st.dataframe(df_detection, use_container_width=True, hide_index=True)

# Section 4: Prevention & Mitigation
st.markdown("---")
st.header("4️⃣ Prevention & Mitigation Strategies")

tab1, tab2, tab3, tab4 = st.tabs(["Prevention", "Detection", "Mitigation", "Recovery"])

with tab1:
    st.markdown("""
    <div class="safe-box">
    <h4>🛡️ Prevention Strategies</h4>

    <strong>1. Spanning Tree Protocol (STP)</strong>
    - Enable on all switches
    - Automatically blocks loop-creating ports
    - Essential for redundant networks

    <strong>2. BBMD Configuration Validation</strong>
    - Review BDT entries carefully
    - Never create circular BDT references
    - Document BBMD topology

    <strong>3. Rate Limiting</strong>
    - Configure broadcast storm control on switches
    - Limit broadcasts to <500 pps per port
    - Drop excess broadcasts

    <strong>4. Network Segmentation</strong>
    - Use VLANs to isolate broadcast domains
    - Limit devices per subnet (<254)
    - Separate critical systems

    <strong>5. Monitoring & Alerts</strong>
    - Monitor broadcast packet rates
    - Alert on anomalies
    - Track switch CPU usage
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown("""
    **Early Detection Indicators:**

    📊 **Monitoring Tools:**
    - PRTG Network Monitor
    - SolarWinds NPM
    - Wireshark for packet capture
    - Native switch statistics

    📈 **Key Metrics:**
    ```
    Normal Network:
    - Broadcast rate: 10-100 packets/sec
    - CPU usage: <20%
    - Link utilization: <50%

    Storm Warning:
    - Broadcast rate: >500 packets/sec ⚠️
    - CPU usage: >60% ⚠️
    - Link utilization: >70% ⚠️

    Active Storm:
    - Broadcast rate: >5000 packets/sec 🔴
    - CPU usage: >90% 🔴
    - Link utilization: >95% 🔴
    ```
    """)

with tab3:
    st.markdown("""
    **Immediate Mitigation Steps:**

    **1. Identify Storm Source** (30 seconds)
    - Check switch statistics for ports with high broadcast rates
    - Look for port with highest TX broadcast counter

    **2. Isolate Storm** (1 minute)
    - Shutdown offending switch port: `shutdown interface GigabitEthernet1/0/X`
    - Or physically unplug cable
    - Storm should stop immediately

    **3. Verify Resolution** (30 seconds)
    - Check broadcast rates drop to normal
    - Verify network responsiveness returns
    - Confirm devices are accessible

    **4. Root Cause Analysis** (5-10 minutes)
    - What device was on that port?
    - BBMD with bad BDT?
    - Switch loop?
    - Malfunctioning device?

    **5. Fix and Restore** (varies)
    - Correct the configuration issue
    - Test before bringing port back up
    - Re-enable port and monitor
    """)

with tab4:
    st.markdown("""
    **Recovery Process:**

    **Phase 1: Emergency Response** (5 min)
    - Stop the storm (isolate source)
    - Verify network stability
    - Document the incident

    **Phase 2: Assessment** (15 min)
    - Check for device damage
    - Verify all systems operational
    - Review logs for affected devices

    **Phase 3: Permanent Fix** (varies)
    - Correct BACnet configuration
    - Enable STP if missing
    - Update network documentation
    - Implement monitoring

    **Phase 4: Prevention** (ongoing)
    - Review similar configurations
    - Add monitoring alerts
    - Train staff on storm prevention
    - Schedule regular audits
    """)

# Key Takeaways
st.markdown("---")
st.header("🎓 Key Takeaways")

st.markdown("""
<div style="background-color: #FFEBEE; color: #1a1a1a; padding: 1.5rem; border-radius: 8px; border: 2px solid #E74C3C;">
    <h4>Critical Points to Remember:</h4>
    <ol>
        <li><strong>Broadcast Storms are Catastrophic</strong>: Can take down entire networks in seconds</li>
        <li><strong>BBMD Loops</strong>: Most common cause in BACnet networks - verify BDT carefully</li>
        <li><strong>STP is Essential</strong>: Spanning Tree Protocol prevents switch loops</li>
        <li><strong>Monitor Continuously</strong>: Track broadcast rates, CPU, bandwidth</li>
        <li><strong>Rate Limiting</strong>: Configure broadcast storm control on all switches</li>
        <li><strong>Quick Response</strong>: Shutdown storm source immediately, investigate later</li>
    </ol>
</div>
""", unsafe_allow_html=True)

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("⬅️ Back to BBMD", use_container_width=True):
        st.switch_page("pages/4_BBMD_Architecture.py")
with col3:
    if st.button("Network Scenarios ➡️", use_container_width=True, type="primary"):
        st.switch_page("pages/6_Network_Scenarios.py")
