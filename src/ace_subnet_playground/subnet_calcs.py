"""
Network Calculation Utilities
Core subnet calculation functions for educational application
"""

import ipaddress
from typing import Dict, List, Optional, Union


def subnet_to_cidr(netmask_str: str) -> Optional[int]:
    """
    Convert netmask to CIDR notation

    Args:
        netmask_str: Netmask in dotted decimal (e.g., '255.255.255.0')

    Returns:
        CIDR prefix length (e.g., 24) or None if invalid

    Example:
        >>> subnet_to_cidr('255.255.255.0')
        24
    """
    try:
        netmask = ipaddress.IPv4Address(netmask_str)
        return ipaddress.IPv4Network(f'0.0.0.0/{netmask_str}').prefixlen
    except ValueError:
        return None


def cidr_to_netmask(cidr: int) -> Optional[str]:
    """
    Convert CIDR to netmask

    Args:
        cidr: CIDR prefix length (0-32)

    Returns:
        Netmask in dotted decimal or None if invalid

    Example:
        >>> cidr_to_netmask(24)
        '255.255.255.0'
    """
    try:
        network = ipaddress.IPv4Network(f'0.0.0.0/{cidr}')
        return str(network.netmask)
    except ValueError:
        return None


def netmask_info(cidr: int) -> Optional[Dict[str, Union[int, str]]]:
    """
    Get detailed information about a netmask/CIDR

    Args:
        cidr: CIDR prefix length

    Returns:
        Dictionary with netmask details or None if invalid
    """
    try:
        network = ipaddress.IPv4Network(f'0.0.0.0/{cidr}')
        return {
            'cidr': cidr,
            'netmask': str(network.netmask),
            'wildcard': str(network.hostmask),
            'total_addresses': network.num_addresses,
            'usable_hosts': network.num_addresses - 2,
            'network_bits': cidr,
            'host_bits': 32 - cidr
        }
    except ValueError:
        return None


def calculate_subnet_size(cidr: int) -> int:
    """
    Calculate how many hosts fit in a subnet

    Args:
        cidr: CIDR prefix length

    Returns:
        Number of usable host addresses

    Example:
        >>> calculate_subnet_size(24)
        254
    """
    host_bits = 32 - int(cidr)
    total = 2 ** host_bits
    usable = total - 2  # Subtract network and broadcast addresses
    return usable


def calculate_subnet_info(network_str: str) -> Dict[str, Union[str, int]]:
    """
    Calculate comprehensive subnet information

    Args:
        network_str: Network in CIDR notation (e.g., '192.168.1.0/24')

    Returns:
        Dictionary with complete subnet information

    Example:
        >>> info = calculate_subnet_info('192.168.1.0/24')
        >>> info['network_address']
        '192.168.1.0'
        >>> info['usable_hosts']
        254
    """
    try:
        network = ipaddress.IPv4Network(network_str, strict=False)

        return {
            'network_address': str(network.network_address),
            'broadcast_address': str(network.broadcast_address),
            'netmask': str(network.netmask),
            'wildcard_mask': str(network.hostmask),
            'cidr': network.prefixlen,
            'first_usable': str(network.network_address + 1),
            'last_usable': str(network.broadcast_address - 1),
            'total_addresses': network.num_addresses,
            'usable_hosts': network.num_addresses - 2 if network.num_addresses > 2 else 0,
            'network_bits': network.prefixlen,
            'host_bits': 32 - network.prefixlen
        }
    except ValueError as e:
        return {'error': str(e)}


def check_subnet_overlap(network1_str: str, network2_str: str) -> tuple[bool, str]:
    """
    Check if two subnets overlap

    Args:
        network1_str: First network in CIDR notation
        network2_str: Second network in CIDR notation

    Returns:
        Tuple of (overlaps: bool, explanation: str)

    Example:
        >>> overlaps, explanation = check_subnet_overlap('192.168.1.0/24', '192.168.1.0/25')
        >>> overlaps
        True
    """
    try:
        net1 = ipaddress.IPv4Network(network1_str, strict=False)
        net2 = ipaddress.IPv4Network(network2_str, strict=False)

        # Check if networks overlap
        overlaps = net1.overlaps(net2)

        if overlaps:
            # Determine the type of overlap
            if net1 == net2:
                explanation = f"Networks are identical: {net1}"
            elif net1.subnet_of(net2):
                explanation = f"{net1} is a subnet of {net2}"
            elif net2.subnet_of(net1):
                explanation = f"{net2} is a subnet of {net1}"
            else:
                explanation = f"Networks partially overlap"

            return (True, explanation)
        else:
            # Calculate how far apart they are
            gap = abs(int(net1.network_address) - int(net2.network_address))
            explanation = f"Networks do not overlap. Addresses are {gap} apart."
            return (False, explanation)

    except ValueError as e:
        return (False, f"Error parsing networks: {e}")


