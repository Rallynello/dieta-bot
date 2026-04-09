#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Menu dettagliato dal piano dietico - Estratto dalle immagini
"""

import json

MENU_SETTIMANALE = {
    "SETTIMANA_1": {
        "LUNEDI": {
            "colazione": "Yogurt greco SL + 1 manciata frutta secca + 2 cucchiai granola + uva a pezzetti",
            "spuntino_1": "2 fette galbusera, oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "Bruschette di pane di segale 70g (1 fetta grande) + pomodorini saltati e hummus + insalata barbabietola",
            "spuntino_2": "1 ricotta + cacao + stevia + cocco in scaglie",
            "cena": "Insalata cavolo carote yogurt senape limone + 2 uova + 3 wasa fibre",
            "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
        },
        "MARTEDI": {
            "colazione": "Overnight porridge con mela cannella + 1 cucchiaino crema di mandorle",
            "spuntino_1": "2 fette galbusera, oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60g riso con 2 uova strapazzate piselli zucchine carote al curry",
            "spuntino_2": "Yogurt + 1 cucchiaio granola",
            "cena": "Merluzzo infarinato con mais + 3 wasa fibre + spinaci",
            "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
        },
        "MERCOLEDI": {
            "colazione": "1 toast con ½ avocado + 1 uovo + 1 spremuta",
            "spuntino_1": "2 fette galbusera, oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "Es. mensa verdura + secondo + 1 bocconcino pane integrale",
            "spuntino_2": "3-4 noci pecan + 1 banana",
            "cena": "Insalata di 150g pollo e finocchio ½ arancia e guacamole + 30g tortilla",
            "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
        },
        "GIOVEDI": {
            "colazione": "Yogurt greco SL + 1 manciata frutta secca + 2 cucchiai granola + 1 kiwi",
            "spuntino_1": "2 fette galbusera, oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60g riso nero con 150g gamberetti e piselli",
            "spuntino_2": "Yogurt + 1 cucchiaio granola",
            "cena": "Tofu 80-100g con cipolla caramellata + insalata cavolo + aceto balsamico + 3 wasa",
            "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
        },
        "VENERDI": {
            "colazione": "2 fette integrali + marmellata + 2 cucchiaini burro arachidi",
            "spuntino_1": "2 fette galbusera, oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60g pasta integrale al dente con broccoli e 70g feta",
            "spuntino_2": "1 quadrato cioccolato fondente + 3 noci",
            "cena": "Patate dolci paprika all'olio di cocco 200g + 1 trancio salmone gratinato + porri saltati",
            "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
        },
        "SABATO": {
            "colazione": "1 fetta pane integrale + velo philadelphia + marmellata",
            "spuntino_1": "2 fette galbusera, oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60g pasta di avena con broccoli uvetta e pinoli + pangrattato",
            "spuntino_2": "1 frutto + 1 manciata frutta secca",
            "cena": "PASTO LIBERO (con moderazione)",
            "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
        },
        "DOMENICA": {
            "colazione": "1 fetta pane integrale + 1 uovo + ½ avocado + 1 spremuta",
            "spuntino_1": "2 fette galbusera, oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "120g gnocchi con 120g piselli + funghi al latte di cocco e curcuma",
            "spuntino_2": "1 frutto + 1 pezzo cioccolato",
            "cena": "Vellutata latte di cocco zucca patate + 70-80g tempeh grigliato + 3 wasa con paprika",
            "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
        }
    },
    "SETTIMANA_2": {
        "LUNEDI": {
            "colazione": "1 yogurt intero greco + cereali all bran prebiotic + 2 cucchiaini semi di lino tritati",
            "spuntino_1": "2 fette galbusera, oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60g pasta di avena con 120g piselli funghi latte cocco con curcuma",
            "spuntino_2": "1 ricotta + cacao + stevia + cocco in scaglie",
            "cena": "50g pane integrale + insalata 120g ceci ½ avocado pomodorini 100g gamberi",
            "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
        },
        "MARTEDI": {
            "colazione": "Pane integrale 1 fetta + 2 cucchiaini burro arachidi + 2 cucchiaini marmellata",
            "spuntino_1": "2 fette galbusera, oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "Insalata di 150g fagioli rossi cavolo noci senape + 3 wasa",
            "spuntino_2": "Yogurt + 1 cucchiaio granola",
            "cena": "Bowl 40g riso basmati + tofu strapazzato con paprika ½ scatoletta mais broccoli saltati carote",
            "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
        },
        "MERCOLEDI": {
            "colazione": "1 yogurt intero greco + cereali all bran prebiotic + 2 cucchiaini semi di lino tritati",
            "spuntino_1": "2 fette galbusera, oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "Es. mensa",
            "spuntino_2": "3-4 noci pecan + 1 banana",
            "cena": "Frittata con 2 uova bieta e feta + finocchi/carote + 3 wasa",
            "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
        },
        "GIOVEDI": {
            "colazione": "Porridge overnight con kiwi velo di yogurt e gocce di cioccolato",
            "spuntino_1": "2 fette galbusera, oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60g risotto funghi parmigiano",
            "spuntino_2": "Yogurt + 1 cucchiaio granola",
            "cena": "120g coniglio olive pinoli + broccoli saltati + 3 wasa",
            "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
        },
        "VENERDI": {
            "colazione": "1 yogurt + cereal all bran prebiotic + semi di lino/chia tritati",
            "spuntino_1": "2 fette galbusera, oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60g riso basmati + 40g lenticchie secche rosse decorticate dahl con latte di cocco spezie coriandolo",
            "spuntino_2": "1 quadrato cioccolato fondente + 3 noci",
            "cena": "3 wasa fibre + 150g sogliola/platessa gratinata + zucca al rosmarino",
            "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
        },
        "SABATO": {
            "colazione": "Pane tostato 50g + ½ avocado + strapazzate + fette biscottate",
            "spuntino_1": "2 fette galbusera, oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60g pasta integrale 80g sgombro pomodorini capperi olive",
            "spuntino_2": "1 frutto + 1 manciata frutta secca",
            "cena": "PASTO LIBERO (con moderazione)",
            "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
        },
        "DOMENICA": {
            "colazione": "Pancake con farina di avena e albume + 1 quadrato cioccolato fondente",
            "spuntino_1": "2 fette galbusera, oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "120g gnocchi pomodorini saltati 70-80g stracciatella",
            "spuntino_2": "1 frutto + 1 pezzo cioccolato",
            "cena": "4-5 falafel + salsa yogurt + insalata mista + 3 wasa",
            "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
        }
    },
    "SETTIMANA_3": {
        "LUNEDI": {
            "colazione": "Porridge caldo con gocce di cioccolato",
            "spuntino_1": "2 fette galbusera, oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60g pasta di avena con fiocchi di latte e zucchine",
            "spuntino_2": "1 ricotta + cacao + stevia + cocco in scaglie",
            "cena": "120g pollo con farina di riso funghi porri e salsa soia + crostini di pane integrale",
            "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
        },
        "MARTEDI": {
            "colazione": "2 fette biscottate integrali + velo yogurt SL + marmellata",
            "spuntino_1": "2 fette galbusera, oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "Insalata finocchi mela uvetta noci tostate + 120g ceci + 3 wasa",
            "spuntino_2": "Yogurt + 1 cucchiaio granola",
            "cena": "Polpo + 200g patate + insalata finocchi carote",
            "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
        },
        "MERCOLEDI": {
            "colazione": "Pane integrale 1 fetta + 1 quadrato cioccolato fondente fuso + 1 yogurt intero",
            "spuntino_1": "2 fette galbusera, oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "Es. mensa",
            "spuntino_2": "3-4 noci pecan + 1 banana",
            "cena": "70g pasta di legumi al pomodoro e lievito alimentare + pane 50g",
            "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
        },
        "GIOVEDI": {
            "colazione": "Pane tostato 50g + 1 uovo strapazzate + ½ avocado",
            "spuntino_1": "2 fette galbusera, oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60g quinoa con 120g ceci 50g feta pomodorini 1 cucchiaio pesto O quinoa fagioli rossi porro zenzero fresco pinoli uvetta limone",
            "spuntino_2": "Yogurt + 1 cucchiaio granola",
            "cena": "Insalata cavolo mela noci + tofu o tempeh alla paprika + 3 wasa",
            "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
        },
        "VENERDI": {
            "colazione": "1 bicchiera di kefir + muesli + semi di lino/chia",
            "spuntino_1": "2 fette galbusera, oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60g riso basmati + bocconcini pollo al curry/curcuma con carote e zucchine",
            "spuntino_2": "1 quadrato cioccolato fondente + 3 noci",
            "cena": "Trancio di pesce al cartoccio + patate speziate 200g + 1 trancio di salmone gratinato + porri saltati",
            "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
        },
        "SABATO": {
            "colazione": "Porridge con ½ banana cannella e 1 quadrato cacao",
            "spuntino_1": "2 fette galbusera, oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "1 piadina integrale + hummus + pomodori secchi bieta",
            "spuntino_2": "1 frutto + 1 manciata frutta secca",
            "cena": "PASTO LIBERO (con moderazione)",
            "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
        },
        "DOMENICA": {
            "colazione": "Pancake con farina di avena e albume + crema di frutta secca 100%",
            "spuntino_1": "2 fette galbusera, oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60g pasta integrale con ricotta e zucca",
            "spuntino_2": "1 frutto + 1 pezzo cioccolato",
            "cena": "Pesce al forno + patate + insalata di finocchi uvetta ½ arancia",
            "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
        }
    },
    "SETTIMANA_4": {
        "LUNEDI": {
            "colazione": "Yogurt greco SL + 1 manciata frutta secca + 2 cucchiai granola + uva a pezzetti",
            "spuntino_1": "2 fette galbusera, oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60g riso basmati 80-100g tofu latte di cocco zucchine carote curry salsa soia",
            "spuntino_2": "1 ricotta + cacao + stevia + cocco in scaglie",
            "cena": "Polpette zucca con ripieno di formaggio SL con pangrattato e specie + 2 wasa",
            "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
        },
        "MARTEDI": {
            "colazione": "Overnight porridge con mela cannella + 1 cucchiaino crema di mandorle",
            "spuntino_1": "2 fette galbusera, oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60g pasta con cavolfiore e 80g tonno olive",
            "spuntino_2": "Yogurt + 1 cucchiaio granola",
            "cena": "Insalata di spinacino feta per noci aceto balsamic barbabietola + 3 wasa",
            "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
        },
        "MERCOLEDI": {
            "colazione": "1 toast con ½ avocado + 1 uovo + 1 spremuta",
            "spuntino_1": "2 fette galbusera, oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "Es. mensa",
            "spuntino_2": "3-4 noci pecan + 1 banana",
            "cena": "Pollo con farina di riso e curcuma al forno con spezie + zucca al forno",
            "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
        },
        "GIOVEDI": {
            "colazione": "Yogurt greco SL + 1 manciata frutta secca + 2 cucchiai granola + 1 kiwi",
            "spuntino_1": "2 fette galbusera, oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "Bowl 50g quinoa spinacino 120g ceci alla paprika ½ avocado pomodorini 150g patata dolce e lime zest",
            "spuntino_2": "Yogurt + 1 cucchiaio granola",
            "cena": "Patate dolci 200g + 2 uova + rusticchela + zucca al forno con spezie + 3 wasa",
            "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
        },
        "VENERDI": {
            "colazione": "2 fette integrali + marmellata + 2 cucchiaini burro arachidi",
            "spuntino_1": "2 fette galbusera, oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "Pad thai con spaghetti di riso 60g 150g gamberi granella arachidi zucchine carote saltati",
            "spuntino_2": "1 quadrato cioccolato fondente + 3 noci",
            "cena": "Sogliola imparata con farina di mais + insalata di finocchi e arance + pane integrale 50g",
            "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
        },
        "SABATO": {
            "colazione": "1 fetta pane integrale + velo philadelphia + marmellata",
            "spuntino_1": "2 fette galbusera, oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60g riso basmati + 150g fagioli cannellini cavolo lilevito alimentare con curcuma e lilevito",
            "spuntino_2": "1 frutto + 1 manciata frutta secca",
            "cena": "PASTO LIBERO (con moderazione)",
            "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
        },
        "DOMENICA": {
            "colazione": "1 fetta pane integrale + 1 uovo + ½ avocado + 1 spremuta",
            "spuntino_1": "2 fette galbusera, oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60g pasta integrale con ricotta e zucca",
            "spuntino_2": "1 frutto + 1 pezzo cioccolato",
            "cena": "2 calamari ripieni insalata spinacino mela noci miele aceto balsamico",
            "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
        }
    }
}

# Salva in JSON
with open('menu_settimanale.json', 'w', encoding='utf-8') as f:
    json.dump(MENU_SETTIMANALE, f, ensure_ascii=False, indent=2)

print("✅ Menu DETTAGLIATO salvato in menu_settimanale.json")
