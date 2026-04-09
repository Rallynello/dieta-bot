#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script per formattare il menu in modo più leggibile
Ogni ingrediente su una riga separata
"""

import json
import re

def formatta_pasto(descrizione):
    """
    Prende una descrizione e la formatta con ogni ingrediente su una riga separata.
    Gestisce: +, "e", "con", "al", "alla", virgole
    """
    descrizione = descrizione.strip()
    
    # Rimpiazza alcuni separatori comuni con "+"
    descrizione = re.sub(r'\s+con\s+', ' + ', descrizione, flags=re.IGNORECASE)
    descrizione = re.sub(r'\s+al\s+', ' + ', descrizione, flags=re.IGNORECASE)
    descrizione = re.sub(r'\s+alla\s+', ' + ', descrizione, flags=re.IGNORECASE)
    descrizione = re.sub(r',\s+oppure\s+', '\n• ', descrizione, flags=re.IGNORECASE)
    
    # Dividi per "+"
    ingredienti = [x.strip() for x in descrizione.split('+')]
    
    righe = []
    for ingrediente in ingredienti:
        if not ingrediente:
            continue
        
        # Se l'ingrediente contiene newline (da "oppure"), dividi
        if '\n' in ingrediente:
            sub_righe = ingrediente.split('\n')
            for sub_r in sub_righe:
                sub_r = sub_r.strip()
                if sub_r and not sub_r.startswith('•'):
                    righe.append(f"• {sub_r}")
                elif sub_r:
                    righe.append(sub_r)
        elif "," in ingrediente:
            sub_ingredienti = [x.strip() for x in ingrediente.split(",")]
            for sub_ing in sub_ingredienti:
                if sub_ing:
                    righe.append(f"• {sub_ing}")
        else:
            righe.append(f"• {ingrediente}")
    
    # Rimuovi i "• " doppi
    result = "\n".join(righe)
    result = re.sub(r'•\s+•', '•', result)
    
    return result

# Carica il menu attuale
with open('menu_settimanale.json', 'r', encoding='utf-8') as f:
    MENU = json.load(f)

# Processa ogni pasto
menu_formattato = {}

for stagione_key, stagione_data in MENU.items():
    menu_formattato[stagione_key] = {}
    
    for settimana_key, settimana_data in stagione_data.items():
        menu_formattato[stagione_key][settimana_key] = {}
        
        for giorno, pasti_dict in settimana_data.items():
            menu_formattato[stagione_key][settimana_key][giorno] = {}
            
            for pasto, descrizione in pasti_dict.items():
                # Se è già formattato (contiene \n), salta
                if isinstance(descrizione, str) and '\n' in descrizione:
                    menu_formattato[stagione_key][settimana_key][giorno][pasto] = descrizione
                elif isinstance(descrizione, str):
                    # Altrimenti formatta
                    menu_formattato[stagione_key][settimana_key][giorno][pasto] = formatta_pasto(descrizione)
                else:
                    menu_formattato[stagione_key][settimana_key][giorno][pasto] = descrizione

# Salva il menu formattato
with open('menu_settimanale.json', 'w', encoding='utf-8') as f:
    json.dump(menu_formattato, f, ensure_ascii=False, indent=2)

print("✅ Menu formattato e salvato!")
print("\n📝 ESEMPIO - ESTATE SETTIMANA 1, LUNEDI:\n")
for pasto, dettagli in menu_formattato['ESTATE']['SETTIMANA_1']['LUNEDI'].items():
    print(f"{pasto.upper()}:")
    print(dettagli)
    print()
