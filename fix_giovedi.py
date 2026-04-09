import json

with open('menu_settimanale.json', 'r', encoding='utf-8') as f:
    menu = json.load(f)

# Correggi GIOVEDI cena
menu['PRIMAVERA']['SETTIMANA_1']['GIOVEDI']['cena'] = "1 confezione fiocchi di latte senza lattosio + insalata mela sedano noci + patate lesse 200 g"

with open('menu_settimanale.json', 'w', encoding='utf-8') as f:
    json.dump(menu, f, ensure_ascii=False, indent=2)

print("Corretto! GIOVEDI cena:")
print(menu['PRIMAVERA']['SETTIMANA_1']['GIOVEDI']['cena'])
