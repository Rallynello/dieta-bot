#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estrae il menu PRIMAVERA - VERSIONE 4
Con parsing intelligente che cerca i dati nella riga specifica
"""

import json
import pdfplumber

GIORNI = ["LUNEDI", "MARTEDI", "MERCOLEDI", "GIOVEDI", "VENERDI", "SABATO", "DOMENICA"]

# Righe hardcoded per ogni settimana
RIGHE_SETTIMANE = {
    1: {"colazione": 1, "pranzo": 6, "spuntino_2": 11, "cena": 12},
    2: {"colazione": 1, "pranzo": 7, "spuntino_2": 13, "cena": 14},
    3: {"colazione": 2, "pranzo": 8, "spuntino_2": 13, "cena": 14},
    4: {"colazione": 2, "pranzo": 8, "spuntino_2": 13, "cena": 14},
}

def pulisci_testo(testo):
    if not testo:
        return ""
    testo = str(testo).strip()
    if testo == "None":
        return ""
    testo = testo.replace("\n", " ")
    while "  " in testo:
        testo = testo.replace("  ", " ")
    return testo.strip()

def estrai_primavera():
    print("\n" + "="*80)
    print("🌱 ESTRAZIONE PRIMAVERA - VERSIONE 4 (PARSING INTELLIGENTE)")
    print("="*80 + "\n")
    
    pdf = pdfplumber.open('Piano Settimana Pasti Primavera1.pdf')
    
    settimane = {}
    pagine_settimane = [1, 2, 3, 4]
    
    for settimana_num, page_idx in enumerate(pagine_settimane, 1):
        print(f"📖 SETTIMANA {settimana_num} (Pagina {page_idx + 1})")
        
        page = pdf.pages[page_idx]
        tables = page.extract_tables()
        
        if not tables or not tables[0]:
            print(f"   ❌ Nessuna tabella!")
            continue
        
        table = tables[0]
        
        # Trova posizioni giorni ESATTE (dalla riga 0-2)
        giorni_pos = {}
        for row_idx in range(min(3, len(table))):
            for col_idx, cella in enumerate(table[row_idx]):
                if cella:
                    testo = pulisci_testo(cella)
                    for giorno in GIORNI:
                        if giorno in testo.upper() and giorno not in giorni_pos:
                            giorni_pos[giorno] = col_idx
        
        if len(giorni_pos) < 7:
            print(f"   ❌ Trovati solo {len(giorni_pos)} giorni!")
            continue
        
        righe = RIGHE_SETTIMANE[settimana_num]
        
        settimana = {}
        for giorno in GIORNI:
            if giorno not in giorni_pos:
                continue
            
            col_header = giorni_pos[giorno]
            
            settimana[giorno] = {
                "colazione": "",
                "spuntino": "1 manciata frutta secca + 2 gallette/wasa",  # Default
                "pranzo": "",
                "spuntino_2": "",
                "cena": ""
            }
            
            # Per ogni pasto, cerca nella riga specifica
            # Prova prima la colonna esatta, poi le adiacenti
            
            # COLAZIONE (può essere su più righe)
            row_idx = righe["colazione"]
            for offset in range(0, 5):  # Accumula fino a 5 righe
                r = row_idx + offset
                if r >= len(table):
                    break
                
                # Prova colonna esatta e adiacenti
                for col_offset in range(-1, 2):
                    c = col_header + col_offset
                    if 0 <= c < len(table[r]):
                        cella = pulisci_testo(table[r][c])
                        if cella and "colazione" not in cella.lower():
                            if settimana[giorno]["colazione"]:
                                settimana[giorno]["colazione"] += " " + cella
                            else:
                                settimana[giorno]["colazione"] = cella
            
            # PRANZO (può essere su più righe)
            row_idx = righe["pranzo"]
            for offset in range(0, 5):
                r = row_idx + offset
                if r >= len(table):
                    break
                
                # Prova colonna esatta e adiacenti
                for col_offset in range(-1, 2):
                    c = col_header + col_offset
                    if 0 <= c < len(table[r]):
                        cella = pulisci_testo(table[r][c])
                        if cella and cella != "-":
                            if settimana[giorno]["pranzo"]:
                                settimana[giorno]["pranzo"] += " " + cella
                            else:
                                settimana[giorno]["pranzo"] = cella
            
            # SPUNTINO_2 (row 11 o specifica per settimana)
            row_idx = righe["spuntino_2"]
            for col_offset in range(-1, 2):
                c = col_header + col_offset
                if 0 <= c < len(table[row_idx]):
                    cella = pulisci_testo(table[row_idx][c])
                    if cella and cella != "-":
                        settimana[giorno]["spuntino_2"] = cella
                        break
            
            # CENA (può essere su più righe)
            row_idx = righe["cena"]
            for offset in range(0, 5):
                r = row_idx + offset
                if r >= len(table):
                    break
                
                # Prova colonna esatta e adiacenti
                for col_offset in range(-1, 2):
                    c = col_header + col_offset
                    if 0 <= c < len(table[r]):
                        cella = pulisci_testo(table[r][c])
                        if cella and cella != "-":
                            if settimana[giorno]["cena"]:
                                settimana[giorno]["cena"] += " " + cella
                            else:
                                settimana[giorno]["cena"] = cella
        
        settimane[f"SETTIMANA_{settimana_num}"] = settimana
        print(f"   ✅ Estratto\n")
    
    pdf.close()
    return settimane

def integra():
    with open('menu_settimanale.json', 'r', encoding='utf-8') as f:
        menu = json.load(f)
    
    primavera = estrai_primavera()
    menu["PRIMAVERA"] = primavera
    
    with open('menu_settimanale.json', 'w', encoding='utf-8') as f:
        json.dump(menu, f, ensure_ascii=False, indent=2)
    
    print("="*80)
    print("✅ PRIMAVERA integrato!")
    print("="*80 + "\n")

if __name__ == "__main__":
    integra()
