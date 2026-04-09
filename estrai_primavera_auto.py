#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estrae PRIMAVERA dal PDF usando la struttura delle colonne individuate
"""
import pdfplumber
import json
import re

def pulisci_testo(text):
    """Pulisce il testo dalle stringhe sporche"""
    if not text:
        return ""
    # Rimuove spazi multipli e accapo
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)  # Converte multipli spazi in uno
    text = text.replace('ThÞ verde', '').replace('Es. smart', '').replace('Es. camminata', '')
    text = text.replace('¢', '')  # Rimuove caratteri strani
    return text.strip()

def estrai_settimana(pdf_path, page_num, settimana_num):
    """Estrae una settimana usando la struttura della tabella"""
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_num]
        tables = page.extract_tables()
        
        if not tables:
            return None
        
        table = tables[0]
        
        # Identifica le colonne dei giorni (cercando LUNEDI, MARTEDI, ecc)
        giorni_cols = {}
        for col_idx, cell in enumerate(table[0]):
            if cell:
                cell_text = cell.upper()
                for giorno in ['LUNEDI', 'MARTEDI', 'MERCOLEDI', 'GIOVEDI', 'VENERDI', 'SABATO', 'DOMENICA']:
                    if giorno in cell_text:
                        giorni_cols[giorno] = col_idx
                        break
        
        print(f"\nSETTIMANA {settimana_num} - Colonne giorni identificate:")
        print(giorni_cols)
        
        # Identifica le righe dei pasti
        # La riga "Colazione" è sempre nella prima, "Pranzo" dopo, "Cena" dopo
        colazione_row = None
        pranzo_row = None
        cena_row = None
        spuntino_row = None
        spuntino2_row = None
        
        for row_idx, row in enumerate(table):
            row_text = ' '.join([str(c) for c in row if c])
            if 'Colazione' in row_text and colazione_row is None:
                colazione_row = row_idx
            elif 'Pranzo' in row_text and pranzo_row is None:
                pranzo_row = row_idx
            elif 'Cena' in row_text and cena_row is None:
                cena_row = row_idx
        
        print(f"Righe pasti: Colazione={colazione_row}, Pranzo={pranzo_row}, Cena={cena_row}")
        
        # Estrai i dati
        settimana_data = {}
        
        for giorno, col_idx in sorted(giorni_cols.items(), key=lambda x: x[1]):
            # Estrai colazione (raccoglie le righe consecutive da colazione_row)
            colazione = ""
            if colazione_row:
                for r in range(colazione_row, min(colazione_row + 5, len(table))):
                    if table[r][col_idx]:
                        cell_text = pulisci_testo(table[r][col_idx])
                        if cell_text and cell_text != '-':
                            colazione += " " + cell_text
                            # Ferma se legge un'altra sezione
                            if any(x in cell_text.lower() for x in ['spuntino', 'pranzo', 'cena']):
                                colazione = colazione.rsplit(' ', 1)[0]  # Rimuove l'ultima parola
                                break
            
            # Estrai pranzo
            pranzo = ""
            if pranzo_row:
                for r in range(pranzo_row, min(pranzo_row + 6, len(table))):
                    if col_idx < len(table[r]) and table[r][col_idx]:
                        cell_text = pulisci_testo(table[r][col_idx])
                        if cell_text and cell_text != '-':
                            pranzo += " " + cell_text
                            # Ferma se legge un'altra sezione
                            if any(x in cell_text.lower() for x in ['spuntino', 'cena']):
                                pranzo = pranzo.rsplit(' ', 1)[0]
                                break
            
            # Estrai cena
            cena = ""
            if cena_row:
                for r in range(cena_row, min(cena_row + 5, len(table))):
                    if col_idx < len(table[r]) and table[r][col_idx]:
                        cell_text = pulisci_testo(table[r][col_idx])
                        if cell_text and cell_text != '-':
                            cena += " " + cell_text
            
            settimana_data[giorno] = {
                "colazione": pulisci_testo(colazione),
                "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": pulisci_testo(pranzo),
                "spuntino_2": "1 frutto + 1 pezzo cioccolato",  # Placeholder
                "cena": pulisci_testo(cena)
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
    except Exception as e:
        print(f"ERRORE SETTIMANA {settimana_num}: {e}")

# Stampa i risultati
print("\n" + "="*80)
print("RISULTATI ESTRAPOLATI:")
print("="*80)
print(json.dumps(primavera_completa, indent=2, ensure_ascii=False))
