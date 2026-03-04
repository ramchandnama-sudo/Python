"""Simple web scraper example using requests and BeautifulSoup.

Usage:
    python web_scraper.py <url>

This script fetches the given URL and prints the page title and all links.
It demonstrates basic HTML parsing and can be extended for specific sites.
"""

import sys
import requests
from bs4 import BeautifulSoup


def scrape(url: str):
    """Fetches the page at `url`, parses it, and prints some data."""
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Python Web Scraper/1.0)"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return

    soup = BeautifulSoup(resp.text, "html.parser")

    # print title
    title = soup.title.string if soup.title else "(no title)"
    print(f"Page title: {title}\n")

    # print all hyperlinks on the page
    links = []
    for a in soup.find_all("a", href=True):
        links.append(a["href"])

    print(f"Found {len(links)} links:")
    for link in links:
        print(link)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python web_scraper.py <url>")
        sys.exit(1)
    scrape(sys.argv[1])
