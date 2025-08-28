import csv
import os
import tkinter as tk
from tkinter import filedialog, messagebox


def extract_info_from_csv(file_path):
    """Read IBGE code and municipality name from the first row of a CSV file."""
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            first_row = next(reader, None)
            if first_row and len(first_row) >= 2:
                ibge = first_row[0].strip()
                municipality = first_row[1].strip()
                return ibge, municipality
    except Exception as exc:  # Catch broad exceptions to show feedback in GUI
        messagebox.showerror("Erro ao ler arquivo", f"{os.path.basename(file_path)}: {exc}")
    return None, None


def rename_csv_files(file_paths):
    """Rename CSV files using IBGE code and municipality name inside each file."""
    for path in file_paths:
        ibge, municipality = extract_info_from_csv(path)
        if ibge and municipality:
            directory = os.path.dirname(path)
            new_name = f"{ibge}_{municipality}.csv"
            new_path = os.path.join(directory, new_name)
            try:
                os.rename(path, new_path)
            except OSError as exc:
                messagebox.showerror("Erro ao renomear", f"{os.path.basename(path)}: {exc}")


def choose_and_rename():
    file_paths = filedialog.askopenfilenames(
        title="Selecione arquivos CSV",
        filetypes=[("CSV Files", "*.csv")],
    )
    if file_paths:
        rename_csv_files(file_paths)
        messagebox.showinfo("Concluído", "Arquivos renomeados com sucesso!")


def main():
    root = tk.Tk()
    root.title("Renomear CSVs")
    root.geometry("300x120")

    btn = tk.Button(root, text="Selecionar CSVs", command=choose_and_rename)
    btn.pack(pady=40)

    root.mainloop()


if __name__ == "__main__":
    main()
