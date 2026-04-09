#!/usr/bin/env python3

import pdfplumber

def pulisci(t):
    if not t: return ""
    return str(t).strip().replace("\n", " ")

pdf = pdfplumber.open('Piano Settimana Pasti Primavera1.pdf')
page = pdf.pages[1]
tables = page.extract_tables()
table = tables[0]

print("Righe 1-6, Colonna 3 (MARTEDI COLAZIONE):\n")
for row_idx in range(1, 6):
    if row_idx < len(table):
        cell = table[row_idx][3] if 3 < len(table[row_idx]) else None
        if cell:
            print(f"Row {row_idx}: {pulisci(cell)}")

pdf.close()
