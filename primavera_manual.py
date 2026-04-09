#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dati PRIMAVERA estratti manualmente dal testo grezzo del PDF
Leggendo sezione per sezione
"""

import json

PRIMAVERA_DATA = {
    "SETTIMANA_1": {
        "LUNEDI": {
            "colazione": "Pane segale 50 g + 50-60 g hummus + pomodorini saltati",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g cous cous 120 g lenticchie pomodori secchi pesto",
            "spuntino_2": "1 ricotta + cacao + stevia + cocco in scaglie",
            "cena": "Trancio di pesce infarinato con farina di mais 150 g + zucchine + 2 crostini integrali"
        },
        "MARTEDI": {
            "colazione": "Overnight porridge con mela cannella + 1 cucchiaino crema di mandorle",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g riso con 80 g tonno e zucchine carote",
            "spuntino_2": "Yogurt + 1 cucchiaio granola",
            "cena": "30 g triangolini mais con guacamole pomodorini + 1 rustichella di pollo + insalata di carote"
        },
        "MERCOLEDI": {
            "colazione": "50 g segale + ricotta + miele + 2 noci",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g riso basmati + 120 g ceci al latte di cocco + chips di carote alla paprika",
            "spuntino_2": "3-4 noci pecan + 1 banana",
            "cena": "Insalata con rucola 2 mozzarelline 100 g melone con aceto balsamico + 30 g pane segale patate lesse 200 g"
        },
        "GIOVEDI": {
            "colazione": "Yogurt greco SL + 1 manciata frutta secca + 2 cucchiai granola + 1 kiwi",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g cous cous con 150 g gamberetti piselli",
            "spuntino_2": "Yogurt + 1 cucchiaio granola",
            "cena": "1 confez. fiocchi di latte senza lattosio + insalata mela sedano noci"
        },
        "VENERDI": {
            "colazione": "2 fette integrali + marmellata + 2 cucchiaini burro arachidi",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g cous cous con 150 g gamberetti piselli",
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
            "pranzo": "120 g gnocchi pomodorini saltati con 70 g feta SL + 1 cucchiaio pesto",
            "spuntino_2": "1 frutto + 1 pezzo cioccolato",
            "cena": "Frittata di spinaci + chips di carote alla paprika + 2 crostini integrali"
        }
    },
    "SETTIMANA_2": {
        "LUNEDI": {
            "colazione": "Pane tostato 50 g + 50 g salmone affumicato + avocado",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "1 piadina integrale + avocado pomodorini + 2 uova sode + pane di segale 50-70 g",
            "spuntino_2": "1 ricotta + cacao + stevia + cocco in scaglie",
            "cena": "Tofu 100 g strapazzato con piselli e carote al curry + 2 crostini"
        },
        "MARTEDI": {
            "colazione": "Pane integrale 1 fetta + 2 cucchiaini burro arachidi + 2 cucchiaini marmellata",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "Insalata di fagiolini avocado cipollotto e basilico + 2 uova sode + insalata di chard",
            "spuntino_2": "Yogurt + 1 cucchiaio granola",
            "cena": "Insalata di avocado e rucola + 150 g patate barbabietola con aceto + 2 crostini"
        },
        "MERCOLEDI": {
            "colazione": "1 yogurt intero greco + cereali all bran prebiotic + 2 cucchiaini semi di lino tritati",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "1 fresella integrale + pomodori e basilico + insalata + 100 g primosale o mozzarella senza lattosio",
            "spuntino_2": "3-4 noci pecan + 1 banana",
            "cena": "Brazino/orata + 120 g piselli in umido + lievito alimentare + insalata con pomodori in + mais + 2 crostini"
        },
        "GIOVEDI": {
            "colazione": "Porridge overnight con kiwi velo di yogurt e gocce di cioccolato",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g riso basmati con 2 uova strapazzate e insalata",
            "spuntino_2": "1 quadrato cioccolato fondente + 1 frutto",
            "spuntino_2": "1 frutto + 1 pezzo cioccolato",
            "cena": "150 g pollo al curry + funghi carote cipolla asparagi + 2 crostini"
        },
        "VENERDI": {
            "colazione": "Pane segale 50 g + 50 g hummus + pomodorini",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "80 g salmone affumicato + 2 uova sode + insalata mista + 200 g patate",
            "spuntino_2": "1 frutto + 1 pezzo cioccolato",
            "cena": "Trancio di trota salmonata + asparagi + 2 crostini finocchi arancia uvetta + 2 crostini"
        },
        "SABATO": {
            "colazione": "1/3 di tortino fatto in casa",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g cous cous + 120 g lenticchie e fagioli melanzane al cannellini curry",
            "spuntino_2": "1 frutto + 1 manciata frutta secca",
            "cena": "Burger vegetale + insalata finocchi carote + 2 wasa + crostini"
        },
        "DOMENICA": {
            "colazione": "150 g pollo al curry + funghi carote cipolla + piselli con olio di cocco",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "Prazo: 60 g riso con asparagi e parmigiano",
            "spuntino_2": "1 frutto + 1 pezzo cioccolato",
            "cena": "PASTO LIBERO (con moderazione)"
        }
# TODO: Aggiungere SETTIMANA_3 e SETTIMANA_4

print("Dati PRIMAVERA estratti manualmente - 2 settimane complete")
