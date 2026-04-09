#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Legge il testo estratto a mano e lo formatta nel JSON
Dal testo visibile nel PDF
"""
import json

primavera_manual = {
    "SETTIMANA_1": {
        "LUNEDI": {
            "colazione": "Pane segale 50 g + 50-60 g hummus + pomodorini saltati",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g cous cous + 120 g lenticchie + pomodori secchi + pesto",
            "spuntino_2": "1 ricotta + cacao + stevia + cocco in scaglie",
            "cena": "Trancio di pesce infarinato con farina di mais 150 g + zucchine + 2 crostini integrali"
        },
        "MARTEDI": {
            "colazione": "Overnight porridge con mela cannella + 1 cucchiaino crema di mandorle",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "Insalata con sedano + 1/2 mela + 3 noci + 100 g tofu in friggitrice + pane 50 g",
            "spuntino_2": "Yogurt + 1 cucchiaio granola",
            "cena": "30 g triangolini mais con guacamole pomodorini + 1 rustichella di pollo + insalata di carote"
        },
        "MERCOLEDI": {
            "colazione": "50 g segale + ricotta + miele + 2 noci",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g riso con 80 g tonno e zucchine carote",
            "spuntino_2": "3-4 noci pecan + 1 banana",
            "cena": "Insalata con rucola + 2 mozzarelline + 100 g melone con aceto balsamico + 30 g pane segale + patate lesse 200 g"
        },
        "GIOVEDI": {
            "colazione": "Yogurt greco SL + 1 manciata frutta secca + 2 cucchiai granola + 1 kiwi",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g cous cous con 150 g gamberetti + piselli",
            "spuntino_2": "Yogurt + 1 cucchiaio granola",
            "cena": "1 confezione fiocchi di latte senza lattosio + insalata mela sedano noci"
        },
        "VENERDI": {
            "colazione": "2 fette integrali + marmellata + 2 cucchiaini burro arachidi",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g cous cous con 150 g gamberetti + piselli",
            "spuntino_2": "1 quadrato cioccolato fondente + 3 noci",
            "cena": "150 g pollo infarinato al limone e curry + piselli e carote saltati al rosmarino"
        },
        "SABATO": {
            "colazione": "1/3 di tortino fatto in casa",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "120 g gnocchi piselli con funghi e panna vegetale o latte di cocco",
            "spuntino_2": "1 frutto + 1 manciata frutta secca",
            "cena": "PASTO LIBERO (con moderazione)"
        },
        "DOMENICA": {
            "colazione": "1/3 di tortino fatto in casa",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "120 g gnocchi + pomodorini saltati con 70 g feta SL + 1 cucchiaio pesto",
            "spuntino_2": "1 frutto + 1 pezzo cioccolato",
            "cena": "Frittata di spinaci + chips di carote alla paprika + 2 crostini integrali"
        }
    }
}

# Carico il file JSON
with open('menu_settimanale.json', 'r', encoding='utf-8') as f:
    menu = json.load(f)

# Aggiorno solo SETTIMANA_1 con i dati manuali corretti
menu['PRIMAVERA']['SETTIMANA_1'] = primavera_manual['SETTIMANA_1']

# Salvo
with open('menu_settimanale.json', 'w', encoding='utf-8') as f:
    json.dump(menu, f, ensure_ascii=False, indent=2)

print("SETTIMANA_1 aggiornata correttamente!")

# Verifica mercoledi
print("\nMERCOLEDI SETTIMANA_1 - Verifica:")
for k, v in menu['PRIMAVERA']['SETTIMANA_1']['MERCOLEDI'].items():
    print(f"  {k}: {v}")
