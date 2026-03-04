import time
from typing import Iterator, Optional

import requests
from bs4 import BeautifulSoup


class StaticScraper:
    def __init__(self, start_url: str, next_selector: Optional[str] = None):
        """Create a scraper using requests and BeautifulSoup.

        ``next_selector`` may refer to a link to follow (CSS selector).
        """
        self.start_url = start_url
        self.next_selector = next_selector

    def scrape(self) -> Iterator[BeautifulSoup]:
        """Yield a BeautifulSoup object for each page in the series."""
        url = self.start_url
        while url:
            resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            yield soup
            if not self.next_selector:
                break
            next_tag = soup.select_one(self.next_selector)
            if next_tag and next_tag.get("href"):
                url = requests.compat.urljoin(url, next_tag["href"])
            else:
                break


class DynamicScraper:
    def __init__(self,
                 start_url: str,
                 next_selector: Optional[str] = None,
                 headless: bool = True):
        """Create a scraper driven by Selenium.

        Requires ``selenium`` and ``webdriver_manager`` to be installed.
        ``next_selector`` may refer to a clickable element (CSS selector) that
        loads additional content, or a link to follow.
        """
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.service import Service
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.common.by import By
            from selenium.webdriver.chrome.options import Options
        except ImportError as e:
            raise RuntimeError("Selenium and webdriver_manager must be installed")

        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                       options=chrome_options)
        self.start_url = start_url
        self.next_selector = next_selector

    def scrape(self, max_pages: Optional[int] = None, delay: float = 1.0) -> Iterator[BeautifulSoup]:
        """Yield a BeautifulSoup object for each page after rendering.

        :param max_pages: stop after this many pages (None => no limit)
        :param delay: seconds to wait after clicking/loading before parsing
        """
        self.driver.get(self.start_url)
        count = 0
        while True:
            html = self.driver.page_source
            yield BeautifulSoup(html, "html.parser")
            count += 1
            if max_pages is not None and count >= max_pages:
                break
            if not self.next_selector:
                break
            try:
                elem = self.driver.find_element(By.CSS_SELECTOR, self.next_selector)
            except Exception:
                break
            # attempt click, otherwise try href
            try:
                elem.click()
            except Exception:
                href = elem.get_attribute("href")
                if href:
                    self.driver.get(href)
                else:
                    break
            time.sleep(delay)
        self.driver.quit()


if __name__ == "__main__":
    # simple demonstration
    import argparse
    parser = argparse.ArgumentParser(description="Advanced scraper demo")
    parser.add_argument("url",
                        nargs="?",
                        default="https://jamesclear.com/why-facts-dont-change-minds",
                        help="starting URL (optional; defaults to jamesclear article)")
    parser.add_argument("--dynamic", action="store_true", help="use Selenium")
    parser.add_argument("--next", help="CSS selector for next page/button")
    args = parser.parse_args()

    if args.dynamic:
        sc = DynamicScraper(args.url, next_selector=args.next)
    else:
        sc = StaticScraper(args.url, next_selector=args.next)
    for i, page in enumerate(sc.scrape(), start=1):
        print(f"Page {i}: {page.title.string if page.title else '(no title)'}")
        if i >= 5:
            break
