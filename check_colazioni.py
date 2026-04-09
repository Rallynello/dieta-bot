#!/usr/bin/env python3

import json

with open('menu_settimanale.json') as f:
    menu = json.load(f)

print("MARTEDI Settimana 1 - COLAZIONE:")
colazione = menu["PRIMAVERA"]["SETTIMANA_1"]["MARTEDI"]["colazione"]
print(f"  {colazione}")

print("\nLUNEDI Settimana 1 - COLAZIONE:")
colazione_lun = menu["PRIMAVERA"]["SETTIMANA_1"]["LUNEDI"]["colazione"]
print(f"  {colazione_lun}")

print("\nMERCOLEDI Settimana 1 - COLAZIONE:")
colazione_mer = menu["PRIMAVERA"]["SETTIMANA_1"]["MERCOLEDI"]["colazione"]
print(f"  {colazione_mer}")