def is_ip_in_subnet(ip_str: str, network_str: str) -> bool:
    """
    Check if an IP address is within a subnet

    Args:
        ip_str: IP address (e.g., '192.168.1.100')
        network_str: Network in CIDR notation (e.g., '192.168.1.0/24')

    Returns:
        True if IP is in subnet, False otherwise
    """
    try:
        ip_addr = ipaddress.IPv4Address(ip_str)
        network = ipaddress.IPv4Network(network_str, strict=False)
        return ip_addr in network
    except ValueError:
        return False


def is_private_network(network_str: str) -> bool:
    """
    Check if network is in private IP range

    Args:
        network_str: Network in CIDR notation

    Returns:
        True if network is private (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16)
    """
    try:
        network = ipaddress.IPv4Network(network_str, strict=False)
        return network.is_private
    except ValueError:
        return False


def get_network_class(network_str: str) -> Optional[Dict[str, Union[str, bool]]]:
    """
    Determine network class with size-aware classification and boundary validation

    Returns both traditional class (by IP range) and effective class (by subnet size),
    plus warnings for boundary violations.

    Args:
        network_str: Network in CIDR notation

    Returns:
        Dictionary with:
        - 'range_class': Traditional class based on IP address range (A/B/C/D/E)
        - 'size_class': Effective class based on subnet mask size
        - 'display': Human-readable classification string
        - 'is_valid': Boolean indicating if subnet crosses boundaries
        - 'warnings': List of warning messages for boundary violations

    Example:
        >>> get_network_class('172.16.0.1/24')
        {'range_class': 'B', 'size_class': 'C', 'display': 'Class C-sized inside Class B range', ...}
    """
    try:
        network = ipaddress.IPv4Network(network_str, strict=False)
        first_octet = int(str(network.network_address).split('.')[0])
        cidr = network.prefixlen
        warnings = []
        is_valid = True

        # Determine traditional class by IP range
        if first_octet < 128:
            range_class = 'A'
        elif first_octet < 192:
            range_class = 'B'
        elif first_octet < 224:
            range_class = 'C'
        elif first_octet < 240:
            range_class = 'D (Multicast)'
        else:
            range_class = 'E (Reserved)'

        # Determine size-based class by subnet mask (smaller CIDR = bigger network)
        # Class A: /1 to /8 (huge networks)
        # Class B: /9 to /16 (large networks)
        # Class C: /17 to /24 (medium networks)
        # Subnet: /25+ (small networks)
        if cidr <= 8:
            size_class = 'A'
        elif cidr <= 16:
            size_class = 'B'
        elif cidr <= 24:
            size_class = 'C'
        else:
            size_class = 'Subnet'

        # Check for boundary violations
        # Private IP ranges: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16
        private_ranges = [
            ipaddress.IPv4Network('10.0.0.0/8'),
            ipaddress.IPv4Network('172.16.0.0/12'),
            ipaddress.IPv4Network('192.168.0.0/16')
        ]

        # Check if subnet crosses private/public boundaries
        network_start = network.network_address
        network_end = network.broadcast_address

        # Check if subnet overlaps with any private range
        overlapping_ranges = [pr for pr in private_ranges if network.overlaps(pr)]

        # If it overlaps with private ranges, check if it extends beyond them
        if overlapping_ranges:
            # Check if the subnet is fully contained within the private ranges
            fully_contained = any(network.subnet_of(pr) for pr in private_ranges)

            if not fully_contained:
                # Subnet overlaps but extends beyond private range boundaries
                warnings.append("⚠️ Subnet crosses private/public IP boundary!")
                is_valid = False

            # Check if subnet crosses multiple private ranges
            if len(overlapping_ranges) > 1:
                warnings.append("⚠️ Subnet spans multiple private IP ranges!")
                is_valid = False

        # Check for class boundary violations (supernetting across classes)
        # Class A: 0.0.0.0 - 127.255.255.255
        # Class B: 128.0.0.0 - 191.255.255.255
        # Class C: 192.0.0.0 - 223.255.255.255
        start_octet = int(str(network_start).split('.')[0])
        end_octet = int(str(network_end).split('.')[0])

        start_class = None
        end_class = None

        if start_octet < 128:
            start_class = 'A'
        elif start_octet < 192:
            start_class = 'B'
        elif start_octet < 224:
            start_class = 'C'

        if end_octet < 128:
            end_class = 'A'
        elif end_octet < 192:
            end_class = 'B'
        elif end_octet < 224:
            end_class = 'C'

        if start_class != end_class:
            warnings.append(f"⚠️ Subnet crosses Class {start_class}/{end_class} boundary!")
            is_valid = False

        # Build display string
        if not is_valid:
            display = f"Invalid: {size_class}-sized subnet crossing boundaries"
        elif first_octet >= 224:
            display = range_class  # D or E
        # Check if this exactly matches a standard private range
        elif network == ipaddress.IPv4Network('10.0.0.0/8'):
            display = "Class A (Standard private range)"
        elif network == ipaddress.IPv4Network('172.16.0.0/12'):
            display = "Class B (Standard private range)"
        elif network == ipaddress.IPv4Network('192.168.0.0/16'):
            display = "Class B-sized (Standard private range)"
        elif range_class == size_class:
            display = f"Class {range_class}"
        else:
            display = f"Class {size_class}-sized inside Class {range_class} range"

        return {
            'range_class': range_class,
            'size_class': size_class,
            'display': display,
            'is_valid': is_valid,
            'warnings': warnings
        }

    except ValueError:
        return None


