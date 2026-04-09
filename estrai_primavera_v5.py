#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estrae il menu PRIMAVERA - VERSIONE 5
Parsing intelligente che NON mescola dati di giorni diversi
"""

import json
import pdfplumber

GIORNI = ["LUNEDI", "MARTEDI", "MERCOLEDI", "GIOVEDI", "VENERDI", "SABATO", "DOMENICA"]

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

def estrai_pasto_multiriga(table, col_idx, start_row, end_row):
    """Estrae un pasto da una riga iniziale, accumulando righe successive se continuano nella stessa colonna"""
    testo_completo = ""
    
    for row_idx in range(start_row, min(end_row, len(table))):
        cella = pulisci_testo(table[row_idx][col_idx]) if col_idx < len(table[row_idx]) else ""
        
        # Se la cella è vuota, fermiamo (probabilmente fine di questo pasto)
        if not cella or cella == "-":
            # Ma continua se è solo una riga di transizione
            if testo_completo and row_idx < start_row + 1:
                break
            continue
        
        if testo_completo:
            testo_completo += " " + cella
        else:
            testo_completo = cella
    
    return testo_completo

def estrai_primavera():
    print("\n" + "="*80)
    print("🌱 ESTRAZIONE PRIMAVERA - VERSIONE 5 (PARSING CONSERVATIVO)")
    print("="*80 + "\n")
    
    pdf = pdfplumber.open('Piano Settimana Pasti Primavera1.pdf')
    
    settimane = {}
    pagine_settimane = [1, 2, 3, 4]
    
    for settimana_num, page_idx in enumerate(pagine_settimane, 1):
        print(f"📖 SETTIMANA {settimana_num}")
        
        page = pdf.pages[page_idx]
        tables = page.extract_tables()
        
        if not tables or not tables[0]:
            continue
        
        table = tables[0]
        
        # Trova giorni
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
            
            col_idx = giorni_pos[giorno]
            
            settimana[giorno] = {
                "colazione": "",
                "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "",
                "spuntino_2": "",
                "cena": ""
            }
            
            # COLAZIONE - accumulaRighe dalla riga 1 fino prima del pranzo
            settimana[giorno]["colazione"] = estrai_pasto_multiriga(table, col_idx, righe["colazione"], righe["pranzo"])
            
            # PRANZO - accumulaRighe dalla riga pranzo fino a spuntino_2
            settimana[giorno]["pranzo"] = estrai_pasto_multiriga(table, col_idx, righe["pranzo"], righe["spuntino_2"])
            
            # SPUNTINO_2 - singola riga
            if righe["spuntino_2"] < len(table) and col_idx < len(table[righe["spuntino_2"]]):
                settimana[giorno]["spuntino_2"] = pulisci_testo(table[righe["spuntino_2"]][col_idx])
            
            # CENA - accumulaRighe dalla riga cena fino alla fine
            settimana[giorno]["cena"] = estrai_pasto_multiriga(table, col_idx, righe["cena"], len(table))
        
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
