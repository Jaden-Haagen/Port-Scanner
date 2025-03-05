#Scan the network for open ports
import nmap
import sys

def nmap_scan(target, scan_type):
    #Performs an Nmap scan based on the provided scan type.
    scanner = nmap.PortScanner()

    if scan_type == "q":
        print(f"\n[Quick Scan] Scanning {target} for the top 1,000 most common ports...")
        scanner.scan(target)  # Default quick scan
    elif scan_type == "w":
        print(f"\n[Well-Known Ports Scan] Scanning {target} for ports 1-1024...")
        scanner.scan(target, '1-1024')
    elif scan_type == "a":
        print(f"\n[All Ports Scan] Scanning {target} for all 65,535 ports (this may take a while)...")
        scanner.scan(target, '1-65535')
    else:
        print("Invalid scan type. Use 'q', 'w', or 'a'.")
        return

    # Display scan results
    for host in scanner.all_hosts():
        print(f"\nHost: {host} ({scanner[host].hostname()})")
        print(f"State: {scanner[host].state()}")

        for protocol in scanner[host].all_protocols():
            print(f"\nProtocol: {protocol}")
            ports = scanner[host][protocol].keys()
            for port in sorted(ports):
                port_info = scanner[host][protocol][port]
                print(f"Port: {port}\tState: {port_info['state']}\tService: {port_info.get('name', 'Unknown')}")

