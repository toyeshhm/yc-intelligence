# YC Intel — Open-Source YC Company Intelligence Platform

Track **5,000+ Y Combinator startups** with automated data pipelines, entity extraction, LLM-powered company profiling, and an analytics dashboard.

## Features

| Module | Description |
|--------|-------------|
| **Startup Directory** | Search & filter by batch, industry, hiring status |
| **Funding Intelligence** | Round tracking, annual volume, industry capital maps |
| **Hiring Trends** | Monthly open-role aggregates, industry heatmaps, hiring leaders |
| **Founder Profiles** | Background extraction, pedigree analysis, prior employers |
| **Data Pipeline** | Python scraper → NER/regex entity extraction → LLM summaries → SQLite import |
| **Pipeline Monitor** | Run history, status, and import progress |
| **Analytics Dashboard** | Interactive charts powered by Recharts |

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  scrape_yc.py   │────▶│ extract_entities │────▶│  summarize.py   │
│  (YC directory) │     │  (regex + NER)   │     │  (OpenAI/local) │
└────────┬────────┘     └────────┬─────────┘     └────────┬────────┘
         │                       │                        │
         └───────────────────────┴────────────────────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │  pipeline_export.json  │
                    └───────────┬────────────┘
                                │
                                ▼
                    ┌────────────────────────┐
                    │  import-pipeline.ts    │
                    │  SQLite + Drizzle ORM  │
                    └───────────┬────────────┘
                                │
                                ▼
                    ┌────────────────────────┐
                    │  Next.js Dashboard     │
                    │  /dashboard/*          │
                    └────────────────────────┘
```

## Quick Start

### Option A: Demo Dashboard (synthetic data)

```bash
cd apps/web
npm install
npm run db:setup    # Seeds 5,200 startups + related data (~30s)
npm run dev         # http://localhost:3000
```

### Option B: Live YC Data Pipeline

```bash
# From repo root — scrape, extract, summarize, import
npm run pipeline:import

cd apps/web && npm run dev
```

Or step-by-step:

```bash
cd pipeline
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env   # Optional: OPENAI_API_KEY for live LLM profiles

python run_pipeline.py    # scrape → extract → summarize → import

cd ../apps/web && npm run dev
```

## Project Structure

```
yc-intelligence/
├── apps/web/                 # Next.js 16 dashboard + API
│   ├── src/app/dashboard/    # Analytics pages
│   ├── src/lib/db/           # Drizzle schema + seed
│   ├── scripts/seed.ts       # Synthetic data generator
│   └── scripts/import-pipeline.ts  # Pipeline → SQLite import
├── pipeline/                 # Python ETL
│   ├── scrape_yc.py
│   ├── extract_entities.py
│   ├── summarize.py
│   ├── import_to_db.py
│   └── run_pipeline.py
└── README.md
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/analytics` | Overview stats, charts data |
| `GET /api/startups?q=&batch=&industry=&hiring=` | Paginated search |
| `GET /api/startups/[slug]` | Company detail + founders + rounds |
| `GET /api/pipeline` | Pipeline run history and latest status |

## Data Sources

| Source | Description |
|--------|-------------|
| **Seed data** | 5,200 synthetic companies for instant demo (`npm run db:setup`) |
| **Live pipeline** | Real YC directory via Algolia API (`npm run pipeline:import`) |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | SQLite path (default: `./data/yc-intelligence.db`) |
| `OPENAI_API_KEY` | Optional — enables live LLM profiling in pipeline |
| `OPENAI_MODEL` | OpenAI model (default: `gpt-4o-mini`) |
| `NEXT_PUBLIC_GITHUB_URL` | GitHub repo URL for landing page link |

## Tech Stack

- **Frontend:** Next.js 16, React 19, Tailwind CSS 4, Recharts
- **Database:** SQLite, Drizzle ORM, better-sqlite3
- **Pipeline:** Python, httpx, BeautifulSoup, OpenAI SDK, optional spaCy NER
- **Design:** DM Sans + Instrument Serif, dark editorial theme

## License

MIT — open source, free to fork and extend.
