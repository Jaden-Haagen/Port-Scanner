import time
import subprocess
import requests
from zapv2 import ZAPv2

# Step 1: Start OWASP ZAP in Daemon Mode
def start_zap(target_url):
    #verify url before starting zap
    try:
        response = requests.head(target_url, timeout = 5)
        #return false if status is not between 200-399
        if response.status_code >= 400:
            print(f"{target_url} was not valid.")
            return False
    except requests.RequestException as e:
        print(f"Error verifiying {target_url}: {e}")
        return False
    #start ZAP if url verified
    print(f"{target_url} verified and is accessible. Starting scan process.")
    # Path to your ZAP directory and zap.sh script
    zap_process = subprocess.Popen(["ZAP_2.16.0/zap.sh", "-daemon", "-port", "8080"])
    print("ZAP started in daemon mode on port 8080.")
    return zap_process

# Step 2: Set up ZAP API client
def setup_zap_api():
    # ZAP API client setup (assuming ZAP is running on localhost:8080)
    zap = ZAPv2(proxies={'http': 'http://localhost:8080', 'https': 'http://localhost:8080'})
    return zap

# Step 3: Spider the target website
def spider_target(zap, target_url):
    print(f"Starting Spidering on {target_url}...")
    spider_scan = zap.spider.scan(target_url)
    while int(zap.spider.status(spider_scan)) < 100:
        print(f"Spidering in progress: {zap.spider.status(spider_scan)}% complete...")
        time.sleep(5)
    print("Spidering complete!")

# Step 4: Start Active Scan on the target
def active_scan(zap, target_url):
    print(f"Starting Active Scan on {target_url}...")
    active_scan = zap.ascan.scan(target_url)
    while int(zap.ascan.status(active_scan)) < 100:
        print(f"Active scan in progress: {zap.ascan.status(active_scan)}% complete...")
        time.sleep(5)
    print("Active Scan complete!")

# Step 5: Shut down ZAP after scanning is complete
def shutdown_zap(zap_process):
    print("Shutting down ZAP...")
    zap_process.terminate()
    zap_process.wait()
    print("ZAP has been shut down.")

#For analyzing the vulnerabilities later
def get_alerts(zap, baseurl):
    # Get all the alerts for the target (baseurl) from ZAP
    print("Retrieving alerts...")
    alerts = zap.core.alerts(baseurl=baseurl, start=0, count=1000)  # You can adjust the 'count' as needed
    return alerts

#Might modify to save in a text file
def print_alerts(alerts):
    if alerts:
        print(f"Found {len(alerts)} vulnerabilities:")
        for alert in alerts:
            print(f"Alert: {alert['alert']} | Risk: {alert['risk']}")
            print(f"URL: {alert['url']}")
            print(f"Description: {alert['description']}\n")
    else:
        print("No vulnerabilities found.")

# Main workflow
def main(target_url):
    # Start ZAP in daemon mode
    zap_process = start_zap()
    
    # Set up ZAP API client
    zap = setup_zap_api()

    # Run spider and active scan
    '''spider_target(zap, target_url)
    active_scan(zap, target_url)'''

    # Shutdown ZAP after scan completion
    shutdown_zap(zap_process)

def zap_scan(target_url):
    if target_url == "localhost" or target_url == None:
        target_url = "http://localhost:5000"
    zap_process = start_zap(target_url)
    if zap_process:
        zap = setup_zap_api
        spider_target(zap, target_url)
        active_scan(zap, target_url)
        shutdown_zap(zap_process)
        print_alerts(get_alerts(zap, target_url))
    return 0

if __name__ == "__main__":
    target_url = "http://localhost:5000" # "https://juice-shop.herokuapp.com/"  # example target urls can be used for testing
    main(target_url)
