#!/usr/bin/env python3

import pdfplumber

def pulisci(t):
    if not t: return ""
    return str(t).strip().replace("\n", " ")[:80]

pdf = pdfplumber.open('Piano Settimana Pasti Primavera1.pdf')
page = pdf.pages[1]
tables = page.extract_tables()
table = tables[0]

print("DEBUG - Row 1 (COLAZIONE) tutte le colonne:\n")
for col_idx, cell in enumerate(table[1]):
    if cell:
        print(f"Col {col_idx}: {pulisci(cell)}")

pdf.close()
