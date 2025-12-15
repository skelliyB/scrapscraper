---
title: scrapscraper
---

# scrapscraper

Used for retrieving data from sites—basically web scraping with Python.

## Uses
One, it’s pretty quick and fast for first-page depth. I am updating it as much as possible. I am the sole developer. It works using `requests`, `BeautifulSoup`, `json`, `argparse`, and `PrettyPrint`.

## Author
– made by skelliyb (alt: lemonsrC00l)

## Arguments
| Flag | Description |
|------|-------------|
| -u   | Target URL |
| -ol  | Output only links |
| -otxt| Output only text |
| -ott | Output only page title |
| -om  | Output only metadata |
| -d   | Recursive depth |
| -f   | Save output to file |
| -j   | Output as JSON |
| -pp  | Enable PrettyPrint |
| -s   | Show HTTP status codes |
| -nb  | Disable banner |
| -nln | Disable legal notice |
| -q   | Quiet mode |

## Features
- Fast scraping for first-page depth  
- Link, text, title, and metadata extraction  
- Optional recursive link fuzzing  
- JSON and pretty-printed output  
- File saving support  
- Status code reporting  
- Tor & proxy support (in progress)  
- CLI-based and callable functions  

## Installation
```bash
git clone https://github.com/skelliyB/scrapscraper
cd scrapscraper
pip install scrapscraper
pip install -r requirements.txt


```python
##Usage

# Basic scrape of a URL
python scrapscraper.py -u https://example.com

# Only output links
python scrapscraper.py -u https://example.com -ol

# Only output text
python scrapscraper.py -u https://example.com -otxt

# Output as JSON and save to file
python scrapscraper.py -u https://example.com -j -f data.json

# Crawl recursively with depth 2
python scrapscraper.py -u https://example.com -d 2 -pp

##funcions
results = scrapedepth("https://example.com", depth=2)
print(results)
from scrapscraper import scrapetext

text = scrapetext("https://example.com", timeout=10, headers={"User-Agent": "Mozilla/5.0"})
print(text)

from scrapscraper import scrapelinks

links = scrapelinks("https://example.com", timeout=10, headers={"User-Agent": "Mozilla/5.0"})
print(links)

from scrapscraper import crawl_with_depth

from scrapscraper import scrapetor

data = scrapetor("https://example.com", timeout=10, proxies="torbundle")
print(data["links"])  # or ["text"], ["title"], ["meta"]

