#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estrae il testo grezzo da PRIMAVERA PDF e lo analizza per giorno
"""

import pdfplumber

pdf = pdfplumber.open('Piano Settimana Pasti Primavera1.pdf')

for settimana_num, page_idx in enumerate([1, 2, 3, 4], 1):
    print(f"\n{'='*80}")
    print(f"SETTIMANA {settimana_num} - TESTO GREZZO (Pagina {page_idx + 1})")
    print(f"{'='*80}\n")
    
    page = pdf.pages[page_idx]
    text = page.extract_text()
    
    print(text)
    print("\n" + "-"*80)

pdf.close()
