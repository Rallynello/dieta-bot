import json

with open('menu_settimanale.json', 'r', encoding='utf-8') as f:
    menu = json.load(f)

# Correggi LUNEDI SETTIMANA_2 pranzo
menu['PRIMAVERA']['SETTIMANA_2']['LUNEDI']['pranzo'] = "1 piadina integrale + 80 g salmone affumicato e crema di 1/2 avocado e insalata"

with open('menu_settimanale.json', 'w', encoding='utf-8') as f:
    json.dump(menu, f, ensure_ascii=False, indent=2)

print("Corretto! LUNEDI SETTIMANA_2 pranzo:")
print(menu['PRIMAVERA']['SETTIMANA_2']['LUNEDI']['pranzo'])
