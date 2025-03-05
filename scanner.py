from port_scanner import nmap_scan
from owasp_zap_scan import zap_scan
import sys
import nmap

def main():
    #Main function to interact with the user in the terminal.
    print("Welcome to the Terminal-Based Vulnerability Scanner!")
    print("===========================================")
    target = None
    while True:
        print("\nSelect an option:")
        print("1. Set target url")
        print("2. Run a port scan")
        print("3. Run a OWASP scan")
        print("0. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            target = input("\nEnter the target IP or hostname: ").strip()
            if target == "test":
                target = "localhost"
        elif choice == "2" and target:
            print("\nChoose a scan type:")
            print("q: Quick scan (top 1,000 most common ports)")
            print("w: Well-known ports scan (ports 1-1024)")
            print("a: All ports scan (all 65,535 ports)")
            scan_type = input("Enter your choice (q, w, or a): ").strip().lower()
            # Run the scan
            nmap_scan(target, scan_type)
        elif choice == "3":
            zap_scan(target)
        elif choice == "0":
            print("\nExiting the scanner. Goodbye!")
            sys.exit(0)
        else:
            print("\nInvalid choice. Please try setting a target url or entering a valid number.")

if __name__ == "__main__":
    main()