def split_subnet(network_str: str, new_prefix: int) -> Union[List[str], Dict[str, str]]:
    """
    Split a subnet into smaller subnets

    Args:
        network_str: Network to split (e.g., '192.168.1.0/24')
        new_prefix: New CIDR prefix (must be larger than current)

    Returns:
        List of subnet strings or error dict

    Example:
        >>> split_subnet('192.168.1.0/24', 25)
        ['192.168.1.0/25', '192.168.1.128/25']
    """
    try:
        network = ipaddress.IPv4Network(network_str, strict=False)
        new_prefix = int(new_prefix)

        if new_prefix <= network.prefixlen:
            return {'error': 'New prefix must be larger (smaller network)'}

        subnets = list(network.subnets(new_prefix=new_prefix))
        return [str(subnet) for subnet in subnets]

    except ValueError as e:
        return {'error': str(e)}


def ip_to_binary(ip_str: str) -> Optional[str]:
    """
    Convert IP address to binary string with dots between octets

    Args:
        ip_str: IP address in dotted decimal

    Returns:
        Binary string (e.g., '11000000.10101000.00000001.01100100')

    Example:
        >>> ip_to_binary('192.168.1.100')
        '11000000.10101000.00000001.01100100'
    """
    try:
        ip_addr = ipaddress.IPv4Address(ip_str)
        octets = str(ip_addr).split('.')
        binary_octets = [format(int(octet), '08b') for octet in octets]
        return '.'.join(binary_octets)
    except ValueError:
        return None


def binary_to_ip(binary_str: str) -> Optional[str]:
    """
    Convert binary string to IP address

    Args:
        binary_str: Binary string with or without dots

    Returns:
        IP address in dotted decimal

    Example:
        >>> binary_to_ip('11000000.10101000.00000001.01100100')
        '192.168.1.100'
    """
    try:
        # Remove dots if present
        binary_clean = binary_str.replace('.', '')

        if len(binary_clean) != 32:
            return None

        # Convert to octets
        octets = [binary_clean[i:i+8] for i in range(0, 32, 8)]
        decimal_octets = [str(int(octet, 2)) for octet in octets]

        return '.'.join(decimal_octets)
    except ValueError:
        return None
