#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estrae PRIMAVERA dal PDF con logica migliorata per spuntino_2
Estrae ogni sezione dalle righe specifiche
"""
import pdfplumber
import json
import re

def pulisci_testo(text):
    """Pulisce il testo dalle stringhe sporche"""
    if not text:
        return ""
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('ThÞ verde', '').replace('Es. smart', '').replace('Es. camminata', '')
    text = text.replace('¢', '').replace('  ', ' ').strip()
    return text

def estrai_cella_multiriga(table, start_row, col_idx, max_rows=5):
    """Estrae il contenuto di una cella che può spannarsi su più righe"""
    result = ""
    for r in range(start_row, min(start_row + max_rows, len(table))):
        if col_idx < len(table[r]) and table[r][col_idx]:
            cell_text = pulisci_testo(table[r][col_idx])
            if cell_text:
                result += " " + cell_text
            # Se la cella è vuota, stop (fine della sezione)
            elif result:
                break
    return pulisci_testo(result)

def estrai_settimana(pdf_path, page_num, settimana_num):
    """Estrae una settimana con logica per sezioni multi-riga"""
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_num]
        tables = page.extract_tables()
        
        if not tables:
            return None
        
        table = tables[0]
        
        # Trova colonne dei giorni
        giorni_cols = {}
        for col_idx, cell in enumerate(table[0]):
            if cell:
                cell_upper = cell.upper()
                for giorno in ['LUNEDI', 'MARTEDI', 'MERCOLEDI', 'GIOVEDI', 'VENERDI', 'SABATO', 'DOMENICA']:
                    if giorno in cell_upper:
                        giorni_cols[giorno] = col_idx
                        break
        
        # Trova righe delle sezioni
        colazione_row = None
        spuntino_row = None
        pranzo_row = None
        spuntino2_row = None
        cena_row = None
        
        for row_idx, row in enumerate(table):
            row_text = ' '.join([str(c) for c in row if c]).upper()
            if 'COLAZIONE' in row_text and colazione_row is None:
                colazione_row = row_idx
            elif 'SPUNTINO' in row_text and 'PRANZO' not in row_text and spuntino_row is None:
                spuntino_row = row_idx
            elif 'PRANZO' in row_text and pranzo_row is None:
                pranzo_row = row_idx
            elif 'CENA' in row_text and cena_row is None:
                cena_row = row_idx
        
        # Identifica spuntino_2 cercandonela colonna 0 tra pranzo e cena
        if pranzo_row and cena_row:
            for row_idx in range(pranzo_row + 1, cena_row):
                if table[row_idx][0]:
                    row_text = str(table[row_idx][0]).upper()
                    if 'SPUNTINO' in row_text:
                        spuntino2_row = row_idx
                        break
        
        # Estrai i dati
        settimana_data = {}
        
        for giorno_sort, (giorno, col_idx) in enumerate(sorted(giorni_cols.items(), key=lambda x: ['LUNEDI', 'MARTEDI', 'MERCOLEDI', 'GIOVEDI', 'VENERDI', 'SABATO', 'DOMENICA'].index(x[0]))):
            # Colazione: da colazione_row fino a spuntino_row (esclusivo)
            colazione = ""
            if colazione_row and spuntino_row:
                colazione = estrai_cella_multiriga(table, colazione_row, col_idx, spuntino_row - colazione_row)
            
            # Pranzo: da pranzo_row fino a spuntino2_row o cena_row
            pranzo = ""
            if pranzo_row:
                max_rows = (spuntino2_row - pranzo_row) if spuntino2_row else (cena_row - pranzo_row if cena_row else 6)
                pranzo = estrai_cella_multiriga(table, pranzo_row, col_idx, max(max_rows, 3))
            
            # Spuntino 2: nella riga spuntino2_row
            spuntino2 = ""
            if spuntino2_row and col_idx < len(table[spuntino2_row]):
                spuntino2 = pulisci_testo(table[spuntino2_row][col_idx])
            
            # Cena: da cena_row in poi
            cena = ""
            if cena_row:
                cena = estrai_cella_multiriga(table, cena_row, col_idx, 5)
            
            settimana_data[giorno] = {
                "colazione": colazione,
                "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": pranzo,
                "spuntino_2": spuntino2 if spuntino2 else "1 frutto + 1 pezzo cioccolato",
                "cena": cena
            }
        
        return settimana_data

# Estrai tutte le settimane
pdf_path = 'Piano Settimana Pasti Primavera1.pdf'
primavera_completa = {}

for settimana_num, page_num in [(1, 1), (2, 2), (3, 3), (4, 4)]:
    try:
        data = estrai_settimana(pdf_path, page_num, settimana_num)
        if data:
            primavera_completa[f"SETTIMANA_{settimana_num}"] = data
            print(f"OK SETTIMANA {settimana_num}")
    except Exception as e:
        print(f"ERRORE SETTIMANA {settimana_num}: {e}")
        import traceback
        traceback.print_exc()

# Stampa i risultati
print("\n" + "="*80)
print("RISULTATI - Solo SETTIMANA 1 (verifica):")
print("="*80)
settimana1 = primavera_completa.get("SETTIMANA_1", {})
for giorno in ['LUNEDI', 'MARTEDI', 'MERCOLEDI']:
    print(f"\n{giorno}:")
    for k, v in settimana1.get(giorno, {}).items():
        print(f"  {k}: {v[:70] if v else 'EMPTY'}...")
