#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script per estrarre testo dalle immagini usando OCR
"""

from PIL import Image
import pytesseract
import os

# Configura il percorso di Tesseract se necessario
# Su Windows, potrebbe servire specificare il percorso
try:
    import pytesseract
    # Prova a trovare Tesseract
    pytesseract.pytesseract.pytesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
except:
    pass

def estrai_testo_ocr(immagine_path):
    """Estrae testo da un'immagine usando OCR"""
    try:
        img = Image.open(immagine_path)
        # Migliora la qualità prima di fare OCR
        img = img.convert('RGB')
        testo = pytesseract.image_to_string(img, lang='ita')
        return testo
    except Exception as e:
        return f"❌ Errore: {str(e)}"

# Percorsi delle immagini PRIMAVERA
immagini = [
    "Settimana1Primavera.PNG",
    "Settimana2Primavera.PNG",
    "Settimana3Primavera.PNG",
    "Settimana4Primavera.PNG"
]

# Estrai testo da ogni immagine
for img_name in immagini:
    img_path = img_name
    
    if not os.path.exists(img_path):
        print(f"AVVISO: {img_name} non trovato")
        continue
    
    print(f"\n{'='*80}")
    print(f"Estraendo testo da: {img_name}")
    print(f"{'='*80}\n")
    
    testo = estrai_testo_ocr(img_path)
    
    # Salva in file
    output_file = f"OCR_Extract/{img_name.replace('.PNG', '.txt')}"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(testo)
    
    print(f"Salvato in: {output_file}\n")

print(f"\n{'='*80}")
print("Estrazione completata!")
print(f"{'='*80}\n")
