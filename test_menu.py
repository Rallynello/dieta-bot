import json

try:
    with open('menu_settimanale.json', 'r', encoding='utf-8') as f:
        menu = json.load(f)
    
    print("✅ JSON caricato")
    print(f"Stagioni: {list(menu.keys())}")
    
    for stagione in menu:
        settimane = list(menu[stagione].keys())
        print(f"\n{stagione}:")
        print(f"  Settimane: {settimane[:3]}")
        
        if settimane:
            prima_settimana = menu[stagione][settimane[0]]
            giorni = list(prima_settimana.keys())
            print(f"  Giorni in {settimane[0]}: {giorni[:2]}")
            
            if giorni:
                primo_giorno = prima_settimana[giorni[0]]
                print(f"  Pasti in {giorni[0]}: {list(primo_giorno.keys())}")

except Exception as e:
    print(f"❌ Errore: {e}")
