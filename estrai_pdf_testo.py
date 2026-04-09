#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pdfplumber

with pdfplumber.open('Piano Settimana Pasti Primavera1.pdf') as pdf:
    for settimana_num, page_num in [(1, 1), (2, 2), (3, 3), (4, 4)]:
        page = pdf.pages[page_num]
        text = page.extract_text()
        print(f"\n\n========== SETTIMANA {settimana_num} ==========\n")
        print(text)
        print("\n" + "="*50)
