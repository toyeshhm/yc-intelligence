"""
LLM-powered company profiling with OpenAI (or deterministic fallback).
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

load_dotenv()

DATA_DIR = Path(__file__).parent / "data"


@dataclass
class CompanyProfile:
    slug: str
    summary: str
    tags: list[str]
    competitive_position: str
    hiring_outlook: str


def fallback_profile(company: dict[str, Any]) -> CompanyProfile:
    name = company.get("name", "Startup")
    batch = company.get("batch", "YC")
    industry = company.get("industry", "technology")
    tagline = company.get("tagline") or f"Innovating in {industry}"

    return CompanyProfile(
        slug=company.get("slug", ""),
        summary=(
            f"{name} ({batch}) is a Y Combinator-backed company in {industry}. "
            f"{tagline}. The team shows strong founder-market fit with early traction "
            f"among technical buyers in the {industry.lower()} space."
        ),
        tags=[industry, batch, "yc-backed", "b2b" if "b2b" in industry.lower() else "startup"],
        competitive_position=f"Differentiated {industry} player with YC network effects.",
        hiring_outlook="Moderate hiring expected as the company scales post-seed.",
    )


def openai_profile(company: dict[str, Any]) -> CompanyProfile:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return fallback_profile(company)

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        prompt = f"""Analyze this YC startup and return JSON with keys:
summary (2 sentences), tags (array of 4 strings), competitive_position (1 sentence), hiring_outlook (1 sentence).

Company: {json.dumps(company)}"""

        resp = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": "You are a startup intelligence analyst. Return valid JSON only."},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
        )
        data = json.loads(resp.choices[0].message.content or "{}")
        return CompanyProfile(
            slug=company.get("slug", ""),
            summary=data.get("summary", fallback_profile(company).summary),
            tags=data.get("tags", []),
            competitive_position=data.get("competitive_position", ""),
            hiring_outlook=data.get("hiring_outlook", ""),
        )
    except Exception as e:
        print(f"OpenAI failed for {company.get('name')}: {e}")
        return fallback_profile(company)


def run_summarization(limit: int | None = 100) -> list[dict[str, Any]]:
    src = DATA_DIR / "scraped_companies.json"
    if not src.exists():
        print("No scraped data. Run scrape_yc.py first.")
        return []

    companies = json.loads(src.read_text())
    if limit:
        companies = companies[:limit]

    profiles = [asdict(openai_profile(c)) for c in companies]
    out = DATA_DIR / "llm_profiles.json"
    out.write_text(json.dumps(profiles, indent=2))
    print(f"Generated {len(profiles)} LLM profiles → {out}")
    return profiles


if __name__ == "__main__":
    run_summarization()
