#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estrae ingredienti da PRIMAVERA e li integra con ingredienti_definitivi.json
Evita doppioni e aggiunge solo quelli nuovi
"""

import json
import re

# Carica il menu
with open('menu_settimanale.json', 'r', encoding='utf-8') as f:
    menu = json.load(f)

# Carica ingredienti esistenti
with open('ingredienti_definitivi.json', 'r', encoding='utf-8') as f:
    ingredienti_attuali = json.load(f)

# Flatten ingredienti attuali per confronto (case-insensitive)
ingredienti_esistenti = set()
for categoria, ingredienti in ingredienti_attuali.items():
    for ing in ingredienti:
        ingredienti_esistenti.add(ing.lower())

# Estrai ingredienti da PRIMAVERA
ingredienti_primavera_raw = set()

if 'PRIMAVERA' in menu:
    primavera = menu['PRIMAVERA']
    for settimana_key, settimana_data in primavera.items():
        for giorno, pasti_dict in settimana_data.items():
            for pasto, descrizione in pasti_dict.items():
                # Estrai parole dai menu
                words = re.findall(r'\b[A-Za-z\u00C0-\u00FF]+\b', descrizione)
                for word in words:
                    articoli = {'di', 'e', 'o', 'a', 'con', 'al', 'da', 'per', 'in', 'su', 'che', 'è', 'il', 'la', 'lo', 'gli', 'le', 'un', 'una', 'uno', 'all', 'alla', 'ai', 'alle', 'as', 'at', 'the', 'of', 'to', 'with', 'g', 'ml', 'cc'}
                    if word.lower() not in articoli and len(word) > 2:
                        ingredienti_primavera_raw.add(word.strip())

# Filtra solo ingredienti NON esistenti
ingredienti_nuovi = set()
for ing in ingredienti_primavera_raw:
    if ing.lower() not in ingredienti_esistenti:
        ingredienti_nuovi.add(ing)

print("🌱 INGREDIENTI NUOVI DA PRIMAVERA (non presenti negli altri periodi):")
print("="*60)

# Categorizziamo i nuovi ingredienti
categorie_nuovi = {
    '🥬 VERDURE': [],
    '🍗 PROTEINE': [],
    '🥕 CARBOIDRATI': [],
    '🧀 LATTICINI': [],
    '🍳 ALTRO': []
}

verdure = ['carote', 'spinaci', 'broccoli', 'zucchine', 'pomodori', 'asparagi', 'fagiolini', 'insalata', 'rucola', 'finocchio', 'cavolo', 'melanzane', 'radicchio', 'cipolla', 'sedano', 'barbabietola', 'porri', 'carciofi', 'piselli']
proteine = ['pollo', 'pesce', 'uova', 'carne', 'tacchino', 'salmone', 'gamberi', 'tonno', 'coniglio', 'merluzzo', 'orata', 'branzino', 'sogliola', 'trota', 'tofu', 'tempeh', 'polpo', 'lenticchie', 'ceci', 'fagioli']
carboidrati = ['riso', 'pasta', 'pane', 'patate', 'farro', 'quinoa', 'cous', 'gnocchi', 'miglio', 'mais']
latticini = ['yogurt', 'ricotta', 'formaggio', 'mozzarella', 'latte', 'feta', 'crescenza', 'grana', 'philadelphia', 'fiocchi', 'primosale', 'caprino']

for ing in sorted(ingredienti_nuovi):
    ing_lower = ing.lower()
    categorizzato = False
    
    for verd in verdure:
        if verd in ing_lower:
            categorie_nuovi['🥬 VERDURE'].append(ing)
            categorizzato = True
            break
    
    if not categorizzato:
        for prot in proteine:
            if prot in ing_lower:
                categorie_nuovi['🍗 PROTEINE'].append(ing)
                categorizzato = True
                break
    
    if not categorizzato:
        for carb in carboidrati:
            if carb in ing_lower:
                categorie_nuovi['🥕 CARBOIDRATI'].append(ing)
                categorizzato = True
                break
    
    if not categorizzato:
        for latt in latticini:
            if latt in ing_lower:
                categorie_nuovi['🧀 LATTICINI'].append(ing)
                categorizzato = True
                break
    
    if not categorizzato:
        categorie_nuovi['🍳 ALTRO'].append(ing)

# Stampa i nuovi ingredienti per categoria
for cat, ings in categorie_nuovi.items():
    if ings:
        print(f"\n{cat}:")
        for ing in sorted(set(ings)):
            print(f"  + {ing}")

# Aggiungi i nuovi ingredienti
print("\n\n✅ AGGIORNAMENTO ingredienti_definitivi.json:")
print("="*60)

for categoria, ingredienti_nuova_cat in categorie_nuovi.items():
    ingredienti_unici = list(set(ingredienti_nuova_cat))
    if ingredienti_unici:
        if categoria not in ingredienti_attuali:
            ingredienti_attuali[categoria] = []
        
        ingredienti_attuali[categoria].extend(ingredienti_unici)
        ingredienti_attuali[categoria] = sorted(list(set(ingredienti_attuali[categoria])))
        
        print(f"{categoria}: +{len(ingredienti_unici)} ingredienti")
        print(f"  Totale ora: {len(ingredienti_attuali[categoria])}")

# Salva il file aggiornato
with open('ingredienti_definitivi.json', 'w', encoding='utf-8') as f:
    json.dump(ingredienti_attuali, f, indent=2, ensure_ascii=False)

print("\n\n✅ File ingredienti_definitivi.json aggiornato con successo!")
