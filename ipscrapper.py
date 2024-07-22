import socket as s
import requests
import argparse
from io import open

VERSION = '1.2.0'
BANNER = f"""

         
         ██████╗░░█████╗░██╗░░░░░██████╗░░██╗░░░░░░░██╗██╗███╗░░██╗
         ██╔══██╗██╔══██╗██║░░░░░██╔══██╗░██║░░██╗░░██║██║████╗░██║
         ██████╦╝███████║██║░░░░░██║░░██║░╚██╗████╗██╔╝██║██╔██╗██║
         ██╔══██╗██╔══██║██║░░░░░██║░░██║░░████╔═████║░██║██║╚████║
         ██████╦╝██║░░██║███████╗██████╔╝░░╚██╔╝░╚██╔╝░██║██║░╚███║
         ╚═════╝░╚═╝░░╚═╝╚══════╝╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚══╝


"""

def verify_internet() -> bool:
    """Check if there is an internet connection"""
    connected = False
    try:
        r = requests.get("https://google.com")
        if r.status_code == 200:
            connected = True
        else:
            print("Oops, check your internet connection")
    except:
        print("Oops, check your internet connection")
    finally:
        return connected

def track_website_ip(domain, save_file=False):
    """Tracks the IP address of the website passed as argument"""
    try:
        if verify_internet():
            ip = s.gethostbyname(domain)
            print(f"{domain} | {ip}")
            # If user wants generate a .txt file to save results
            if save_file:
                save_results(domain, ip)
    except s.gaierror:
        print(f"Domain {domain} failed, try again please")

def save_results(domain, ip):
    """Save results in a .txt file"""
    with open('results.txt', 'a+') as f:
        f.write(f"{domain} : {ip}" + '\n')

def track_multiple_websites(file_path, save_file=False):
    """Tracks the IP addresses of websites listed in a file"""
    with open(file_path, 'r') as file:
        domains = file.readlines()
    for domain in domains:
        domain = domain.strip()
        track_website_ip(domain, save_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find the IP address of any website")
    parser.add_argument('-d', '--domain', metavar='', type=str, required=False, help="Domain to track")
    parser.add_argument('-f', '--file', metavar='', type=str, required=False, help="File containing list of domains to track")
    parser.add_argument('-s', '--save', action='store_true', help="Save results in a file")
    parser.add_argument('--version', action='store_true', help="Current version")
    args = parser.parse_args()

    if not any(vars(args).values()):
        print(BANNER)
        parser.print_help()
    else:
        if args.domain and args.save:
            track_website_ip(args.domain, save_file=True)
        elif args.domain:
            track_website_ip(args.domain)
        elif args.file and args.save:
            track_multiple_websites(args.file, save_file=True)
        elif args.file:
            track_multiple_websites(args.file)
        elif args.version:
            print(f"Website IP Tracker {VERSION}")
        else:
            parser.print_help()
