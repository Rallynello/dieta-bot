import json
import re
from collections import defaultdict

# Carica il menu
with open('menu_settimanale.json', 'r', encoding='utf-8') as f:
    menu = json.load(f)

# Estrai tutti gli ingredienti
ingredienti = set()

# Lista di parole chiave per spezzare frasi lunghe
separatori = [' e ', ' con ', ' di ', ' in ', ' al ', ' alla ']

for stagione, settimane in menu.items():
    for settimana, giorni in settimane.items():
        for giorno, pasti in giorni.items():
            for pasto, descrizione in pasti.items():
                if isinstance(descrizione, str):
                    righe = [r.strip() for r in descrizione.split('\n') if r.strip()]
                    for riga in righe:
                        # Rimuovi bullet point
                        riga = riga.replace('• ', '').strip()
                        if riga and not riga.startswith('('):
                            # Rimuovi parentesi e numeri all'inizio
                            riga = re.sub(r'^\d+\s*[a-zA-Z]*\s*', '', riga).strip()
                            riga = re.sub(r'\s*\(.*?\)\s*', ' ', riga).strip()
                            
                            # Prova a spezzare per separatori comuni
                            parti = [riga]
                            for sep in [' e ', ' con ', ' in ', ' al ', ' alla ']:
                                nuove_parti = []
                                for parte in parti:
                                    if sep in parte.lower():
                                        subparti = parte.split(sep)
                                        nuove_parti.extend(subparti)
                                    else:
                                        nuove_parti.append(parte)
                                parti = nuove_parti
                            
                            # Aggiungi tutti i pezzetti
                            for parte in parti:
                                parte = parte.strip()
                                # Rimuovi numeri finali (tipo "150 g")
                                parte = re.sub(r'\s+[\d,\.]+\s*[a-zA-Z%]*$', '', parte).strip()
                                
                                if parte and len(parte) > 2 and not re.match(r'^\d+', parte):
                                    ingredienti.add(parte)

# Ordina alfabeticamente
ingredienti_sorted = sorted(list(ingredienti))

# Categorizza manualmente
categorie = {
    "🥕 Verdure": [],
    "🍗 Proteine": [],
    "🍞 Carboidrati": [],
    "🥜 Frutta Secca": [],
    "🧀 Latticini": [],
    "🍫 Dolci/Snack": [],
    "🌿 Altro": []
}

# Parole chiave per categorizzazione
proteine_keywords = ['pollo', 'pesce', 'salmone', 'merluzzo', 'tonno', 'gamberi', 'calamari', 'uova', 'bresaola', 
                     'prosciutto', 'carne', 'ochio di bue', 'uovo', 'frittatina', 'pesce spada', 'sogliola', 'platessa',
                     'salsiccia', 'carni', 'cacio', 'vitello', 'maiale']

verdure_keywords = ['asparagi', 'pomodori', 'pomodorini', 'spinaci', 'zucchine', 'insalata', 'rucola', 'finocchio',
                   'fagiolini', 'piselli', 'melanzane', 'carote', 'sedano', 'cavolo', 'broccoli', 'cavolfiore',
                   'insalatina', 'radicchio', 'lattuga', 'cicoria', 'porro', 'cipolla', 'aglio', 'erbette',
                   'pomodoro', 'olive', 'peperoni', 'zucca']

carboidrati_keywords = ['pane', 'riso', 'pasta', 'farro', 'porridge', 'toast', 'wasa', 'crackers', 'pancake',
                       'quinoa', 'piadina', 'cereal', 'ceci', 'lenticchie', 'farinata', 'patate', 'legumi',
                       'bran', 'farina', 'pudding', 'avena', 'orzo', 'bagel']

frutta_secca_keywords = ['mandorle', 'noci', 'nocciole', 'pistacchio', 'uvetta', 'semi di lino', 'semi di chia',
                        'semi', 'parmigiano', 'grana', 'formaggio', 'scaglie']

latticini_keywords = ['yogurt', 'ricotta', 'philadelphia', 'latte', 'formaggio', 'burro', 'feta', 'grana',
                     'parmigiano', 'scamorza', 'mozzarella', 'gorgonzola', 'mascarpone']

dolci_keywords = ['cioccolato', 'budino', 'cacao', 'gelato', 'barretta', 'equilibra', 'stevia', 'truvia',
                 'fragole', 'mirtilli', 'kiwi', 'arancia', 'avocado', 'frutto', 'frutta']

for ing in ingredienti_sorted:
    ing_lower = ing.lower()
    categorizzato = False
    
    for keyword in proteine_keywords:
        if keyword in ing_lower:
            categorie["🍗 Proteine"].append(ing)
            categorizzato = True
            break
    
    if not categorizzato:
        for keyword in verdure_keywords:
            if keyword in ing_lower:
                categorie["🥕 Verdure"].append(ing)
                categorizzato = True
                break
    
    if not categorizzato:
        for keyword in carboidrati_keywords:
            if keyword in ing_lower:
                categorie["🍞 Carboidrati"].append(ing)
                categorizzato = True
                break
    
    if not categorizzato:
        for keyword in frutta_secca_keywords:
            if keyword in ing_lower:
                categorie["🥜 Frutta Secca"].append(ing)
                categorizzato = True
                break
    
    if not categorizzato:
        for keyword in latticini_keywords:
            if keyword in ing_lower:
                categorie["🧀 Latticini"].append(ing)
                categorizzato = True
                break
    
    if not categorizzato:
        for keyword in dolci_keywords:
            if keyword in ing_lower:
                categorie["🍫 Dolci/Snack"].append(ing)
                categorizzato = True
                break
    
    if not categorizzato:
        categorie["🌿 Altro"].append(ing)

# Salva in JSON
with open('ingredienti_categorizzati.json', 'w', encoding='utf-8') as f:
    json.dump(categorie, f, ensure_ascii=False, indent=2)

print("✅ Ingredienti estratti e categorizzati!")
print(f"Totale ingredienti: {len(ingredienti_sorted)}\n")
for cat, ingr in categorie.items():
    print(f"{cat}: {len(ingr)} ingredienti")
