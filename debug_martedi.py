#!/usr/bin/env python3

import pdfplumber
import json

def pulisci(t):
    if not t: return ""
    return str(t).strip().replace("\n", " ")[:80]

pdf = pdfplumber.open('Piano Settimana Pasti Primavera1.pdf')
page = pdf.pages[1]  # Settimana 1
tables = page.extract_tables()
table = tables[0]

print("DEBUG SETTIMANA 1 - MARTEDI\n")

# Trova posizione di MARTEDI
for row_idx in range(min(2, len(table))):
    for col_idx, cell in enumerate(table[row_idx]):
        if cell and "MARTEDI" in str(cell).upper():
            print(f"MARTEDI trovato in Row {row_idx}, Col {col_idx}")
            print(f"Testo: {pulisci(cell)}\n")
            
            # Stampa tutte le righe per questa colonna
            print(f"Contenuto di MARTEDI (Col {col_idx}):")
            for r in range(len(table)):
                if table[r] and col_idx < len(table[r]):
                    cell_content = pulisci(table[r][col_idx])
                    if cell_content:
                        print(f"  Row {r}: {cell_content}")
            break

pdf.close()

print("\n" + "="*80)
print("Cosa c'è nel JSON:")
with open('menu_settimanale.json') as f:
    data = json.load(f)

mart = data["PRIMAVERA"]["SETTIMANA_1"]["MARTEDI"]
print("\nMARTEDI nel JSON:")
for pasto, ricetta in mart.items():
    print(f"  {pasto}: {ricetta[:70]}")
