#!/usr/bin/env python3
"""Crawl design galleries (Dribbble, Firecrawl) and save images + metadata.

Writes output to `../apps/web/data/designs.json` relative to the pipeline folder.
Uses Playwright for JS-heavy pages and falls back to requests+BeautifulSoup.
"""
import json
import os
from pathlib import Path

OUT_PATH = Path(__file__).resolve().parents[1] / "apps" / "web" / "data" / "designs.json"
DEFAULT_SOURCES = [
    "https://dribbble.com/shots",
    # add Firecrawl or other gallery URLs here
]


def ensure_out_dir():
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)


def write_output(items):
    ensure_out_dir()
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(items)} designs to {OUT_PATH}")


def scrape_with_requests(urls):
    from httpx import get
    from bs4 import BeautifulSoup

    results = []
    for url in urls:
        print("Fetching (requests):", url)
        try:
            r = get(url, timeout=20)
            r.raise_for_status()
        except Exception as e:
            print("Request failed:", e)
            continue
        soup = BeautifulSoup(r.text, "lxml")
        imgs = soup.select("img")
        for img in imgs[:40]:
            src = img.get("src") or img.get("data-src")
            alt = img.get("alt") or ""
            if not src:
                continue
            results.append({"source": url, "image": src, "title": alt})
    return results


def scrape_with_playwright(urls):
    try:
        from playwright.sync_api import sync_playwright
    except Exception as e:
        print("Playwright not available:", e)
        return []

    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        for url in urls:
            print("Visiting:", url)
            try:
                page.goto(url, timeout=30000)
            except Exception as e:
                print("Playwright goto failed:", e)
                continue
            # try to gather shot links and thumbnails
            # generic image selector
            imgs = page.query_selector_all("img")
            count = 0
            for im in imgs:
                if count >= 40:
                    break
                try:
                    src = im.get_attribute("src") or im.get_attribute("data-src")
                    alt = im.get_attribute("alt") or ""
                except Exception:
                    continue
                if not src:
                    continue
                results.append({"source": url, "image": src, "title": alt})
                count += 1
        browser.close()
    return results


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--out", help="output path override", default=str(OUT_PATH))
    parser.add_argument("--sources", nargs="*", help="list of URLs to crawl", default=DEFAULT_SOURCES)
    args = parser.parse_args()

    urls = args.sources
    items = []

    # try Playwright first
    try:
        items = scrape_with_playwright(urls)
    except Exception as e:
        print("Playwright scrape failed, falling back to requests:", e)
        items = scrape_with_requests(urls)

    if not items:
        print("No items found with Playwright, trying requests fallback")
        items = scrape_with_requests(urls)

    # dedupe by image URL
    seen = set()
    dedup = []
    for it in items:
        if it["image"] in seen:
            continue
        seen.add(it["image"])
        dedup.append(it)

    # write to provided out path if different
    outp = Path(args.out)
    ensure_out_dir()
    with open(outp, "w", encoding="utf-8") as f:
        json.dump(dedup, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(dedup)} items to {outp}")


if __name__ == "__main__":
    main()
