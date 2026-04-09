import json
from PIL import Image
import pytesseract
import re

# Estrai dati dalle immagini Inverno2 (settimane 5-8)
inverno2_images = [
    "Settimana5Inverno2.PNG",
    "Settimana6Inverno2.PNG", 
    "Settimana7Inverno2.PNG",
    "Settimana8Inverno2.PNG"
]

inverno2_data = {}

for i, img_path in enumerate(inverno2_images, start=5):
    try:
        img = Image.open(img_path)
        text = pytesseract.image_to_string(img, lang='ita')
        
        # Parsing manuale - estrai i giorni e i pasti
        # Per ora inserisco placeholder - tu compila manualmente leggendo le immagini
        inverno2_data[str(i)] = {
            "lunedi": {},
            "martedi": {},
            "mercoledi": {},
            "giovedi": {},
            "venerdi": {},
            "sabato": {},
            "domenica": {}
        }
        print(f"Settimana {i} OCR text:\n{text}\n{'='*50}\n")
    except Exception as e:
        print(f"Errore lettura {img_path}: {e}")

# Carica il JSON completo
with open("dieta-bot/menu_settimanale_completo.json", "r", encoding="utf-8") as f:
    menu = json.load(f)

# Aggiungi le settimane 5-8 a inverno
menu["inverno"]["5"] = inverno2_data.get("5", {})
menu["inverno"]["6"] = inverno2_data.get("6", {})
menu["inverno"]["7"] = inverno2_data.get("7", {})
menu["inverno"]["8"] = inverno2_data.get("8", {})

# Salva
with open("dieta-bot/menu_settimanale_completo.json", "w", encoding="utf-8") as f:
    json.dump(menu, f, ensure_ascii=False, indent=2)

print("JSON aggiornato con settimane 5-8!")
