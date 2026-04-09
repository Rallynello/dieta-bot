#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estrae i menu dai 3 PDF e crea menu_completo_nuovo.json
Legge le tabelle colonna per colonna (1 colonna = 1 giorno)
"""

import json
import pdfplumber
from pathlib import Path

GIORNI = ["LUNEDI", "MARTEDI", "MERCOLEDI", "GIOVEDI", "VENERDI", "SABATO", "DOMENICA"]
PASTI_ORDINE = ["colazione", "spuntino", "pranzo", "spuntino_2", "cena", "dopo_cena"]

def estrai_settimane_da_pdf(pdf_path, nome_pdf):
    """Estrae tutte le settimane da un PDF"""
    print(f"\n📄 Elaborando {nome_pdf}...")
    settimane = {}
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"   📑 Pagine totali: {len(pdf.pages)}")
            
            for page_idx, page in enumerate(pdf.pages):
                print(f"   📌 Pagina {page_idx + 1}...")
                
                # Estrai tabelle da questa pagina
                tables = page.extract_tables()
                
                if tables:
                    for table_idx, table in enumerate(tables):
                        print(f"      🔲 Tabella {table_idx + 1}")
                        
                        # Analizza la tabella colonna per colonna
                        if len(table) > 0 and len(table[0]) > 1:
                            # Prova a estrarre i giorni
                            settimana = estrai_settimana_da_tabella(table)
                            if settimana:
                                num_settimana = len(settimane) + 1
                                settimane[num_settimana] = settimana
                                print(f"         ✓ Settimana {num_settimana} estratta")
                
    except Exception as e:
        print(f"❌ Errore: {e}")
    
    return settimane

def estrai_settimana_da_tabella(table):
    """
    Estrae una settimana da una tabella.
    Assume: prima colonna = nomi pasti, altre colonne = giorni
    """
    if not table or len(table) < 6 or len(table[0]) < 2:
        return None
    
    settimana = {}
    
    # Estrarre i 7 giorni
    num_colonne = len(table[0])
    
    for giorno_idx in range(min(7, num_colonne - 1)):
        giorno = GIORNI[giorno_idx]
        settimana[giorno] = {
            "colazione": "",
            "spuntino": "",
            "pranzo": "",
            "spuntino_2": "",
            "cena": "",
            "dopo_cena": ""
        }
        
        # Estrarre i pasti per questo giorno (colonna)
        for pasto_idx, pasto in enumerate(PASTI_ORDINE):
            if pasto_idx < len(table):
                cella = table[pasto_idx][giorno_idx + 1] if giorno_idx + 1 < len(table[pasto_idx]) else ""
                
                # Pulisci il testo
                if cella:
                    testo = str(cella).strip()
                    # Se è solo "–", copia dal Lunedì (spuntino standard)
                    if testo == "–" and pasto == "spuntino":
                        testo = settimana["LUNEDI"]["spuntino"]
                    settimana[giorno][pasto] = testo
    
    return settimana

def crea_menu_completo():
    """Crea il menu completo dai 3 PDF"""
    menu = {
        "estate": {},
        "inverno": {}
    }
    
    # Estate: Settimane 1-4
    print("\n☀️  ELABORANDO ESTATE...")
    estate_settimane = estrai_settimane_da_pdf(
        "Piano Settimana Pasti Estate1.pdf",
        "Piano Settimana Pasti Estate1.pdf"
    )
    for num, settimana in estate_settimane.items():
        menu["estate"][str(num)] = settimana
    
    # Inverno: Settimane 1-4
    print("\n❄️  ELABORANDO INVERNO (1-4)...")
    inverno1_settimane = estrai_settimane_da_pdf(
        "Piano Settimana Pasti Inverno1.pdf",
        "Piano Settimana Pasti Inverno1.pdf"
    )
    for num, settimana in inverno1_settimane.items():
        menu["inverno"][str(num)] = settimana
    
    # Inverno: Settimane 5-8
    print("\n❄️  ELABORANDO INVERNO (5-8)...")
    inverno2_settimane = estrai_settimane_da_pdf(
        "Piano Settimana Pasti Inverno2.pdf",
        "Piano Settimana Pasti Inverno2.pdf"
    )
    for num, settimana in inverno2_settimane.items():
        # Aggiungi offset 4 (settimana 1 diventa 5)
        menu["inverno"][str(num + 4)] = settimana
    
    return menu

def salva_json(menu, nome_file):
    """Salva il menu in JSON"""
    with open(nome_file, 'w', encoding='utf-8') as f:
        json.dump(menu, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Salvato: {nome_file}")
    
    # Stampa statistiche
    estate_count = len(menu.get("estate", {}))
    inverno_count = len(menu.get("inverno", {}))
    print(f"   📊 Estate: {estate_count} settimane")
    print(f"   📊 Inverno: {inverno_count} settimane")

if __name__ == "__main__":
    print("🚀 Inizio estrazione menu dai PDF...")
    
    menu = crea_menu_completo()
    salva_json(menu, "menu_completo_nuovo.json")
    
    print("\n✅ Processo completato!")
    print("   Verifica menu_completo_nuovo.json")
    print("   Se corretto, rinomina in menu_settimanale_completo.json")
