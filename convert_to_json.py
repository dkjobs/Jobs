#!/usr/bin/env python3
"""
DKJOBS — Konverter XLSX/CSV til JSON til brug på GitHub Pages
-------------------------------------------------------------
Krav:  pip install pandas openpyxl
Brug:  python convert_to_json.py din_fil.xlsx
       python convert_to_json.py din_fil.csv

Output: en JSON-fil klar til upload i data/ mappen på GitHub.
        Opdatér derefter data/manifest.json manuelt.
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime, date

def safe_str(val, max_len=None):
    if val is None:
        return ""
    s = str(val).strip()
    if max_len:
        s = s[:max_len]
    return s

def parse_date(val):
    """Return ISO date string or empty string."""
    if not val:
        return ""
    if isinstance(val, (datetime, date)):
        return val.strftime("%Y-%m-%d")
    s = str(val).strip()
    # Try common formats
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(s[:10], fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return s[:10]  # best-effort

def convert(input_path: Path) -> Path:
    try:
        import pandas as pd
    except ImportError:
        print("Fejl: pandas ikke installeret. Kør:  pip install pandas openpyxl")
        sys.exit(1)

    suffix = input_path.suffix.lower()
    print(f"Indlæser {input_path.name} …")

    if suffix == ".csv":
        df = pd.read_csv(input_path, dtype=str, encoding="utf-8-sig")
    elif suffix in (".xlsx", ".xlsm"):
        df = pd.read_excel(input_path, dtype=str)
    else:
        print(f"Fejl: Understøtter ikke filtype '{suffix}'. Brug .xlsx eller .csv")
        sys.exit(1)

    df = df.where(pd.notnull(df), None)
    print(f"  {len(df)} rækker fundet")

    records = []
    for _, row in df.iterrows():
        r = row.to_dict()
        record = {
            "job_id":          safe_str(r.get("job_id") or r.get("id")),
            "job_title":       safe_str(r.get("job_title") or r.get("title"), 120),
            "company_name":    safe_str(r.get("company_name") or r.get("company"), 80),
            "job_url":         safe_str(r.get("job_url") or r.get("url")),
            "job_category":    safe_str(r.get("job_category") or r.get("category")),
            "job_type":        safe_str(r.get("job_type")),
            "employment_form": safe_str(r.get("employment_form") or r.get("employment")),
            "town":            safe_str(r.get("town") or r.get("city")),
            "region":          safe_str(r.get("region")),
            "application_date": parse_date(r.get("application_date")),
            "created_date":     parse_date(r.get("created_date")),
            "gpt_context":     safe_str(r.get("gpt_context") or r.get("description"), 300),
        }
        # Only keep jobs that have at least a title or URL
        if record["job_title"] or record["job_url"]:
            records.append(record)

    output_path = input_path.with_suffix(".json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    print(f"  {len(records)} jobopslag gemt → {output_path.name}")
    print()
    print("Næste skridt:")
    print(f"  1. Upload '{output_path.name}' til mappen 'data/' i dit GitHub-repo")
    print(f"  2. Opdatér 'data/manifest.json' — tilføj en linje som denne:")
    print()
    stem = input_path.stem
    today = datetime.today().strftime("%-d. %B %Y").replace(
        "January","januar").replace("February","februar").replace("March","marts") \
        .replace("April","april").replace("May","maj").replace("June","juni") \
        .replace("July","juli").replace("August","august").replace("September","september") \
        .replace("October","oktober").replace("November","november").replace("December","december")
    entry = {
        "name": stem.replace("_", " ").title(),
        "filename": output_path.name,
        "date": today
    }
    print('    ' + json.dumps(entry, ensure_ascii=False))
    print()
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    p = Path(sys.argv[1])
    if not p.exists():
        print(f"Fejl: Filen '{p}' findes ikke")
        sys.exit(1)

    convert(p)
