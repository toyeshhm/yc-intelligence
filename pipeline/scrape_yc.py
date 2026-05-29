"""
YC Company Directory Scraper
Fetches company data from Y Combinator's public companies page/API.
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import httpx
from bs4 import BeautifulSoup

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

HEADERS = {
    "User-Agent": "YC-Intel-OS/1.0 (research; open-source)",
    "Accept": "text/html,application/json",
}


@dataclass
class ScrapedCompany:
    name: str
    slug: str
    batch: str
    tagline: str
    industry: str
    status: str
    website: str | None
    description: str | None


def slugify(name: str) -> str:
    return re.sub(r"(^-|-$)", "", re.sub(r"[^a-z0-9]+", "-", name.lower()))


def scrape_yc_algolia(client: httpx.Client) -> list[ScrapedCompany]:
    """Attempt YC Algolia-backed search API used by the companies page."""
    url = "https://45bwzk1cta.execute-api.us-west-1.amazonaws.com/prod/rpc/search"
    companies: list[ScrapedCompany] = []
    page = 0

    while True:
        payload = {
            "params": f"query=&page={page}&hitsPerPage=100&facetFilters=%5B%5D"
        }
        try:
            resp = client.post(url, json=payload, headers=HEADERS, timeout=30)
            if resp.status_code != 200:
                break
            data = resp.json()
            hits = data.get("hits", [])
            if not hits:
                break
            for hit in hits:
                name = hit.get("name", "")
                if not name:
                    continue
                companies.append(
                    ScrapedCompany(
                        name=name,
                        slug=hit.get("slug") or slugify(name),
                        batch=hit.get("batch", "Unknown"),
                        tagline=hit.get("one_liner") or hit.get("oneLiner") or "",
                        industry=hit.get("industry") or hit.get("subindustry") or "Unknown",
                        status=hit.get("status") or "Active",
                        website=hit.get("website"),
                        description=hit.get("long_description") or hit.get("longDescription"),
                    )
                )
            page += 1
            if page >= 60:
                break
            time.sleep(0.3)
        except Exception as e:
            print(f"Algolia fetch stopped at page {page}: {e}")
            break

    return companies


def scrape_yc_html_fallback(client: httpx.Client) -> list[ScrapedCompany]:
    """Fallback: parse embedded JSON from companies HTML page."""
    resp = client.get("https://www.ycombinator.com/companies", headers=HEADERS, timeout=30)
    soup = BeautifulSoup(resp.text, "lxml")
    companies: list[ScrapedCompany] = []

    for script in soup.find_all("script"):
        text = script.string or ""
        if "company" not in text.lower():
            continue
        matches = re.findall(r'"name"\s*:\s*"([^"]+)"', text)
        for name in matches[:200]:
            companies.append(
                ScrapedCompany(
                    name=name,
                    slug=slugify(name),
                    batch="Unknown",
                    tagline="",
                    industry="Unknown",
                    status="Active",
                    website=None,
                    description=None,
                )
            )
        if companies:
            break

    return companies


def run_scraper() -> list[dict[str, Any]]:
    with httpx.Client(follow_redirects=True) as client:
        companies = scrape_yc_algolia(client)
        if len(companies) < 50:
            print("Algolia returned few results, trying HTML fallback...")
            companies.extend(scrape_yc_html_fallback(client))

    # Deduplicate by slug
    seen: set[str] = set()
    unique: list[ScrapedCompany] = []
    for c in companies:
        if c.slug not in seen:
            seen.add(c.slug)
            unique.append(c)

    out_path = DATA_DIR / "scraped_companies.json"
    out_path.write_text(json.dumps([asdict(c) for c in unique], indent=2))
    print(f"Scraped {len(unique)} companies → {out_path}")
    return [asdict(c) for c in unique]


if __name__ == "__main__":
    run_scraper()
