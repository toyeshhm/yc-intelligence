"""
Entity extraction from scraped company text using regex + optional spaCy NER.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).parent / "data"

ROUND_PATTERNS = [
    (r"series\s+([a-e])", "Series {}"),
    (r"seed\s+round", "Seed"),
    (r"pre-?seed", "Pre-Seed"),
]

INVESTOR_PATTERN = re.compile(
    r"\b(Sequoia|a16z|Benchmark|Accel|Greylock|Founders Fund|Y Combinator|"
    r"Lightspeed|Tiger Global|Index Ventures|General Catalyst)\b",
    re.I,
)

FOUNDER_PATTERN = re.compile(
    r"([A-Z][a-z]+ [A-Z][a-z]+)(?:,|\s+—|\s+-)\s*(CEO|CTO|Co-?founder|Founder)",
    re.I,
)

EDU_PATTERN = re.compile(
    r"\b(Stanford|MIT|Harvard|Berkeley|CMU|Caltech|Princeton|Yale|Columbia)\b"
)

_nlp = None


def _get_nlp():
    global _nlp
    if _nlp is not None:
        return _nlp
    try:
        import spacy

        _nlp = spacy.load("en_core_web_sm")
    except Exception:
        _nlp = False
    return _nlp


def extract_orgs_with_spacy(text: str) -> list[str]:
    nlp = _get_nlp()
    if not nlp:
        return []
    doc = nlp(text[:5000])
    return list({ent.text for ent in doc.ents if ent.label_ in ("ORG", "GPE")})


@dataclass
class ExtractedEntities:
    slug: str
    funding_rounds: list[dict[str, Any]]
    investors: list[str]
    founders: list[dict[str, str]]
    education: list[str]
    hiring_signals: dict[str, Any]


def extract_from_company(company: dict[str, Any]) -> ExtractedEntities:
    text = " ".join(
        filter(
            None,
            [
                company.get("name", ""),
                company.get("tagline", ""),
                company.get("description", ""),
            ],
        )
    )

    rounds: list[dict[str, Any]] = []
    for pattern, label in ROUND_PATTERNS:
        if re.search(pattern, text, re.I):
            rounds.append({"round_type": label.format("A") if "{}" in label else label, "source": "regex"})

    investors = list({m.group(0) for m in INVESTOR_PATTERN.finditer(text)})
    spacy_orgs = extract_orgs_with_spacy(text)
    for org in spacy_orgs[:3]:
        if org not in investors and len(org) > 2:
            investors.append(org)

    founders = [
        {"name": m.group(1), "role": m.group(2)}
        for m in FOUNDER_PATTERN.finditer(text)
    ]
    education = list({m.group(0) for m in EDU_PATTERN.finditer(text)})

    hiring = {
        "is_hiring": bool(re.search(r"\bhiring\b|\bcareers\b|\bopen roles\b", text, re.I)),
        "open_roles_estimate": len(re.findall(r"\b(engineer|designer|sales|marketing)\b", text, re.I)),
    }

    return ExtractedEntities(
        slug=company.get("slug", ""),
        funding_rounds=rounds,
        investors=investors,
        founders=founders,
        education=education,
        hiring_signals=hiring,
    )


def run_extraction() -> list[dict[str, Any]]:
    src = DATA_DIR / "scraped_companies.json"
    if not src.exists():
        print("No scraped data found. Run scrape_yc.py first.")
        return []

    companies = json.loads(src.read_text())
    results = [asdict(extract_from_company(c)) for c in companies]
    out = DATA_DIR / "extracted_entities.json"
    out.write_text(json.dumps(results, indent=2))
    nlp = _get_nlp()
    mode = "regex + spaCy NER" if nlp else "regex only"
    print(f"Extracted entities for {len(results)} companies ({mode}) → {out}")
    return results


if __name__ == "__main__":
    run_extraction()
