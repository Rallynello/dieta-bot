#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estrae il menu PRIMAVERA dal PDF - VERSIONE 3
Usa indici di riga specifici per ogni settimana che ho ricavato dal debug
"""

import json
import pdfplumber

GIORNI = ["LUNEDI", "MARTEDI", "MERCOLEDI", "GIOVEDI", "VENERDI", "SABATO", "DOMENICA"]

# Dalle analisi:
# Settimana 1: Colazione=1, Spuntino=5, Pranzo=6, Spuntino_2=11, Cena=12
# Settimana 2 (pagina 3): Colazione=1, Pranzo=7 (circa), Spuntino_2=13, Cena=14 (circa)
# Settimana 3 (pagina 4): Colazione=2, Pranzo=8, Spuntino_2=13, Cena=14
# Settimana 4 (pagina 5): Colazione=2, Pranzo=8 (circa), Spuntino_2=13, Cena=14 (circa)

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
    print("🌱 ESTRAZIONE PRIMAVERA - VERSIONE 3 (RIGHE HARDCODED)")
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
        
        # Trova posizioni giorni
        giorni_pos = {}
        for row_idx in range(min(3, len(table))):
            for col_idx, cella in enumerate(table[row_idx]):
                if cella:
                    testo = pulisci_testo(cella)
                    for giorno in GIORNI:
                        if giorno in testo.upper():
                            if giorno not in giorni_pos:
                                giorni_pos[giorno] = col_idx
        
        if len(giorni_pos) < 7:
            print(f"   ❌ Trovati solo {len(giorni_pos)} giorni!")
            continue
        
        righe = RIGHE_SETTIMANE[settimana_num]
        
        settimana = {}
        for giorno in GIORNI:
            if giorno not in giorni_pos:
                continue
            
            col_idx = giorni_pos[giorno]
            colonne = [col_idx, col_idx - 1, col_idx + 1]
            
            settimana[giorno] = {
                "colazione": "",
                "spuntino": "1 manciata frutta secca + 2 gallette/wasa",  # Default
                "pranzo": "",
                "spuntino_2": "",
                "cena": ""
            }
            
            # Estrai colazione
            for c in colonne:
                if 0 <= c < len(table[righe["colazione"]]):
                    cella = pulisci_testo(table[righe["colazione"]][c])
                    if cella:
                        settimana[giorno]["colazione"] = cella
                        break
            
            # Estrai pranzo (può essere su più righe)
            for offset in range(0, 5):
                row_idx = righe["pranzo"] + offset
                if row_idx >= len(table):
                    break
                for c in colonne:
                    if 0 <= c < len(table[row_idx]):
                        cella = pulisci_testo(table[row_idx][c])
                        if cella and cella != "-":
                            if settimana[giorno]["pranzo"]:
                                settimana[giorno]["pranzo"] += " " + cella
                            else:
                                settimana[giorno]["pranzo"] = cella
            
            # Estrai spuntino_2
            for c in colonne:
                if 0 <= c < len(table[righe["spuntino_2"]]):
                    cella = pulisci_testo(table[righe["spuntino_2"]][c])
                    if cella and cella != "-":
                        settimana[giorno]["spuntino_2"] = cella
                        break
            
            # Estrai cena (può essere su più righe)
            for offset in range(0, 5):
                row_idx = righe["cena"] + offset
                if row_idx >= len(table):
                    break
                for c in colonne:
                    if 0 <= c < len(table[row_idx]):
                        cella = pulisci_testo(table[row_idx][c])
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
    
    with open('menu_settimanale_completo.json', 'r', encoding='utf-8') as f:
        menu_bot = json.load(f)
    
    menu_bot["PRIMAVERA"] = primavera
    
    with open('menu_settimanale_completo.json', 'w', encoding='utf-8') as f:
        json.dump(menu_bot, f, ensure_ascii=False, indent=2)
    
    print("="*80)
    print("✅ PRIMAVERA integrato!")
    print("="*80 + "\n")

if __name__ == "__main__":
    integra()
