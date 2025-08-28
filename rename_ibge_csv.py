import csv
import os
import unicodedata
from pathlib import Path

def slugify(text: str) -> str:
    """Normalize and convert text to a safe filename fragment."""
    normalized = unicodedata.normalize("NFKD", text)
    no_accents = "".join(c for c in normalized if not unicodedata.combining(c))
    safe = no_accents.replace(" ", "_")
    return safe

def extract_fields(path: Path):
    """Return (ibge, municipio) from the first data row of a CSV file."""
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        try:
            row = next(reader)
        except StopIteration:
            return None, None
        headers = {h.lower(): h for h in reader.fieldnames or []}
        ibge_key = next((v for k, v in headers.items() if "ibge" in k), None)
        mun_key = next((v for k, v in headers.items() if "municipio" in k or "munic" in k or "nome" == k), None)
        if not ibge_key or not mun_key:
            return None, None
        return row.get(ibge_key), row.get(mun_key)

def rename_files(directory: str):
    dir_path = Path(directory)
    for csv_file in dir_path.glob("*.csv"):
        ibge, municipio = extract_fields(csv_file)
        if not ibge or not municipio:
            continue
        new_name = f"{ibge}_{slugify(municipio)}.csv"
        target = csv_file.with_name(new_name)
        if target.exists():
            # Skip to avoid overwriting existing files
            continue
        csv_file.rename(target)

if __name__ == "__main__":
    rename_files(os.getcwd())
