# 🌐 BACnet Subnet & BBMD Educational Academy

An interactive Streamlit application for learning subnet architecture, BACnet protocol concepts, and BBMD (BACnet Broadcast Management Device) operations with a focus on building automation systems.

## 🎯 Overview

This educational platform provides hands-on learning through:
- **Interactive subnet calculators** with real-time visualizations
- **Binary operation tutorials** showing how devices process packets
- **BACnet protocol demonstrations** for building automation
- **BBMD architecture** with interactive BDT/FDT builders
- **Broadcast storm simulations** with network topology visualizations
- **Real-world scenarios** and troubleshooting guides

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- uv package manager

### Installation

1. Sync dependencies with uv:
```bash
uv sync
```

2. Run the application:
```bash
uv run streamlit run streamlit_app.py
```

The application will open in your browser at `http://localhost:8501`

## 📚 Learning Modules

### ✅ Module 1: Subnet Basics 🔢
**Status: ✅ Complete**

- IP addressing fundamentals
- Subnet mask calculations with interactive CIDR slider
- Binary representation visualization
- Common subnet masks for BACnet networks
- Network class identification
- Practice exercises

### ✅ Module 2: Binary Operations ⚙️
**Status: ✅ Complete**

- Bitwise AND tutorial with truth table
- Interactive 8-bit AND calculator
- Packet processing simulation with step-by-step breakdown
- Network address calculation
- Visual explanation of why broadcasts don't cross routers
- BACnet Who-Is/I-Am examples

### ✅ Module 3: BACnet Overview 🏢
**Status: ✅ Complete**

- BACnet/IP protocol introduction
- Interactive Who-Is/I-Am discovery simulator
- Network numbering concepts
- Device instance management
- Device instance conflict checker
- Subnet configuration impact on BACnet

### ✅ Module 4: BBMD Architecture 🌉
**Status: ✅ Complete**

- BBMD functionality and purpose explained
- Interactive Broadcast Distribution Table (BDT) builder
- Foreign Device Table (FDT) management
- Message routing simulator across subnets
- Network topology visualization
- Step-by-step routing demonstrations

### ✅ Module 5: Broadcast Storms ⚡
**Status: ✅ Complete**

- Interactive network topology builder
- Real-time broadcast storm simulations
- Multiple topology scenarios (normal, loop, triangle, mesh)
- Storm detection and metrics visualization
- Prevention and mitigation strategies
- Recovery procedures

### ✅ Module 6: Network Scenarios 🗺️
**Status: ✅ Complete**

- Real-world BACnet configurations
- Multi-floor office building design
- Industrial campus networks
- Hospital critical infrastructure
- Multi-site VPN challenges and solutions
- Interactive troubleshooting guides
- IP conflict detection tools

## 🏗️ Project Structure

```
ace-subnet-playground/
├── streamlit_app.py                # ✅ Main entry point (navigation)
├── overview.py                          # ✅ Overview/landing page
├── pages/                          # ✅ All modules complete
│   ├── 1_Subnet_Basics.py         # ✅ Complete
│   ├── 2_Binary_Operations.py     # ✅ Complete
│   ├── 3_BACnet_Overview.py       # ✅ Complete
│   ├── 4_BBMD_Architecture.py     # ✅ Complete
│   ├── 5_Broadcast_Storms.py      # ✅ Complete
│   └── 6_Network_Scenarios.py     # ✅ Complete
├── src/
│   └── ace_subnet_playground/
│       ├── __init__.py             # ✅
│       └── subnet_calcs.py         # ✅ Core utilities
├── pyproject.toml                  # ✅ uv configuration
├── README.md                       # ✅ This file
└── QUICKSTART.md                   # ✅ Quick reference
```

## 🔧 Key Features (All Implemented!)

### Interactive Subnet Calculator
- Real-time CIDR slider (8-32 bits)
- Network/broadcast address calculation
- Usable IP range display with first/last addresses
- Binary representation with network/host bit highlighting
- Visual bar showing network vs host bit distribution
- Common subnet mask reference table
- Network class and private IP detection

