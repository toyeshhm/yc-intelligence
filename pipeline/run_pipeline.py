#!/usr/bin/env python3
"""
End-to-end data pipeline: scrape → extract → summarize → export
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from rich.console import Console
from rich.progress import track

from scrape_yc import run_scraper
from extract_entities import run_extraction
from summarize import run_summarization
from import_to_db import main as import_to_db

console = Console()
DATA_DIR = Path(__file__).parent / "data"


def merge_and_export() -> Path:
    companies = json.loads((DATA_DIR / "scraped_companies.json").read_text())
    entities_path = DATA_DIR / "extracted_entities.json"
    profiles_path = DATA_DIR / "llm_profiles.json"

    entities = {}
    if entities_path.exists():
        entities = {e["slug"]: e for e in json.loads(entities_path.read_text())}

    profiles = {}
    if profiles_path.exists():
        profiles = {p["slug"]: p for p in json.loads(profiles_path.read_text())}

    merged = []
    for c in companies:
        slug = c.get("slug", "")
        merged.append({
            **c,
            "entities": entities.get(slug, {}),
            "llm_profile": profiles.get(slug, {}),
            "pipeline_version": "1.0",
            "processed_at": datetime.now(timezone.utc).isoformat(),
        })

    out = DATA_DIR / "pipeline_export.json"
    out.write_text(json.dumps(merged, indent=2))
    return out


def main() -> int:
    console.print("[bold orange1]YC Intelligence Pipeline[/]")
    steps = [
        ("Scraping YC directory", run_scraper),
        ("Extracting entities", run_extraction),
        ("LLM summarization", lambda: run_summarization(limit=200)),
    ]

    for label, fn in track(steps, description="Running pipeline..."):
        console.print(f"  → {label}")
        fn()

    export_path = merge_and_export()
    console.print(f"\n[green]✓ Export complete[/] → {export_path}")
    console.print(f"  Companies processed: {len(json.loads(export_path.read_text()))}")

    console.print("  → Importing to SQLite database")
    import_code = import_to_db()
    if import_code != 0:
        console.print("[yellow]⚠ DB import failed — run manually: npm run db:import[/]")
        return import_code

    console.print("[green]✓ Pipeline complete[/] (scrape → extract → summarize → import)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
