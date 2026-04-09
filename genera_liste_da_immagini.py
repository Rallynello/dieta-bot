#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛒 GENERATORE LISTE DELLA SPESA DA IMMAGINI

COME FUNZIONA:
1. Guardi le immagini (Settimana1.PNG, Settimana2.PNG, ecc.)
2. Modifichi i dizionari qui sotto (SETTIMANA_1, SETTIMANA_2, ecc.)
3. Esegui: python genera_liste_da_immagini.py
4. Le 4 liste vengono rigenerate!

Quando cambi le immagini, basta modificare questo file e rigenerare!
"""

from datetime import datetime

# ===========================================================================
# SETTIMANA 1
# ===========================================================================

SETTIMANA_1 = {
    'CARNE E PESCE': [
        'Pollo: 150g',
        'Merluzzo: 1 trancio',
        'Salmone: 1 trancio',
        'Gamberetti: 150g',
    ],
    'UOVA': [
        'Uova: 6 pezzi',
    ],
    'PROTEINE VEGETALI': [
        'Tofu: 80-100g',
        'Tempeh: 70-80g',
    ],
    'LATTICINI': [
        'Yogurt greco 0%: 2-3 vasetti',
        'Ricotta: 1 confezione',
        'Feta: 70g',
        'Philadelphia light: Q.B.',
    ],
    'CEREALI E CARBOIDRATI': [
        'Pane di segale: 70g',
        'Pane integrale: Q.B.',
        'Fette biscottate: 1 confezione',
        'Wasa fibre: 2 pacchetti',
        'Gallette: 1 confezione',
        'Crackers legumi: 1 confezione',
        'Tortilla: 30g',
        'Riso: 60g',
        'Riso nero: 60g',
        'Pasta integrale: 60g',
        'Pasta di avena: 60g',
        'Gnocchi: 120g',
        'Avena: Q.B.',
    ],
    'LEGUMI': [
        'Hummus: 1 confezione',
        'Piselli: 360g',
    ],
    'VERDURE': [
        'Pomodorini: 500g',
        'Insalata: 1 cespo',
        'Barbabietola: 2 pezzi',
        'Cavolo: 1 cespo',
        'Carote: 500g',
        'Zucchine: 3 pezzi',
        'Broccoli: 300g',
        'Spinaci: 200g',
        'Funghi: 200g',
        'Finocchio: 2 pezzi',
        'Porri: 2 pezzi',
        'Cipolla: 2 pezzi',
        'Mais: 1 scatoletta',
        'Patate dolci: 200g',
        'Zucca: 300g',
    ],
    'FRUTTA': [
        'Uva: 1 grappolo',
        'Mele: 3 pezzi',
        'Kiwi: 2 pezzi',
        'Arance: 4 pezzi',
        'Banane: 2 pezzi',
        'Avocado: 2 pezzi',
    ],
    'FRUTTA SECCA E SEMI': [
        'Frutta secca mista: 200g',
        'Noci pecan: Q.B.',
        'Noci: Q.B.',
        'Pinoli: Q.B.',
        'Granola: 200g',
        'Cocco scaglie: Q.B.',
        'Semi chia/lino: Q.B.',
    ],
    'CONDIMENTI E DISPENSA': [
        'Crema di mandorle: 1 vasetto',
        'Burro arachidi: Q.B.',
        'Marmellata: 1 vasetto',
        'Senape: 1 vasetto',
        'Limone: 3 pezzi',
        'Spezie varie',
        'Latte cocco: 1 lattina',
        'Olio cocco: Q.B.',
        'Olio EVO: Q.B.',
        'Uvetta: Q.B.',
        'Pangrattato: Q.B.',
        'Cacao: Q.B.',
        'Cioccolato 80%: 1 tavoletta',
        'Stevia: Q.B.',
        'Aceto balsamico: Q.B.',
        'Tè verde: 1 confezione',
    ],
}

SETTIMANA_2 = {
    'CARNE E PESCE': [
        'Coniglio: 120g',
        'Sgombro: 80g',
        'Sogliola/Platessa: 150-180g',
        'Gamberi: 100g',
    ],
    'UOVA': [
        'Uova: 3 pezzi',
        'Albumi: Q.B.',
    ],
    'PROTEINE VEGETALI': [
        'Tofu: 100g',
    ],
    'LATTICINI': [
        'Yogurt greco 0%: 4 vasetti',
        'Ricotta: 1 confezione',
        'Stracciatella: 80g',
        'Parmigiano: Q.B.',
    ],
    'CEREALI E CARBOIDRATI': [
        'Pane integrale: 100g',
        'Fette biscottate: 1 confezione',
        'Wasa fibre: 2 pacchetti',
        'Crackers: 1 confezione',
        'Riso basmati: 100g',
        'Risotto: 60g',
        'Pasta avena: 60g',
        'Gnocchi: 120g',
        'Avena fiocchi: Q.B.',
        'Farina avena: Q.B.',
        'Cereali All Bran: 1 confezione',
    ],
    'LEGUMI': [
        'Piselli: 120g',
        'Fagioli rossi: 150g',
        'Lenticchie rosse: 40g',
        'Ceci: 120g',
        'Falafel: 4-5 pezzi',
    ],
    'VERDURE': [
        'Funghi: 300g',
        'Broccoli: 300g',
        'Carote: 400g',
        'Cavolo: 1 cespo',
        'Pomodorini: 400g',
        'Mais: 1 scatoletta',
        'Finocchi: 2 pezzi',
        'Zucca: 300g',
        'Porri: 2 pezzi',
        'Bieta: 1 mazzo',
        'Insalata: Q.B.',
    ],
    'FRUTTA': [
        'Kiwi: 3 pezzi',
        'Banane: 2 pezzi',
        'Avocado: 2 pezzi',
    ],
    'FRUTTA SECCA E SEMI': [
        'Frutta secca: 200g',
        'Noci: Q.B.',
        'Granella arachidi: Q.B.',
        'Semi lino tritati: Q.B.',
        'Semi chia: Q.B.',
        'Cocco scaglie: Q.B.',
        'Granola: 200g',
    ],
    'CONDIMENTI E DISPENSA': [
        'Burro arachidi: 1 vasetto',
        'Marmellata: 1 vasetto',
        'Latte cocco: 2 lattine',
        'Senape: 1 vasetto',
        'Olive: 1 vasetto',
        'Capperi: 1 vasetto',
        'Spezie: curcuma, paprika, curry, coriandolo, rosmarino',
        'Cioccolato 80%: 1 tavoletta',
        'Cacao: Q.B.',
        'Stevia: Q.B.',
        'Olio EVO: Q.B.',
        'Tè verde: 1 confezione',
    ],
}

SETTIMANA_3 = {
    'CARNE E PESCE': [
        'Pollo: 120g',
    ],
    'UOVA': [
        'Uova: 1 pezzo',
        'Albumi: Q.B.',
    ],
    'PROTEINE VEGETALI': [
        'Tofu: 2 porzioni',
        'Tempeh: 1 porzione',
    ],
    'LATTICINI': [
        'Yogurt greco: Q.B.',
        'Ricotta: 2 confezioni',
    ],
    'CEREALI E CARBOIDRATI': [
        'Pane integrale: 100g',
        'Fette biscottate: 1 confezione',
        'Wasa fibre: 1 pacchetto',
        'Crackers: Q.B.',
        'Riso basmati: 60g',
        'Pasta: 130g',
        'Pasta integrale: 60g',
        'Quinoa: 60g',
        'Avena: Q.B.',
    ],
    'LEGUMI': [
        'Ceci: 120g',
        'Hummus: 1 confezione',
    ],
    'VERDURE': [
        'Insalata: 50g + Q.B.',
        'Pomodorini: 400g',
        'Carote: 400g',
        'Zucchine: 3 pezzi',
        'Cavolo: 1 cespo',
        'Funghi: 200g',
        'Porri: 2 pezzi',
        'Finocchi: 2 pezzi',
        'Zucca: 300g',
        'Patate: 200g',
        'Bieta: 1 mazzo',
    ],
    'FRUTTA': [
        'Mele: 3 pezzi',
        'Banane: 2 pezzi',
        'Arance: 4 pezzi',
        'Avocado: 2 pezzi',
    ],
    'FRUTTA SECCA E SEMI': [
        'Frutta secca: 200g',
        'Pinoli: Q.B.',
        'Semi chia: Q.B.',
        'Cocco scaglie: Q.B.',
        'Granola: 200g',
    ],
    'CONDIMENTI E DISPENSA': [
        'Burro arachidi: Q.B.',
        'Marmellata: 1 vasetto',
        'Crema mandorle: Q.B.',
        'Senape: 1 vasetto',
        'Spezie varie',
        'Cioccolato 80%: 1 tavoletta',
        'Cacao: Q.B.',
        'Uvetta: Q.B.',
        'Olio EVO: Q.B.',
        'Tè verde: 1 confezione',
    ],
}

SETTIMANA_4 = {
    'CARNE E PESCE': [
        'Sogliola/Platessa: 150g',
        'Gamberi: 150g',
        'Tonno: 80g',
    ],
    'UOVA': [
        'Uova: 4 pezzi',
    ],
    'PROTEINE VEGETALI': [
        'Tofu: 100g + Q.B.',
    ],
    'LATTICINI': [
        'Yogurt greco: 3 vasetti',
        'Ricotta: 1 confezione',
        'Philadelphia: Q.B.',
    ],
    'CEREALI E CARBOIDRATI': [
        'Pane integrale: Q.B.',
        'Fette biscottate: 1 confezione',
        'Wasa fibre: 1 pacchetto',
        'Crackers: Q.B.',
        'Riso basmati: 60g',
        'Pasta: 60g',
        'Quinoa: 50g',
        'Avena: Q.B.',
    ],
    'LEGUMI': [
        'Ceci: 120g',
        'Fagioli cannellini: 150g',
    ],
    'VERDURE': [
        'Broccoli: 300g',
        'Spinaci: 200g',
        'Zucchine: 3 pezzi',
        'Carote: 400g',
        'Pomodorini: 400g',
        'Cavolo: 1 cespo',
        'Insalata: Q.B.',
        'Finocchi: 2 pezzi',
        'Porri: 2 pezzi',
        'Zucca: 300g',
        'Patate dolci: 150g',
        'Barbabietola: 2 pezzi',
    ],
    'FRUTTA': [
        'Mele: 3 pezzi',
        'Banane: 2 pezzi',
        'Kiwi: 2 pezzi',
        'Arance: 4 pezzi',
        'Pere: 2 pezzi',
        'Uva: 1 grappolo',
        'Avocado: 2 pezzi',
    ],
    'FRUTTA SECCA E SEMI': [
        'Frutta secca: 200g',
        'Granella arachidi: Q.B.',
        'Semi chia: Q.B.',
        'Cocco scaglie: Q.B.',
        'Granola: 200g',
    ],
    'CONDIMENTI E DISPENSA': [
        'Burro arachidi: 1 vasetto',
        'Marmellata: 1 vasetto',
        'Senape: 1 vasetto',
        'Olive: 1 vasetto',
        'Mais: 1 scatoletta',
        'Spezie varie',
        'Cioccolato 80%: 1 tavoletta',
        'Cacao: Q.B.',
        'Uvetta: Q.B.',
        'Pangrattato: Q.B.',
        'Olio EVO: Q.B.',
        'Tè verde: 1 confezione',
    ],
}

SETTIMANE = {'1': SETTIMANA_1, '2': SETTIMANA_2, '3': SETTIMANA_3, '4': SETTIMANA_4}

def genera(n, d):
    f = f"Lista_Settimana_{n}_DA_IMMAGINE.txt"
    with open(f, 'w', encoding='utf-8') as file:
        file.write("="*70 + f"\nLISTA DELLA SPESA - SETTIMANA {n}\n   Spesa della domenica\n" + "="*70 + "\n\n")
        for cat, items in d.items():
            file.write(f"{cat}\n" + "-"*70 + "\n")
            for i in items:
                file.write(f"  [ ] {i}\n")
            file.write("\n")
        file.write("="*70 + f"\nNOTE:\n- Generato: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n- Modifica: genera_liste_da_immagini.py\n" + "="*70 + "\n")
    return f

print("\n" + "="*70 + "\n🛒 GENERATORE LISTE DELLA SPESA\n" + "="*70 + "\n")
for n, d in SETTIMANE.items():
    print(f"✓ {genera(n, d)}")
print("\n" + "="*70 + "\n✅ FATTO! Quando cambi le immagini, modifica questo script e riesegui.\n" + "="*70 + "\n")
