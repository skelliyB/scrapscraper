import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse # the imports are for the script to work :3
from pprint import pprint
import argparse
import json
from colorama import Fore, Style, init
import logging
import random

filename = "dataon.json" # Default filename for JSON output feel free to change if you like :3

init(autoreset=True)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def legalnotice():
    print(Fore.RED + "By continuing, you acknowledge that you are responsible for complying with the target website's terms of service and applicable laws (INCLUDES ROBOTS.txt).") # legal notice 

def banner1(): # banners are just for fun and to make the script look more interesting :3 i made 4 of them and they are all different and i think they are pretty cool :3 you can add your own
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
            \_______/""")
    
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

# These are the arguments for the script :3
parser = argparse.ArgumentParser()
parser.add_argument('-pp','--pprint', action='store_true', help='Pretty print output')
parser.add_argument("-u",'--url', type=str, help='url of the website to scrape')
parser.add_argument('-j','--json', action='store_true', help='save output as JSON instead of plain text')
parser.add_argument('-ol', '--onlylinks', action='store_true', help='only print links')
parser.add_argument('-om', '--onlymeta', action='store_true', help='only print meta tags')
parser.add_argument('-otxt', '--onlytext', action='store_true', help='only prints text')
parser.add_argument('-ott', '--onlytitle', action='store_true', help='only prints title')
parser.add_argument('-f','--file', type=str, help='file name')
parser.add_argument('-s','--status', action='store_true', help='live reports')
parser.add_argument('-nb','--nobanner', action='store_true', help='disable banner output')
parser.add_argument('-nln','--nolegalnotice', action='store_true', help='disable legal notice (enabling means you agree to the legal notice)')
parser.add_argument('-q','--nonoise', action='store_true', help='disable banner and legal notice output')
parser.add_argument('-d', '--depth', type=int, default=0, help='crawl depth (0 = single page)')
args = parser.parse_args()

def nobanner():
    logging.info("banner disabled")
def nolegalnotice():
    logging.info("legal notice disabled")



    
# the main function that runs the script
def scrape_website(url: str):
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("error:", e)
        return None
    
    if args.status:
        if response.status_code == 200:
            logging.info( f"Status Code: {response.status_code}")
            print( Fore.GREEN + f"Status Code: {response.status_code}")
            logging.info(  f"Url: {url}")
        elif response.status_code == 404:
            logging.error( f"Status Code: {response.status_code}")
            print( Fore.RED + f"Status Code: {response.status_code}")
            logging.error( f"Url: {url}")
        else:
            logging.warning( f"Status Code: {response.status_code}")
            print( Fore.YELLOW + f"Status Code: {response.status_code}")
            logging.warning(  f"Url: {url}" )

    
    

    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.title.string if soup.title else "No title found"
    text = soup.get_text(separator="\n", strip=True)
    links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]
    meta = [
    {k: v for k, v in tag.attrs.items()} for tag in soup.find_all("meta")]



    if args.onlylinks:
        return {"links": links}
    elif args.onlymeta:
        return {"meta": meta}
    elif args.onlytext:
       return {"text": text} ## now finnaly works :3
    elif args.onlytitle:
        return {"title": title}
    else:
         return {
        "title": title,
        "text": text,
        "links": links,
        "meta": meta
         }

def get_same_domain_links(base_url, links):
    base_domain = urlparse(base_url).netloc
    clean_links = []
    for link in links:
        parsed = urlparse(link)
        if parsed.netloc == base_domain:
            clean_links.append(link)
    return clean_links

    
                


def crawl_with_depth(start_url, depth, headers=None, timeout=10):
    if headers is None:
        headers = {"User-Agent": "Mozilla/5.0"}

    visited = set()
    results = {}
    queue = [(start_url, 0)]

    while queue:
        current_url, current_depth = queue.pop(0)

        if current_url in visited or current_depth > depth:
            continue

        visited.add(current_url)

        data = scraper(
            current_url,
            timeout=timeout,
            headers=headers
        )

        if not data:
            continue

        results[current_url] = {
            "title": data["title"],
            "depth": current_depth
        }

        if current_depth < depth:
            same_domain_links = get_same_domain_links(
                start_url, data["links"]
            )
            for link in same_domain_links:
                if link not in visited:
                    queue.append((link, current_depth + 1))

    return results


def scraper(site, timeout, headers):
    headers = headers
    try:
        response = requests.get(site, headers=headers, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("error:", e)
        return None
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string if soup.title else "No title found"
    text = soup.get_text(separator="\n", strip=True)
    links = [urljoin(site, a['href']) for a in soup.find_all('a', href=True)]
    meta = [{k: v for k, v in tag.attrs.items()} for tag in soup.find_all("meta")]
    return {
        "title": title,
        "text": text,
        "links": links,
        "meta": meta
    }

def scrapedepth(site, timeout, headers, prettyprint, depth):
    data = crawl_with_depth(site,  headers=headers, depth=depth)
    if prettyprint == True:
        pprint(data)
    else:
        print(data)


def scrapelinks(site, timeout, headers):
    headers = headers
    try:
        response = requests.get(site, headers=headers, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("error:", e)
        return None
    soup = BeautifulSoup(response.content, 'html.parser')
    links = [urljoin(site, a['href']) for a in soup.find_all('a', href=True)]
    return links

def scrapemeta(site, timeout, headers):
    headers = headers
    try:
        response = requests.get(site, headers=headers, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("error:", e)
        return None
    soup = BeautifulSoup(response.content, 'html.parser')
    meta = [{k: v for k, v in tag.attrs.items()} for tag in soup.find_all("meta")]
    return meta

def scrapetext(site, timeout, headers):
    headers = headers
    try:
        response = requests.get(site, headers=headers, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("error:", e)
        return None
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text(separator="\n", strip=True)
    return text

def scrapetitle(site, timeout, headers):
    headers = headers
    try:
        response = requests.get(site, headers=headers, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("error:", e)
        return None
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string if soup.title else "No title found"
    return title

# calling all the fuction and making sure the script runs correctly :3
if __name__ == "__main__":

    
    mainurl = args.url
    data = scrape_website(mainurl)
    if not args.url:
        parser.error("URL is required (-u / --url)")


    if  not is_valid_url(mainurl):
        
        print("invalid url")
        logging.error("invalid url")
        exit(1)

    if args.depth > 0:

        data = crawl_with_depth(mainurl, args.depth)
    else:
        logging.info("single page scrape")

    

    

    if args.nonoise:
        args.nobanner = True
        args.nolegalnotice = True

    if not args.nobanner:
        banner = random.choice([banner1, banner2, banner3, banner4])
        banner()
    else:
        nobanner()

    if not args.nolegalnotice:
        legalnotice()
    else: 
        nolegalnotice()

    data = scrape_website(mainurl)

        
        
    

    if data is None:
        logging.error("failed to scrape the website")
        exit(1)

    if args.json and args.file:
        try:
            with open(args.file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"Data saved to {args.file}")

        except Exception as e:
            logging.error(f"Failed to save data to {args.file}: {e}")
            exit(1)
        

    if args.json and not args.file:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)     
        print(f"Data saved to {filename}")      
        
    elif args.pprint:
        pprint(data)

    else:
        print(data)
    

    
           
    
