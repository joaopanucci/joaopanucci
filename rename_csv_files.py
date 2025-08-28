import csv
import unicodedata
from pathlib import Path

def slugify(value: str) -> str:
    """Simplify a string for filenames: remove accents, spaces and keep alphanumerics."""
    normalized = unicodedata.normalize('NFKD', value)
    ascii_str = normalized.encode('ascii', 'ignore').decode('ascii')
    ascii_str = ascii_str.replace(' ', '_').lower()
    return ''.join(ch for ch in ascii_str if ch.isalnum() or ch in {'_', '-'})


def extract_data(csv_path: Path):
    """Extract IBGE and municipality name from the first data row of a CSV file."""
    with csv_path.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        try:
            row = next(reader)
        except StopIteration:
            raise ValueError(f"Arquivo vazio: {csv_path}")
    # normalize keys to lowercase for case-insensitive matching
    row_norm = {k.lower(): v for k, v in row.items()}
    ibge = row_norm.get('ibge') or row_norm.get('codigo_ibge') or row_norm.get('codigo')
    municipio = (
        row_norm.get('municipio')
        or row_norm.get('nome')
        or row_norm.get('cidade')
    )
    if not ibge or not municipio:
        raise ValueError(f"Campos IBGE e municipio nao encontrados em {csv_path}")
    return ibge.strip(), municipio.strip()


def rename_csv_files(directory: str = '.'):    
    for csv_file in Path(directory).glob('*.csv'):
        ibge, municipio = extract_data(csv_file)
        new_name = f"{ibge}-{slugify(municipio)}.csv"
        new_path = csv_file.with_name(new_name)
        csv_file.rename(new_path)
        print(f"{csv_file.name} -> {new_name}")


if __name__ == '__main__':
    rename_csv_files()
