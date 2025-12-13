# main.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pprint import pprint
import argparse
import json
from colorama import Fore, init
import logging
import random

filename = "dataon.json"

init(autoreset=True)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def legalnotice():
    print(Fore.RED + "By continuing, you acknowledge that you are responsible for complying with the target website's terms of service and applicable laws (INCLUDES ROBOTS.txt).")


def banner1():
    print(Fore.CYAN + r""" ____                      
/ ___| _ __ __ _ _ __  ___ 
\___ \| '__/ _` | '_ \/ __|
 ___) | | | (_| | |_) \__ \
|____/|_|  \__,_| .__/|___/
                |_|""")
    
def banner2():
    print(Fore.RED + r""" 
        /               \
       /                 \
      /                   \
      |   XXXX     XXXX   |
      |   XXXX     XXXX   |
      |   XXX       XXX   |
      |         X         |
      \__      XXX     __/
        |\     XXX     /|
        | |           | |
        | I I I I I I I |
        |  I I I I I I  |
         \_           _/
          \_         _/
            \_______/""") # ascii :3
def banner3():
    print(Fore.MAGENTA + r""" 
                  FISHKISSFISHKIS               
       SFISHKISSFISHKISSFISH            F
    ISHK   ISSFISHKISSFISHKISS         FI
  SHKISS   FISHKISSFISHKISSFISS       FIS
HKISSFISHKISSFISHKISSFISHKISSFISH    KISS
  FISHKISSFISHKISSFISHKISSFISHKISS  FISHK
      SSFISHKISSFISHKISSFISHKISSFISHKISSF
  ISHKISSFISHKISSFISHKISSFISHKISSF  ISHKI
SSFISHKISSFISHKISSFISHKISSFISHKIS    SFIS
  HKISSFISHKISSFISHKISSFISHKISS       FIS
    HKISSFISHKISSFISHKISSFISHK         IS
       SFISHKISSFISHKISSFISH            K
         ISSFISHKISSFISHK    """)
def banner4():
    print(Fore.GREEN + r""" 
         What's reality? I don't know. When my bird was looking at my computer monitor,
 I thought "Whoa! That bird has no idea what he's looking at!"

 And yet, what does the bird do? Does he panic?

 No, he can't really panic, he just does the best he can.

 Is he able to live in a world where he's so ignorant?

 Well, he doesn't really have a choice.

 The bird is okay, even though he doesn't really understand the world.

 You're that bird looking at the monitor, and you're thinking to yourself
 "I can figure this out!"

 Maybe you have some bird ideas. Maybe that's the best you can do.

  ~ Terry A. Davis ( i dont agree with the stuff he said like stuff about racism and stuff but i like him in a technilogical  way rip terry)""")


def is_valid_url(url: str) -> bool:
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme) and bool(parsed_url.netloc)


def scrape_website(url: str, args):
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("error:", e)
        return None

    if args.status:
        if response.status_code == 200:
            logging.info(Fore.GREEN + f"Status Code: {response.status_code}")
        elif response.status_code == 404:
            logging.error(Fore.RED + f"Status Code: {response.status_code}")
        else:
            logging.warning(Fore.YELLOW + f"Status Code: {response.status_code}")

    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.title.string if soup.title else "No title found"
    text = soup.get_text(separator="\n", strip=True)
    links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]
    meta = [{k: v for k, v in tag.attrs.items()} for tag in soup.find_all("meta")]

    if args.onlylinks:
        return {"links": links}
    elif args.onlymeta:
        return {"meta": meta}
    elif args.onlytitle:
        return {"title": title}
    else:
        return {"title": title, "text": text, "links": links, "meta": meta}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-pp','--pprint', action='store_true', help='Pretty print output')
    parser.add_argument("-u",'--url', type=str, help='URL of the website to scrape')
    parser.add_argument('-j','--json', action='store_true', help='Save output as JSON')
    parser.add_argument('-ol', '--onlylinks', action='store_true', help='Only print links')
    parser.add_argument('-om', '--onlymeta', action='store_true', help='Only print meta tags')
    parser.add_argument('-ott', '--onlytitle', action='store_true', help='Only print title')
    parser.add_argument('-f','--file', type=str, help='File name')
    parser.add_argument('-s','--status', action='store_true', help='Live reports')
    parser.add_argument('-nb','--nobanner', action='store_true', help='Disable banner output')
    parser.add_argument('-nln','--nolegalnotice', action='store_true', help='Disable legal notice')
    parser.add_argument('-q','--nonoise', action='store_true', help='Disable banner and legal notice')
    args = parser.parse_args()

    mainurl = args.url
    if not mainurl:
        parser.error("URL is required (-u / --url)")
    if not is_valid_url(mainurl):
        logging.error("Invalid URL")
        exit(1)

    if args.nonoise:
        args.nobanner = True
        args.nolegalnotice = True

    if not args.nobanner:
        banner = random.choice([banner1, banner2, banner3, banner4])
        banner()
    if not args.nolegalnotice:
        legalnotice()

    data = scrape_website(mainurl, args)
    if data is None:
        logging.error("Failed to scrape the website")
        exit(1)

    if args.json and args.file:
        with open(args.file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Data saved to {args.file}")
    elif args.json:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Data saved to {filename}")
    elif args.pprint:
        pprint(data)
    else:
        print(data)


if __name__ == "__main__":
    main()
