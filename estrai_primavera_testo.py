#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estrae PRIMAVERA parseando il testo grezzo del PDF
"""

import json
import pdfplumber
import re

GIORNI = ["LUNEDI", "MARTEDI", "MERCOLEDI", "GIOVEDI", "VENERDI", "SABATO", "DOMENICA"]

RIGHE_ETICHETTE = {
    1: {"colazione": "Colazione", "pranzo": "Pranzo", "spuntino_2": "Spuntino", "cena": "Cena"},
    2: {"colazione": "Colazione", "pranzo": "Pranzo", "spuntino_2": "Spuntino", "cena": "Cena"},
    3: {"colazione": "Colazione", "pranzo": "Pranzo", "spuntino_2": "Spuntino", "cena": "Cena"},
    4: {"colazione": "Colazione", "pranzo": "Pranzo", "spuntino_2": "Spuntino", "cena": "Cena"},
}

def pulisci(t):
    if not t:
        return ""
    t = str(t).strip()
    t = t.replace("\n", " ")
    while "  " in t:
        t = t.replace("  ", " ")
    return t

def estrai_primavera():
    print("\n" + "="*80)
    print("🌱 ESTRAZIONE PRIMAVERA - TESTO GREZZO")
    print("="*80 + "\n")
    
    pdf = pdfplumber.open('Piano Settimana Pasti Primavera1.pdf')
    
    settimane = {}
    
    for settimana_num, page_idx in enumerate([1, 2, 3, 4], 1):
        print(f"📖 SETTIMANA {settimana_num}")
        
        page = pdf.pages[page_idx]
        text = page.extract_text()
        
        # Split per giorno - cerca i nomi dei giorni
        # Il testo ha formato: LUNEDI ... MARTEDI ... MERCOLEDI ... ecc
        # Ogni giorno è separato dal successivo
        
        settimana = {}
        
        # Prova a splitta il testo per giorno in ordine
        sezioni = {}
        for giorno in GIORNI:
            # Cerca posizione del giorno nel testo
            pos = text.upper().find(giorno)
            if pos >= 0:
                sezioni[giorno] = pos
        
        # Ordina i giorni per posizione
        giorni_ordinati = sorted(sezioni.items(), key=lambda x: x[1])
        
        for idx, (giorno, pos) in enumerate(giorni_ordinati):
            # Estrai il testo dal giorno corrente fino al prossimo
            if idx < len(giorni_ordinati) - 1:
                pos_fine = giorni_ordinati[idx + 1][1]
            else:
                pos_fine = len(text)
            
            testo_giorno = text[pos:pos_fine]
            
            settimana[giorno] = {
                "colazione": "",
                "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "",
                "spuntino_2": "",
                "cena": ""
            }
            
            # Estrai sezioni dal testo del giorno
            # Usa espressioni regolari per trovare:
            # - Colazione (tutto prima di "Spuntino" o "Pranzo")
            # - Pranzo (tra "Pranzo" e "Spuntino")
            # - Spuntino_2 (tra "Spuntino" e "Cena")
            # - Cena (da "Cena" fino alla fine o al prossimo giorno)
            
            # Find Colazione
            match_col = re.search(r'Colazione\s+(.*?)(?=Spuntino|Pranzo)', testo_giorno, re.DOTALL)
            if match_col:
                settimana[giorno]["colazione"] = pulisci(match_col.group(1))
            
            # Find Pranzo
            match_pran = re.search(r'Pranzo\s+(.*?)(?=Spuntino(?!\s*Se))', testo_giorno, re.DOTALL)
            if match_pran:
                settimana[giorno]["pranzo"] = pulisci(match_pran.group(1))
            
            # Find Spuntino_2 (la riga che non dice "Se ti svegli dopo")
            # Cerchiamo tra "Spuntino" e "Cena"
            match_spunt2 = re.search(r'Spuntino\s+([^S]+?)(?=Cena)', testo_giorno, re.DOTALL)
            if match_spunt2:
                spunt_text = pulisci(match_spunt2.group(1))
                # Se contiene "Se ti svegli", è lo spuntino standard, ignora
                if "Se ti svegli" not in spunt_text:
                    settimana[giorno]["spuntino_2"] = spunt_text
            
            # Find Cena
            match_cena = re.search(r'Cena\s+(.*?)$', testo_giorno, re.DOTALL)
            if match_cena:
                settimana[giorno]["cena"] = pulisci(match_cena.group(1))
        
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