### Packet Processing Simulator
- Interactive device configuration
- Packet destination input
- Step-by-step bitwise AND visualization
- Binary breakdown of all calculations
- Visual explanation of routing decisions

### BACnet Discovery Simulator
- Interactive Who-Is/I-Am demonstration
- Same subnet vs different subnet scenarios
- Device instance conflict detection
- Network number validation

### BBMD Configuration Tools
- Interactive BDT builder
- Visual network topology with BBMDs
- Message routing simulator
- Step-by-step forwarding demonstrations

### Broadcast Storm Simulator
- Multiple network topologies
- Real-time broadcast propagation
- Exponential packet growth visualization
- Storm detection metrics
- Prevention and mitigation guides

### Network Scenario Library
- Real-world case studies
- Interactive troubleshooting
- IP conflict detector
- Design best practices

## 💡 Educational Approach

This platform uses:
- **Progressive complexity**: Start simple, build to advanced
- **Visual learning**: Interactive diagrams and animations
- **Hands-on practice**: Configurable simulations
- **Real-world context**: BACnet-specific examples
- **Immediate feedback**: See results of changes instantly
- **Scenario-based learning**: Apply knowledge to practical situations

## 🎓 Complete Learning Outcomes

After completing all modules, you will be able to:

✅ Calculate subnet information from CIDR notation
✅ Understand binary operations in subnet masking
✅ Explain how devices process network packets
✅ Design BACnet networks with proper addressing
✅ Configure BBMDs for multi-subnet communication
✅ Detect and prevent broadcast storms
✅ Troubleshoot common BACnet network issues
✅ Apply best practices to real-world scenarios

## 🧪 Development

### Run tests (when implemented):
```bash
uv run pytest
```

### Code formatting:
```bash
uv run ruff format .
uv run ruff check .
```

## 📖 Technical Details

### Core Utilities (`src/ace_subnet_playground/subnet_calcs.py`)

Fully implemented subnet calculation functions:
- `subnet_to_cidr()` - Convert netmask to CIDR notation
- `cidr_to_netmask()` - Convert CIDR to netmask
- `netmask_info()` - Get detailed netmask information
- `calculate_subnet_size()` - Calculate usable hosts
- `calculate_subnet_info()` - Comprehensive subnet analysis
- `check_subnet_overlap()` - Detect overlapping subnets
- `is_ip_in_subnet()` - Check IP membership
- `is_private_network()` - Detect private IP ranges
- `get_network_class()` - Determine network class (A/B/C)
- `split_subnet()` - Divide subnet into smaller subnets
- `ip_to_binary()` - Convert IP to binary representation
- `binary_to_ip()` - Convert binary to IP address

## 🤝 About This Project

Created by the **Hive Mind Collective Intelligence System** - a coordinated swarm of specialized AI agents:

- **Researcher Agent**: Analyzed existing subnet education code from cxalloy-review-project
- **Analyst Agent**: Designed comprehensive application architecture
- **Coder Agent**: Planned implementation strategy and tech stack
- **Tester Agent**: Created comprehensive testing strategy

The application was built using insights from all agents working in parallel, implementing modules 1-6 in a single continuous development session.

## 🎉 Project Status

**🟢 100% COMPLETE - All Core Features Implemented!**

All 6 educational modules are fully functional with:
- Interactive visualizations
- Real-time simulations
- Hands-on exercises
- Troubleshooting tools
- Best practices guides

## 📄 License

Educational use.

## 🙏 Built With

- **Streamlit** - Interactive web framework
- **Plotly** - Visualization library
- **NetworkX** - Network graph algorithms
- **Python ipaddress** - Subnet calculations
- **uv** - Fast Python package manager

---

**Version**: 1.0.0
**Status**: ✅ **100% Complete** - All 6 modules functional
**Last Updated**: 2025-10-28
**Target Audience**: Network engineers, BACnet developers, building automation professionals
**Created By**: Hive Mind Collective (4 specialized AI agents)
