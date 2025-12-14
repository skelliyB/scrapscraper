```md
## scrapscraper
Used for retrieving data from sites basically web scraping with python 
## Uses
One its pretty quick and fast for first page depth 
I am updating it as much as possible
i am the sole developer
how it works is pretty simple it uses requests , beautiful soup, json, argparse , and PrettyPrint to make it look pretty

## author
-- made by skelliyb and my alt is lemonsrC00l


## Arguments

| Flag | Description |
|----|------------|
| `-u` | Target URL |
| `-ol` | Output only links |
| `-otxt` | Output only text |
| `-ott` | Output only page title |
| `-om` | Output only metadata |
| `-d` | Recursive depth |
| `-f` | Save output to file |
| `-j` | Output as JSON |
| `-pp` | Enable PrettyPrint |
| `-s` | Show HTTP status codes |
| `-nb` | Disable banner |
| `-nln` | Disable legal notice |
| `-q` | Quiet mode |

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
pip install -r requirements.txt
