#!/usr/bin/env python3
"""Import pipeline export into the Next.js SQLite database."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
WEB = ROOT / "apps" / "web"
EXPORT = Path(__file__).parent / "data" / "pipeline_export.json"


def main() -> int:
    if not EXPORT.exists():
        print(f"Export not found: {EXPORT}. Run the pipeline first.")
        return 1

    replace = "--replace" in sys.argv or "--no-replace" not in sys.argv
    cmd = ["npm", "run", "db:import", "--", str(EXPORT)]
    if replace:
        cmd.append("--replace")

    print(f"Importing {EXPORT} into SQLite...")
    result = subprocess.run(cmd, cwd=WEB, check=False)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
