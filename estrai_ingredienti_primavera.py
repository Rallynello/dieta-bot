#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estrae ingredienti da PRIMAVERA e li integra con ingredienti_definitivi.json
"""

import json
import re

# Carica il menu
with open('menu_settimanale.json', 'r', encoding='utf-8') as f:
    menu = json.load(f)

# Carica ingredienti esistenti
with open('ingredienti_definitivi.json', 'r', encoding='utf-8') as f:
    ingredienti_attuali = json.load(f)

# Estrai ingredienti da PRIMAVERA
ingredienti_primavera = set()

if 'PRIMAVERA' in menu:
    primavera = menu['PRIMAVERA']
    for settimana_key, settimana_data in primavera.items():
        for giorno, pasti_dict in settimana_data.items():
            for pasto, descrizione in pasti_dict.items():
                # Estrai parole (ingredienti potenziali)
                # Filtra le parole lunghe (probabilmente ingredienti)
                words = re.findall(r'\b[A-Za-z\u00C0-\u00FF]+\b', descrizione)
                for word in words:
                    # Scarta parole molto comuni e articoli
                    articoli = {'di', 'e', 'o', 'a', 'con', 'al', 'da', 'per', 'in', 'su', 'che', 'è', 'il', 'la', 'lo', 'gli', 'le', 'un', 'una', 'uno', 'all', 'alla', 'ai', 'alle', 'as', 'at', 'the', 'of', 'to', 'with'}
                    if word.lower() not in articoli and len(word) > 2:
                        ingredienti_primavera.add(word.strip())

# Stampa ingredienti estratti
print("🌱 Ingredienti estratti da PRIMAVERA:")
for ing in sorted(ingredienti_primavera):
    print(f"  - {ing}")

print(f"\nTotale ingredienti estratti: {len(ingredienti_primavera)}")

# Raggruppa per categoria (semplice euristica)
categorie = {
    '🥬 VERDURE': [],
    '🍗 PROTEINE': [],
    '🥕 CARBOIDRATI': [],
    '🧀 LATTICINI': [],
    '🍳 ALTRO': []
}

verdure = ['carote', 'spinaci', 'broccoli', 'zucchine', 'pomodori', 'asparagi', 'fagiolini', 'insalata', 'rucola', 'finocchio', 'cavolo', 'melanzane', 'radicchio', 'cipolla', 'sedano', 'barbabietola']
proteine = ['pollo', 'pesce', 'uova', 'carne', 'tacchino', 'salmone', 'gamberi', 'tonno', 'coniglio', 'merluzzo', 'orata', 'branzino', 'sogliola', 'trota', 'tofu', 'tempeh', 'polpo']
carboidrati = ['riso', 'pasta', 'pane', 'patate', 'farro', 'quinoa', 'cous', 'gnocchi', 'lenticchie', 'ceci', 'fagioli', 'miglio']
latticini = ['yogurt', 'ricotta', 'formaggio', 'mozzarella', 'latte', 'feta', 'crescenza', 'grana', 'philadelphia', 'fiocchi']

for ing in sorted(ingredienti_primavera):
    ing_lower = ing.lower()
    categorizzato = False
    
    for verd in verdure:
        if verd in ing_lower:
            categorie['🥬 VERDURE'].append(ing)
            categorizzato = True
            break
    
    if not categorizzato:
        for prot in proteine:
            if prot in ing_lower:
                categorie['🍗 PROTEINE'].append(ing)
                categorizzato = True
                break
    
    if not categorizzato:
        for carb in carboidrati:
            if carb in ing_lower:
                categorie['🥕 CARBOIDRATI'].append(ing)
                categorizzato = True
                break
    
    if not categorizzato:
        for latt in latticini:
            if latt in ing_lower:
                categorie['🧀 LATTICINI'].append(ing)
                categorizzato = True
                break
    
    if not categorizzato:
        categorie['🍳 ALTRO'].append(ing)

# Stampa categorizzazione
print("\n📋 Ingredienti categorizzati:")
for cat, ings in categorie.items():
    if ings:
        print(f"\n{cat}:")
        for ing in sorted(set(ings)):
            print(f"  - {ing}")

# Integra con ingredienti_definitivi
for categoria, ingredienti in ingredienti_attuali.items():
    print(f"\n✅ Ingredienti attuali in {categoria}: {len(ingredienti)}")

print("\n" + "="*50)
print("Vuoi aggiornare ingredienti_definitivi.json? (s/n)")
