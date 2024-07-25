import socket as s
import requests
import argparse
from io import open
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

VERSION = '2.2.0'
BANNER = f"""
         
         ██████╗░░█████╗░██╗░░░░░██████╗░░██╗░░░░░░░██╗██╗███╗░░██╗
         ██╔══██╗██╔══██╗██║░░░░░██╔══██╗░██║░░██╗░░██║██║████╗░██║
         ██████╦╝███████║██║░░░░░██║░░██║░╚██╗████╗██╔╝██║██╔██╗██║
         ██╔══██╗██╔══██║██║░░░░░██║░░██║░░████╔═████║░██║██║╚████║
         ██████╦╝██║░░██║███████╗██████╔╝░░╚██╔╝░╚██╔╝░██║██║░╚███║
         ╚═════╝░╚═╝░░╚═╝╚══════╝╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚══╝

                                                                      {VERSION} """

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

def normalize_domain(domain):
    """Remove http:// or https:// from the domain if present"""
    if domain.startswith("http://"):
        domain = domain[len("http://"):]
    elif domain.startswith("https://"):
        domain = domain[len("https://"):]
    return domain

def track_website_ip(domain, save_file=False):
    """Tracks the IP address of the website passed as argument"""
    try:
        if verify_internet():
            domain = normalize_domain(domain)
            ip = s.gethostbyname(domain)
            print(f"{domain} | {ip}")
            if save_file:
                save_results(ip)
    except s.gaierror:
        print(f"Domain {domain} failed, try again please")

def save_results(ip):
    """Save results in a .txt file"""
    with open('results.txt', 'a+') as f:
        f.write(f"{ip}" + '\n')

def track_multiple_websites(file_path, save_file=False):
    """Tracks the IP addresses of websites listed in a file"""
    with open(file_path, 'r') as file:
        domains = file.readlines()
    for domain in domains:
        domain = domain.strip()
        track_website_ip(domain, save_file)

def get_urls(query, pages):
    """Retrieve URLs from DuckDuckGo"""
    driver = webdriver.Chrome()
    driver.get(f"https://duckduckgo.com/?va=j&t=hc&q={query}")

    loading_symbols = ['|', '/', '-', '\\']
    filter_domains = [
        "youtube.com",
        "facebook.com",
        "google.com",
        "google.az",
        "google.pl",
        "wikipedia.org"
    ]

    all_urls = []

    try:
        for i in range(pages):
            try:
                time.sleep(2)
                more_results = driver.find_element(By.ID, "more-results")
                more_results.click()
                for j in range(4):
                    print(f'\rLoading {loading_symbols[j % len(loading_symbols)]}', end='')
                    time.sleep(0.5)
            except:
                break

        elements = driver.find_elements(By.CSS_SELECTOR, '[data-testid="result-extras-url-link"]')
        for element in elements:
            first_child = element.find_element(By.CSS_SELECTOR, ':first-child')
            url = first_child.text
            if len(url) > 1 and not any(domain in url for domain in filter_domains):
                all_urls.append(url)
    finally:
        print('\rLoading complete!')
        driver.quit()

    return all_urls

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find the IP address of any website")
    parser.add_argument('-d', '--domain', metavar='', type=str, required=False, help="Domain to track")
    parser.add_argument('-f', '--file', metavar='', type=str, required=False, help="File containing list of domains to track")
    parser.add_argument('-s', '--save', action='store_true', help="Save results in a file")
    parser.add_argument('--version', action='store_true', help="Current version")
    parser.add_argument('-gu', '--get-url', metavar='', type=str, required=False, help="Get URLs based on keyword")
    parser.add_argument('-p', '--pages', metavar='', type=int, required=False, help="Number of pages to search")
    parser.add_argument('-gi', '--get-ip', action='store_true', help="Get IP addresses of the found URLs")
    args = parser.parse_args()

    if not any(vars(args).values()):
        print(BANNER)
        parser.print_help()
    else:
        if args.get_url and args.pages:
            urls = get_urls(args.get_url, args.pages)
            filename = f"{args.get_url.replace(' ', '_')}.txt"
            with open(filename, 'w') as file:
                for url in urls:
                    file.write(f'{url}\n')
            if args.get_ip:
                for url in urls:
                    track_website_ip(url, save_file=args.save)
        elif args.domain and args.save:
            track_website_ip(args.domain, save_file=True)
        elif args.domain:
            track_website_ip(args.domain)
        elif args.file and args.save:
            track_multiple_websites(args.file, save_file=True)
        elif args.file:
            track_multiple_websites(args.file)
        elif args.version:
            print(f"BALDWIN {VERSION}")
        else:
            parser.print_help()
