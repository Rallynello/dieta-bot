import json
import re

# Leggi il menu JSON
with open('menu_settimanale.json', 'r', encoding='utf-8') as f:
    menu = json.load(f)

ingredienti_per_categoria = {
    '🥬 VERDURE': set(),
    '🍗 PROTEINE': set(),
    '🥕 CARBOIDRATI': set(),
    '🧀 LATTICINI': set()
}

# Parole chiave per categorizzazione
verdure_keywords = ['spinaci', 'carote', 'zucchine', 'insalata', 'pomodori', 'asparagi', 'broccoli', 
                   'cavolo', 'melanzane', 'peperoni', 'cipolla', 'aglio', 'lattuga', 'rucola', 'bietola',
                   'radicchio', 'sedano', 'barbabietola', 'scarola', 'catalogna', 'cicoria', 'finocchio',
                   'endivìa', 'porro', 'verza', 'cavolfiore', 'cavolini', 'cetrioli', 'zucca']

proteine_keywords = ['pollo', 'pesce', 'carne', 'uova', 'tofu', 'salmone', 'merluzzo', 'trota', 'sgombro',
                    'vitello', 'manzo', 'maiale', 'prosciutto', 'tacchino', 'orata', 'branzino', 'spigola',
                    'rombo', 'dentice', 'cernia', 'nasello', 'sogliola', 'sardine', 'acciughe', 'cotoletta',
                    'bistecca', 'arrosto', 'brasato', 'stufato', 'ossobuco', 'involtini', 'polpette']

carboidrati_keywords = ['riso', 'pasta', 'pane', 'patate', 'farro', 'orzo', 'ceci', 'lenticchie', 'fagioli',
                       'grano', 'avena', 'mais', 'polenta', 'couscous', 'spelto', 'teff', 'gnocchi', 'risotto']

latticini_keywords = ['ricotta', 'yogurt', 'formaggio', 'mozzarella', 'grana', 'parmigiano', 'latte', 'burro',
                     'mascarpone', 'pecorino', 'provolone', 'scamorza', 'emmental', 'camembert', 'fontina',
                     'taleggio', 'stracchino', 'crescenza', 'feta', 'gorgonzola']

def pulisci_ingrediente(ing):
    """Pulisce un ingrediente"""
    # Rimuovi i bullet
    ing = ing.lstrip('•').strip()
    
    # Rimuovi numeri iniziali e unità (tipo "200 g " o "1 fetta")
    ing = re.sub(r'^[\d\s,./]+[a-z]*\s+', '', ing, flags=re.IGNORECASE)
    
    # Rimuovi parentesi e roba strana
    ing = re.sub(r'[()"\'\[\]]', '', ing)
    
    # Rimuovi unità di misura finali
    unita = ['g', 'gr', 'mg', 'kg', 'ml', 'l', 'cl', 'dl', 'fetta', 'fette', 'etto', 'ettì', 'tazza', 
             'cucchiaio', 'cucchiaini', 'porzione', 'porzioni', 'pezzo', 'pezzi']
    for u in unita:
        ing = re.sub(rf'\s+{u}s?(\s|$)', '', ing, flags=re.IGNORECASE)
    
    # Trim
    ing = ing.strip()
    
    return ing

def categorizza(ing):
    """Categorizza un ingrediente"""
    ing_lower = ing.lower()
    
    for keyword in verdure_keywords:
        if keyword in ing_lower:
            return '🥬 VERDURE'
    
    for keyword in proteine_keywords:
        if keyword in ing_lower:
            return '🍗 PROTEINE'
    
    for keyword in carboidrati_keywords:
        if keyword in ing_lower:
            return '🥕 CARBOIDRATI'
    
    for keyword in latticini_keywords:
        if keyword in ing_lower:
            return '🧀 LATTICINI'
    
    return None

# Estrai ingredienti dal menu
print("📖 Estraendo ingredienti dal menu...")

for stagione, settimane in menu.items():
    print(f"\n  {stagione}")
    for settimana, giorni in settimane.items():
        for giorno, pasti in giorni.items():
            for pasto, descrizione in pasti.items():
                if isinstance(descrizione, str) and descrizione.strip():
                    # Splitti per riga (ogni ingrediente è su una riga)
                    linee = descrizione.split('\n')
                    for linea in linee:
                        linea = linea.strip()
                        if not linea:
                            continue
                        
                        ing = pulisci_ingrediente(linea)
                        
                        # Scarta se troppo corto o vuoto
                        if len(ing) < 2:
                            continue
                        
                        # Scarta se sono solo numeri
                        if ing.isdigit():
                            continue
                        
                        # Scarta se non ha lettere
                        if not any(c.isalpha() for c in ing):
                            continue
                        
                        categoria = categorizza(ing)
                        if categoria:
                            ingredienti_per_categoria[categoria].add(ing)

# Converti in liste e ordina
risultato = {cat: sorted(list(ing)) for cat, ing in ingredienti_per_categoria.items()}

# Stampa risultati
print("\n\n✅ INGREDIENTI ESTRATTI:\n")
for categoria, ingredienti in risultato.items():
    print(f"{categoria}: {len(ingredienti)} ingredienti")
    for ing in sorted(ingredienti)[:10]:
        print(f"  - {ing}")
    if len(ingredienti) > 10:
        print(f"  ... e altri {len(ingredienti) - 10}")

# Salva il file per il bot
with open('ingredienti_puliti.json', 'w', encoding='utf-8') as f:
    json.dump(risultato, f, ensure_ascii=False, indent=2)

print("\n✅ Salvato in 'ingredienti_puliti.json'")
