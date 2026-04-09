import json

with open('menu_settimanale.json', 'r', encoding='utf-8') as f:
    menu = json.load(f)

# Correggi DOMENICA cena
menu['PRIMAVERA']['SETTIMANA_1']['DOMENICA']['cena'] = "150 g pollo infarinato al limone e curry + piselli e carote saltati al rosmarino"

# Correggi VENERDI cena
menu['PRIMAVERA']['SETTIMANA_1']['VENERDI']['cena'] = "Insalata con rucola + 2 mozzarelline + 100 g melone con aceto balsamico + 30 g pane segale + patate lesse 200 g"

with open('menu_settimanale.json', 'w', encoding='utf-8') as f:
    json.dump(menu, f, ensure_ascii=False, indent=2)

print("Corretti!")
print("DOMENICA cena:", menu['PRIMAVERA']['SETTIMANA_1']['DOMENICA']['cena'])
print("VENERDI cena:", menu['PRIMAVERA']['SETTIMANA_1']['VENERDI']['cena'])
