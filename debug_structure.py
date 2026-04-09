#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estrae le tabelle dal PDF PRIMAVERA usando le celle di pdfplumber
Analizza le coordinate per capire la struttura della tabella
"""
import pdfplumber
import json

def analyze_page_structure(pdf_path, page_num, settimana_num):
    """Analizza la struttura di una pagina usando le celle della tabella"""
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_num]
        
        # Estrae tutte le tabelle nella pagina
        tables = page.extract_tables()
        
        if not tables:
            print(f"❌ Nessuna tabella trovata in SETTIMANA {settimana_num}")
            return
        
        table = tables[0]
        
        print(f"\n{'='*80}")
        print(f"SETTIMANA {settimana_num} - Struttura tabella:")
        print(f"{'='*80}")
        print(f"Dimensioni: {len(table)} righe × {len(table[0]) if table else 0} colonne\n")
        
        # Stampa la riga dei giorni (solitamente riga 0)
        print("RIGA 0 (Giorni header):")
        for col_idx, cell in enumerate(table[0]):
            print(f"  Col {col_idx}: {cell[:50] if cell else 'EMPTY'}")
        
        print("\n" + "-"*80)
        
        # Stampa le prime 15 righe per capire la struttura
        for row_idx in range(min(15, len(table))):
            print(f"\nRIGA {row_idx}:")
            for col_idx, cell in enumerate(table[row_idx]):
                if cell:  # Solo celle non vuote
                    text = cell.replace('\n', ' ')[:60]
                    print(f"  Col {col_idx}: {text}")

# Analizza tutte e 4 le settimane
pdf_path = 'Piano Settimana Pasti Primavera1.pdf'
for settimana_num, page_num in [(1, 1), (2, 2), (3, 3), (4, 4)]:
    try:
        analyze_page_structure(pdf_path, page_num, settimana_num)
    except Exception as e:
        print(f"❌ Errore SETTIMANA {settimana_num}: {e}")
