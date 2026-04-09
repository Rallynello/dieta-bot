#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estrae i menu dai PDF e crea un nuovo JSON completo
"""

import json
import re
from pathlib import Path

# Percorsi PDF
PDF_ESTATE1 = "Piano Settimana Pasti Estate1.pdf"
PDF_INVERNO1 = "Piano Settimana Pasti Inverno1.pdf"
PDF_INVERNO2 = "Piano Settimana Pasti Inverno2.pdf"

GIORNI = ["LUNEDI", "MARTEDI", "MERCOLEDI", "GIOVEDI", "VENERDI", "SABATO", "DOMENICA"]
PASTI = ["colazione", "spuntino", "pranzo", "spuntino_2", "cena", "dopo_cena"]

def estrai_testo_pdf(pdf_path):
    """Estrae il testo dal PDF"""
    try:
        import PyPDF2
        testo_completo = ""
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                testo_completo += page.extract_text() + "\n"
        return testo_completo
    except Exception as e:
        print(f"❌ Errore lettura {pdf_path}: {e}")
        return ""

def parse_tabella_settimanale(testo, num_settimana):
    """
    Estrae una tabella settimanale dal testo del PDF.
    Ritorna un dizionario con i 7 giorni e i loro pasti.
    """
    settimana = {}
    for giorno in GIORNI:
        settimana[giorno] = {
            "colazione": "",
            "spuntino": "",
            "pranzo": "",
            "spuntino_2": "",
            "cena": "",
            "dopo_cena": ""
        }
    
    # ⚠️ NOTA: L'estrazione da PDF è complessa e dipende dal formato.
    # Qui uso un approccio generico - potrebbe non essere perfetto.
    # Se i PDF hanno tabelle strutturate, potrebbe servire pdfplumber.
    
    return settimana

def crea_json_da_pdf():
    """Crea il JSON completo dai PDF"""
    menu_completo = {
        "estate": {},
        "inverno": {}
    }
    
    print("📄 Estraendo dati dai PDF...")
    print("⚠️  NOTA: Estrazione da PDF è complessa - potrebbero servire correzioni manuali")
    
    # Estate: settimane 1-4
    print("\n☀️  ESTATE:")
    testo_estate1 = estrai_testo_pdf(PDF_ESTATE1)
    if testo_estate1:
        print(f"   ✓ Estratti {len(testo_estate1)} caratteri da Estate1")
    
    # Inverno: settimane 1-4
    print("\n❄️  INVERNO (Settimane 1-4):")
    testo_inverno1 = estrai_testo_pdf(PDF_INVERNO1)
    if testo_inverno1:
        print(f"   ✓ Estratti {len(testo_inverno1)} caratteri da Inverno1")
    
    # Inverno: settimane 5-8
    print("\n❄️  INVERNO (Settimane 5-8):")
    testo_inverno2 = estrai_testo_pdf(PDF_INVERNO2)
    if testo_inverno2:
        print(f"   ✓ Estratti {len(testo_inverno2)} caratteri da Inverno2")
    
    print("\n⚠️  L'estrazione automatica da PDF è limitata.")
    print("    Per risultati accurati, usa uno di questi metodi:")
    print("    1. OCR con pytesseract (migliore per PDF scansionati)")
    print("    2. pdfplumber (migliore per PDF con tabelle)")
    print("    3. Estrazione manuale (più accurata)")
    
    return menu_completo

def salva_menu_json(menu, nome_file):
    """Salva il menu in JSON"""
    with open(nome_file, 'w', encoding='utf-8') as f:
        json.dump(menu, f, ensure_ascii=False, indent=2)
    print(f"\n✅ Salvato: {nome_file}")

if __name__ == "__main__":
    menu = crea_json_da_pdf()
    salva_menu_json(menu, "menu_estratto_da_pdf.json")
    
    print("\n📋 Prossimi step:")
    print("   1. Apri i PDF e controlla i dati")
    print("   2. Modifica manualmente il JSON se necessario")
    print("   3. Confronta con le immagini PNG per validare")
