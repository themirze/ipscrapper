import socket as s
import requests
import argparse
from io import open
import re
import os
import time
import itertools
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

VERSION = '2.0.0'
BANNER = f"""

         
         ██████╗░░█████╗░██╗░░░░░██████╗░░██╗░░░░░░░██╗██╗███╗░░██╗
         ██╔══██╗██╔══██╗██║░░░░░██╔══██╗░██║░░██╗░░██║██║████╗░██║
         ██████╦╝███████║██║░░░░░██║░░██║░╚██╗████╗██╔╝██║██╔██╗██║
         ██╔══██╗██╔══██║██║░░░░░██║░░██║░░████╔═████║░██║██║╚████║
         ██████╦╝██║░░██║███████╗██████╔╝░░╚██╔╝░╚██╔╝░██║██║░╚███║
         ╚═════╝░╚═╝░░╚═╝╚══════╝╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚══╝

                                                                      {VERSION}
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

def scrape_urls(query, pages):
    """Scrape URLs from DuckDuckGo based on the provided query and number of pages"""
    # Chrome options for background mode
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f"https://duckduckgo.com/?va=j&t=hc&q={query}")

    loading = itertools.cycle(['|', '/', '-', '\\'])

    try:
        for i in range(pages):
            try:
                # Wait for the "more-results" button to be clickable
                time.sleep(2)
                more_results = driver.find_element(By.ID, "more-results")
                more_results.click()
                for _ in range(4):
                    print(f'\rLoading {next(loading)}', end='')
                    time.sleep(0.5)
            except:
                break  # No more results button, exit loop
    finally:
        print('\rLoading complete!')
        pageSource = driver.page_source
        driver.quit()

    if 'Make sure all words are spelled correctly.' in pageSource:
        exit('No Results Found.')

    urls = list(set(re.findall(r'</a></span><a href="(.*?)"', pageSource)))
    with open('Results.txt', 'w') as file:
        for url in urls:
            print(url)
            file.write(url + '\n')

    print('Successfully grabbed URLs.')
    return 'Results.txt'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find the IP address of any website")
    parser.add_argument('-d', '--domain', metavar='', type=str, required=False, help="Domain to track")
    parser.add_argument('-f', '--file', metavar='', type=str, required=False, help="File containing list of domains to track")
    parser.add_argument('-q', '--query', metavar='', type=str, required=False, help="Keyword query to scrape URLs from DuckDuckGo")
    parser.add_argument('-p', '--pages', metavar='', type=int, required=False, help="Number of pages to scrape for URLs")
    parser.add_argument('-s', '--save', action='store_true', help="Save results in a file")
    parser.add_argument('--version', action='store_true', help="Current version")
    args = parser.parse_args()

    if not any(vars(args).values()):
        print(BANNER)
        parser.print_help()
    else:
        if args.query and args.pages:
            file_path = scrape_urls(args.query, args.pages)
            if args.save:
                track_multiple_websites(file_path, save_file=True)
            else:
                track_multiple_websites(file_path)
        elif args.domain and args.save:
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
