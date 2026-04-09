import json

with open('menu_settimanale.json', 'r', encoding='utf-8') as f:
    menu = json.load(f)

# Correggi GIOVEDI pranzo
menu['PRIMAVERA']['SETTIMANA_1']['GIOVEDI']['pranzo'] = "60 g riso basmati + 120 g ceci al latte di cocco + chips di carote alla paprika"

with open('menu_settimanale.json', 'w', encoding='utf-8') as f:
    json.dump(menu, f, ensure_ascii=False, indent=2)

print("Corretto! GIOVEDI pranzo:")
print(menu['PRIMAVERA']['SETTIMANA_1']['GIOVEDI']['pranzo'])
