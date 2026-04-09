#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Menu completo da tutte le immagini
ESTATE: Settimana 1-4
INVERNO: Settimana 1-4 (Inverno1) + Settimana 5-8 (Inverno2)
"""

import json

MENU_COMPLETO = {
    "ESTATE": {
        "SETTIMANA_1": {
            "LUNEDI": {
                "colazione": "50 g pane di segale tostato + 1 quadrato cioccolato + 1 yogurt di soia + 1 kiwi",
                "spuntino_1": "10 mandorle o 4 noci o 2 cubetti parmigiano. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) (facoltativo)",
                "pranzo": "Farro con ceci e pomodorini + 2 cucchiai pesto",
                "spuntino_2": "1 pacchetto crackers di legumi",
                "cena": "Asparagi + 2 uova con scaglie grana e nocciole tostate + 3 wasa fibre",
                "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto (facoltativo)"
            },
            "MARTEDI": {
                "colazione": "50 g pane segale tostato + 2 fette bresaola + velo philadelphia",
                "spuntino_1": "10 mandorle o 4 noci o 2 cubetti parmigiano. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) (facoltativo)",
                "pranzo": "Riso nero con fagiolini e piselli + frittatina",
                "spuntino_2": "1 barretta low sugar equilibra",
                "cena": "Merluzzo con pomodorini e olive + wasa fibre + spinaci",
                "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto (facoltativo)"
            },
            "MERCOLEDI": {
                "colazione": "1 toast con pane integrale e prosciutto",
                "spuntino_1": "10 mandorle o 4 noci o 2 cubetti parmigiano. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) (facoltativo)",
                "pranzo": "2 patate in insalata con fagiolini e pesto + tonno",
                "spuntino_2": "Ricotta cacao + stevia + mandorle",
                "cena": "Insalata di pollo e finocchio ½ arancia e mandorle + wasa fibre",
                "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto (facoltativo)"
            },
            "GIOVEDI": {
                "colazione": "Porridge con mirtilli e cacao",
                "spuntino_1": "10 mandorle o 4 noci o 2 cubetti parmigiano. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) (facoltativo)",
                "pranzo": "Riso nero con salmone affumicato + zucchine e rucola",
                "spuntino_2": "3 wasa + 10 mandorle",
                "cena": "Insalata di farro ceci ½ avocado pomodorini",
                "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto (facoltativo)"
            },
            "VENERDI": {
                "colazione": "1 yogurt di soia + cereal all bran prebiotic + semi di lino/chia",
                "spuntino_1": "10 mandorle o 4 noci o 2 cubetti parmigiano. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) (facoltativo)",
                "pranzo": "Pasta integrale al dente con zucchine e feta",
                "spuntino_2": "1 quadrato cioccolato fondente + 10 mandorle",
                "cena": "Riso basmati + trancio di salmone gratinato + zucchine grigliate",
                "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto (facoltativo)"
            },
            "SABATO": {
                "colazione": "Chia pudding con fragole e latte di mandorle",
                "spuntino_1": "10 mandorle o 4 noci o 2 cubetti parmigiano. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) (facoltativo)",
                "pranzo": "Calamari e piselli",
                "spuntino_2": "3 gallette + crema di nocciole tostate",
                "cena": "PASTO LIBERO (con moderazione)",
                "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto (facoltativo)"
            },
            "DOMENICA": {
                "colazione": "Pancake con farina di avena e albume + 1 quadrato cioccolato fondente fuso",
                "spuntino_1": "10 mandorle o 4 noci o 2 cubetti parmigiano. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) (facoltativo)",
                "pranzo": "Riso basmati integrale con gamberi e zucchine",
                "spuntino_2": "1 yogurt + 1 frutto + 1 quadrato cioccolato",
                "cena": "Farinata di ceci al forno + asparagi + wasa",
                "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto (facoltativo)"
            }
        },
        "SETTIMANA_2": {
            "LUNEDI": {
                "colazione": "1 yogurt intero greco + cereali all bran prebiotic + 2 cucchiaini semi di lino tritati",
                "spuntino_1": "10 mandorle o 4 noci o 2 cubetti parmigiano. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) (facoltativo)",
                "pranzo": "Riso piselli asparagi e lievito alimentare",
                "spuntino_2": "1 ricotta + cacao + truvia + 5 mandorle",
                "cena": "Pane integrale tostato 2 uova ochio di bue + fagiolini e pomodori",
                "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto (facoltativo)"
            },
            "MARTEDI": {
                "colazione": "1 toast con pane integrale e prosciutto",
                "spuntino_1": "10 mandorle o 4 noci o 2 cubetti parmigiano. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) (facoltativo)",
                "pranzo": "Bowl di quinoa ½ avocado melanzane grigliate pomodorini secchi e ceci tostati",
                "spuntino_2": "1 pacchetto crackers di legumi",
                "cena": "Trancio di pesce spada + patate in insalata + spinaci",
                "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto (facoltativo)"
            },
            "MERCOLEDI": {
                "colazione": "1 yogurt intero greco + cereali all bran prebiotic + 2 cucchiaini semi di lino tritati",
                "spuntino_1": "10 mandorle o 4 noci o 2 cubetti parmigiano. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) (facoltativo)",
                "pranzo": "Piadina di farina di ceci con velo philadelphia ½ fette salmone affumicato + 5 wasa",
                "spuntino_2": "1 barretta low sugar equilibra",
                "cena": "Insalata di finocchi e mandorle in scaglie + salmone affumicato + 5 wasa",
                "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto (facoltativo)"
            },
            "GIOVEDI": {
                "colazione": "Porridge overnight con fragole velo di yogurt e gocce di cioccolato",
                "spuntino_1": "10 mandorle o 4 noci o 2 cubetti parmigiano. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) (facoltativo)",
                "pranzo": "Riso basmati con tonno e piselli",
                "spuntino_2": "Yogurt + fragole",
                "cena": "Insalata di pollo sedano noci salsa yogurt + pane integrale",
                "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto (facoltativo)"
            },
            "VENERDI": {
                "colazione": "1 yogurt di soia + cereal all bran prebiotic + semi di lino/chia",
                "spuntino_1": "10 mandorle o 4 noci o 2 cubetti parmigiano. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) (facoltativo)",
                "pranzo": "Farro con lenticchie e pomodorini",
                "spuntino_2": "1 quadrato cioccolato fondente + 3 noci",
                "cena": "wasa fibre + 150 g sogliola/platessa gratinata+ melanzane al pomodoro",
                "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto (facoltativo)"
            },
            "SABATO": {
                "colazione": "Cous cous carote piselli sgombro + fagiolini",
                "spuntino_1": "10 mandorle o 4 noci o 2 cubetti parmigiano. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) (facoltativo)",
                "pranzo": "Cous cous carote piselli sgombro + fagiolini",
                "spuntino_2": "1 yogurt + 1 quadrato cioccolato",
                "cena": "PASTO LIBERO (con moderazione)",
                "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto (facoltativo)"
            },
            "DOMENICA": {
                "colazione": "Pancake con farina di avena e albume + 1 quadrato cioccolato fondente",
                "spuntino_1": "10 mandorle o 4 noci o 2 cubetti parmigiano. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) (facoltativo)",
                "pranzo": "Gnocchi o spatzles con crema di zucchine ricotta",
                "spuntino_2": "1 gelato 2 gusti",
                "cena": "Insalata greca con feta cipolla cetrioli pomodori + wasa",
                "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto (facoltativo)"
            }
        },
        "SETTIMANA_3": {
            "LUNEDI": {
                "colazione": "Porridge caldo con gocce di cioccolato",
                "spuntino_1": "10 mandorle o 4 noci o 2 cubetti parmigiano. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) (facoltativo)",
                "pranzo": "Insalata mista con noci e fiocchi di latte SL + pane integrale",
                "spuntino_2": "1 barretta equilibra",
                "cena": "Insalata di 2 fettine pollo con pomodori ½ avocado mais + crostini di pane integrale",
                "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto (facoltativo)"
            },
            "MARTEDI": {
                "colazione": "3 wasa + velo yogurt + crema di nocciole tostate",
                "spuntino_1": "10 mandorle o 4 noci o 2 cubetti parmigiano. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) (facoltativo)",
                "pranzo": "Riso nero con feta + zucchine e menta",
                "spuntino_2": "3 gallette + mix pistacchi/mandorle",
                "cena": "polpo + patate + insalata di finocchi e carote",
                "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto (facoltativo)"
            },
            "MERCOLEDI": {
                "colazione": "Pane integrale + 1 quadrato cioccolato fondente fuso + 1 yogurt intero",
                "spuntino_1": "10 mandorle o 4 noci o 2 cubetti parmigiano. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) (facoltativo)",
                "pranzo": "Cous cous lenticchie melanzane pomodorini",
                "spuntino_2": "1 yogurt + cacao + stevia",
                "cena": "riso basmati + bocconcini pollo al curry/curcuma con carote e zucchine",
                "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto (facoltativo)"
            },
            "GIOVEDI": {
                "colazione": "Pane tostato 50 g + 1 uovo strapazzate + ½ avocado",
                "spuntino_1": "10 mandorle o 4 noci o 2 cubetti parmigiano. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) (facoltativo)",
                "pranzo": "60 g quinoa con 120 g ceci 50 g feta pomodorini 1 cucchiaio pesto. O quinoa fagioli rossi porro zenzero fresco pinoli uvetta limone",
                "spuntino_2": "3 wasa + ½ confezione fiocchi di latte",
                "cena": "Insalata cavolo mela noci + tofu o tempeh alla paprika + 3 wasa",
                "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto (facoltativo)"
            },
            "VENERDI": {
                "colazione": "1 bicchiera di kefir + muesli + semi di lino/chia",
                "spuntino_1": "10 mandorle o 4 noci o 2 cubetti parmigiano. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) (facoltativo)",
                "pranzo": "quinoa con tonno e asparagi",
                "spuntino_2": "1 barretta equilibra",
                "cena": "Carpaccio pesce spada + melanzane grigliate + insalata di finocchi e zucchine + pane integrale",
                "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto (facoltativo)"
            },
            "SABATO": {
                "colazione": "Porridge con ½ banana cannella e 1 quadrato cacao",
                "spuntino_1": "10 mandorle o 4 noci o 2 cubetti parmigiano. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) (facoltativo)",
                "pranzo": "1 piadina integrale + hummus + pomodori secchi bieta",
                "spuntino_2": "1 frutto + 1 manciata frutta secca",
                "cena": "PASTO LIBERO (con moderazione)",
                "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto (facoltativo)"
            },
            "DOMENICA": {
                "colazione": "Pancake con farina di avena e albume + crema di frutta secca 100%",
                "spuntino_1": "10 mandorle o 4 noci o 2 cubetti parmigiano. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) (facoltativo)",
                "pranzo": "60 g pasta integrale con ricotta e zucca",
                "spuntino_2": "1 frutto + 1 pezzo cioccolato",
                "cena": "Pesce al forno + patate + insalata di finocchi uvetta ½ arancia",
                "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto (facoltativo)"
            }
        },
        "SETTIMANA_4": {
            "LUNEDI": {
                "colazione": "1 yogurt di soia naturale + cereali all bran prebiotic + 2 cucchiaini semi di lino tritati",
                "spuntino_1": "10 mandorle + 3 wasa",
                "pranzo": "Riso basmati piselli carote e 2 uova strapazzate",
                "spuntino_2": "10 mandorle + 3 wasa",
                "cena": "pollo alle mandorle (vedi ricetta) + zucchine e carote saltate + 4 wasa",
                "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto (facoltativo)"
            },
            "MARTEDI": {
                "colazione": "50 g pane segale tostato + 2 fette bresaola + velo philadelphia",
                "spuntino_1": "10 mandorle + 3 wasa",
                "pranzo": "Insalata patate lesse ceci fagiolini pomodori al pesto",
                "spuntino_2": "1 yogurt greco 2% + 1 manciata mirtilli",
                "cena": "Vellutata di zucca + frittatina di spinaci con 2 uova + 4-5 wasa",
                "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto (facoltativo)"
            },
            "MERCOLEDI": {
                "colazione": "1 yogurt intero greco + cereali all bran prebiotic + 2 cucchiaini semi di lino tritati",
                "spuntino_1": "10 mandorle + 3 wasa",
                "pranzo": "Insalata di pollo caesar salad (vedi ricetta) + crostini integrali",
                "spuntino_2": "3 wasa + 20 g ceci secchi tostati",
                "cena": "Insalata di gamberi mango e mandorle (vedi ricetta) + 4-5 wasa",
                "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto (facoltativo)"
            },
            "GIOVEDI": {
                "colazione": "1 toast integrale tacchino e formaggio",
                "spuntino_1": "10 mandorle + 3 wasa",
                "pranzo": "Zucchine al forno ripieno di carne macinate di tacchino + insalata mista",
                "spuntino_2": "1 yogurt greco 0% + 8 mandorle + truvia",
                "cena": "Avocado toast con salmone affumicato e pane integrale",
                "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto (facoltativo)"
            },
            "VENERDI": {
                "colazione": "1 yogurt + cacao + 3 noci + muesli",
                "spuntino_1": "10 mandorle + 3 wasa",
                "pranzo": "Farro con salmone affumicato e pomodorini",
                "spuntino_2": "1 quadrato cioccolato fondente + 10 mandorle",
                "cena": "Sogliola impanata con farina di mais + insalata di finocchi e arance + pane integrale 50 g",
                "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto (facoltativo)"
            },
            "SABATO": {
                "colazione": "2 uova occhio di bue + ¼ avocado + 1 fetta pane integrale",
                "spuntino_1": "10 mandorle + 3 wasa",
                "pranzo": "1 piadina di farro con hummus e verdura grigliata",
                "spuntino_2": "3 gallette + crema di nocciole tostate",
                "cena": "PASTO LIBERO (con moderazione)",
                "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto (facoltativo)"
            },
            "DOMENICA": {
                "colazione": "Frittaina di albume + 1 quadrato cioccolato fuso + 1 fetta pane integrale tostato",
                "spuntino_1": "10 mandorle + 3 wasa",
                "pranzo": "Pasta integrale con melanzane pomodorini e ricotta stagionata",
                "spuntino_2": "1 yogurt + 1 frutto",
                "cena": "Insalata di farro con lenticchie cipollotti pomodori",
                "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto (facoltativo)"
            }
        }
    },
    "INVERNO": {
        "SETTIMANA_1": {
            "LUNEDI": {
                "colazione": "Yogurt greco SL + 1 manciata frutta secca + 2 cucchiai granola + uva a pezzetti",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "Bruschette di pane di segale 70 g (1 fetta grande) + pomodorini saltati e hummus + insalata barbabietola",
                "spuntino_2": "1 ricotta + cacao + stevia + cocco in scaglie",
                "cena": "Insalata cavolo carote yogurt senape limone + 2 uova + 3 wasa fibre",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "MARTEDI": {
                "colazione": "Overnight porridge con mela cannella + 1 cucchiaino crema di mandorle",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "60 g riso con 2 uova strapazzate piselli zucchine carote al curry",
                "spuntino_2": "Yogurt + 1 cucchiaio granola",
                "cena": "Merluzzo infarinato con mais + 3 wasa fibre + spinaci",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "MERCOLEDI": {
                "colazione": "1 toast con ½ avocado + 1 uovo + 1 spremuta",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "Es. mensa verdura + secondo + 1 bocconcino pane integrale",
                "spuntino_2": "3-4 noci pecan + 1 banana",
                "cena": "Insalata di 150 g pollo e finocchio ½ arancia e guacamole + 30 g tortilla",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "GIOVEDI": {
                "colazione": "Yogurt greco SL + 1 manciata frutta secca + 2 cucchiai granola + 1 kiwi",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "60 g riso nero con 150 g gamberetti e piselli",
                "spuntino_2": "Yogurt + 1 cucchiaio granola",
                "cena": "Tofu 80-100 g con cipolla caramellata + insalata cavolo + aceto balsamico + 3 wasa",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "VENERDI": {
                "colazione": "2 fette integrali + marmellata + 2 cucchiaini burro arachidi",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "60 g pasta integrale al dente con broccoli e 70 g feta",
                "spuntino_2": "1 quadrato cioccolato fondente + 3 noci",
                "cena": "Patate dolci paprika all'olio di cocco 200 g + 1 trancio salmone gratinato + porri saltati",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "SABATO": {
                "colazione": "1 fetta pane integrale + velo philadelphia + marmellata",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "60 g pasta di avena con broccoli uvetta e pinoli + pangrattato",
                "spuntino_2": "1 frutto + 1 manciata frutta secca",
                "cena": "PASTO LIBERO (con moderazione)",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "DOMENICA": {
                "colazione": "1 fetta pane integrale + 1 uovo + ½ avocado + 1 spremuta",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "120 g gnocchi con 120 g piselli + funghi al latte di cocco e curcuma",
                "spuntino_2": "1 frutto + 1 pezzo cioccolato",
                "cena": "Vellutata latte di cocco zucca patate + 70-80 g tempeh grigliato + 3 wasa con paprika",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            }
        },
        "SETTIMANA_2": {
            "LUNEDI": {
                "colazione": "1 yogurt intero greco + cereali all bran prebiotic + 2 cucchiaini semi di lino tritati",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "60 g pasta di avena con 120 g piselli funghi latte cocco con curcuma",
                "spuntino_2": "1 ricotta + cacao + stevia + cocco in scaglie",
                "cena": "50 g pane integrale + insalata 120 g ceci ½ avocado pomodorini 100 g gamberi",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "MARTEDI": {
                "colazione": "Pane integrale 1 fetta + 2 cucchiaini burro arachidi + 2 cucchiaini marmellata",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "Insalata di 150 g fagioli rossi cavolo noci senape + 3 wasa",
                "spuntino_2": "Yogurt + 1 cucchiaio granola",
                "cena": "Bowl 40 g riso basmati + tofu strapazzato con paprika ½ scatoletta mais broccoli saltati carote",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "MERCOLEDI": {
                "colazione": "1 yogurt intero greco + cereali all bran prebiotic + 2 cucchiaini semi di lino tritati",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "Es. mensa",
                "spuntino_2": "3-4 noci pecan + 1 banana",
                "cena": "Frittata con 2 uova bieta e feta + finocchi/carote + 3 wasa",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "GIOVEDI": {
                "colazione": "Porridge overnight con kiwi velo di yogurt e gocce di cioccolato",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "60 g risotto funghi parmigiano",
                "spuntino_2": "Yogurt + 1 cucchiaio granola",
                "cena": "120 g coniglio olive pinoli + broccoli saltati + 3 wasa",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "VENERDI": {
                "colazione": "1 yogurt + cereal all bran prebiotic + semi di lino/chia tritati",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "60 g riso basmati + 40 g lenticchie secche rosse decorticate dahl con latte di cocco spezie coriandolo",
                "spuntino_2": "1 quadrato cioccolato fondente + 3 noci",
                "cena": "3 wasa fibre + 150 g sogliola/platessa gratinata + zucca al rosmarino",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "SABATO": {
                "colazione": "Pane tostato 50 g + ½ avocado + strapazzate + fette biscottate",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "60 g pasta integrale 80 g sgombro pomodorini capperi olive",
                "spuntino_2": "1 frutto + 1 manciata frutta secca",
                "cena": "PASTO LIBERO (con moderazione)",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "DOMENICA": {
                "colazione": "Pancake con farina di avena e albume + 1 quadrato cioccolato fondente",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "120 g gnocchi pomodorini saltati 70-80 g stracciatella",
                "spuntino_2": "1 frutto + 1 pezzo cioccolato",
                "cena": "4-5 falafel + salsa yogurt + insalata mista + 3 wasa",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            }
        },
        "SETTIMANA_3": {
            "LUNEDI": {
                "colazione": "Porridge caldo con gocce di cioccolato",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "60 g pasta di avena con fiocchi di latte e zucchine",
                "spuntino_2": "1 ricotta + cacao + stevia + cocco in scaglie",
                "cena": "120 g pollo con farina di riso funghi porri e salsa soia + crostini di pane integrale",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "MARTEDI": {
                "colazione": "2 fette biscottate integrali + velo yogurt SL + marmellata",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "Insalata finocchi mela uvetta noci tostate + 120 g ceci + 3 wasa",
                "spuntino_2": "Yogurt + 1 cucchiaio granola",
                "cena": "Polpo + 200 g patate + insalata finocchi carote",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "MERCOLEDI": {
                "colazione": "Pane integrale 1 fetta + 1 quadrato cioccolato fondente fuso + 1 yogurt intero",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "Es. mensa",
                "spuntino_2": "3-4 noci pecan + 1 banana",
                "cena": "70 g pasta di legumi al pomodoro e lievito alimentare + pane 50 g",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "GIOVEDI": {
                "colazione": "Pane tostato 50 g + 1 uovo strapazzate + ½ avocado",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "60 g quinoa con 120 g ceci 50 g feta pomodorini 1 cucchiaio pesto. O quinoa fagioli rossi porro zenzero fresco pinoli uvetta limone",
                "spuntino_2": "Yogurt + 1 cucchiaio granola",
                "cena": "Insalata cavolo mela noci + tofu o tempeh alla paprika + 3 wasa",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "VENERDI": {
                "colazione": "1 bicchiera di kefir + muesli + semi di lino/chia",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "60 g riso basmati + bocconcini pollo al curry/curcuma con carote e zucchine",
                "spuntino_2": "1 quadrato cioccolato fondente + 3 noci",
                "cena": "Trancio di pesce al cartoccio + patate speziate 200 g + 1 trancio di salmone gratinato + porri saltati",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "SABATO": {
                "colazione": "Porridge con ½ banana cannella e 1 quadrato cacao",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "1 piadina integrale + hummus + pomodori secchi bieta",
                "spuntino_2": "1 frutto + 1 manciata frutta secca",
                "cena": "PASTO LIBERO (con moderazione)",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "DOMENICA": {
                "colazione": "Pancake con farina di avena e albume + crema di frutta secca 100%",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "60 g pasta integrale con ricotta e zucca",
                "spuntino_2": "1 frutto + 1 pezzo cioccolato",
                "cena": "Pesce al forno + patate + insalata di finocchi uvetta ½ arancia",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            }
        },
        "SETTIMANA_4": {
            "LUNEDI": {
                "colazione": "Yogurt greco SL + 1 manciata frutta secca + 2 cucchiai granola + uva a pezzetti",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "60 g riso basmati 80-100 g tofu latte di cocco zucchine carote curry salsa soia",
                "spuntino_2": "1 ricotta + cacao + stevia + cocco in scaglie",
                "cena": "Polpette zucca con ripieno di formaggio SL con pangrattato e specie + 2 wasa",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "MARTEDI": {
                "colazione": "Overnight porridge con mela cannella + 1 cucchiaino crema di mandorle",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "60 g pasta con cavolfiore e 80 g tonno olive",
                "spuntino_2": "Yogurt + 1 cucchiaio granola",
                "cena": "Insalata di spinacino feta per noci aceto balsamic barbabietola + 3 wasa",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "MERCOLEDI": {
                "colazione": "1 toast con ½ avocado + 1 uovo + 1 spremuta",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "Es. mensa",
                "spuntino_2": "3-4 noci pecan + 1 banana",
                "cena": "Pollo con farina di riso e curcuma al forno con spezie + zucca al forno",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "GIOVEDI": {
                "colazione": "Yogurt greco SL + 1 manciata frutta secca + 2 cucchiai granola + 1 kiwi",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "Bowl 50 g quinoa spinacino 120 g ceci alla paprika ½ avocado pomodorini 150 g patata dolce e lime zest",
                "spuntino_2": "Yogurt + 1 cucchiaio granola",
                "cena": "Patate dolci 200 g + 2 uova + rusticchela + zucca al forno con spezie + 3 wasa",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "VENERDI": {
                "colazione": "2 fette integrali + marmellata + 2 cucchiaini burro arachidi",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "Pad thai con spaghetti di riso 60 g 150 g gamberi granella arachidi zucchine carote saltati",
                "spuntino_2": "1 quadrato cioccolato fondente + 3 noci",
                "cena": "Sogliola imparata con farina di mais + insalata di finocchi e arance + pane integrale 50 g",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "SABATO": {
                "colazione": "1 fetta pane integrale + velo philadelphia + marmellata",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "60 g riso basmati + 150 g fagioli cannellini cavolo lilevito alimentare con curcuma e lilevito",
                "spuntino_2": "1 frutto + 1 manciata frutta secca",
                "cena": "PASTO LIBERO (con moderazione)",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "DOMENICA": {
                "colazione": "1 fetta pane integrale + 1 uovo + ½ avocado + 1 spremuta",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "60 g pasta integrale con ricotta e zucca",
                "spuntino_2": "1 frutto + 1 pezzo cioccolato",
                "cena": "2 calamari ripieni insalata spinacino mela noci miele aceto balsamico",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            }
        },
        "SETTIMANA_5": {
            "LUNEDI": {
                "colazione": "Pane segale 50 g + 50-60 g hummus + pomodorini saltati",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "60 g riso + 120 g lenticchie + zucca",
                "spuntino_2": "1 ricotta + cacao + stevia + cocco in scaglie",
                "cena": "50 g pane tostato + 1 burger di soia + cipolla caramellata + pomodori/ insalata",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "MARTEDI": {
                "colazione": "Overnight porridge con mela cannella + 1 cucchiaino crema di mandorle",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "Insalata con 50 g tonno + 1 uovo sodo + pomodorini mais + 50 g pane segale o integrale",
                "spuntino_2": "Yogurt + 1 cucchiaio granola",
                "cena": "150 g orata/branzino con pomodorini e olive + insalata mista + 3 wasa",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "MERCOLEDI": {
                "colazione": "70 g piadina integrale o di farro o kamut + 120 g hummus + pomodori/insalata",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "120 g ceci in insalata con ½ avocado, pomodorini, valeriana + 50 g pane di segale o integrale",
                "spuntino_2": "Yogurt + 1 cucchiaio granola",
                "cena": "3 wasa + vellutata di zucca + 120 g conigli olive tostati + 120 g",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "GIOVEDI": {
                "colazione": "Insalata finocchi arance uvetta pinoli + 2 wasa",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "120 g ceci in insalata con ½ avocado, pomodorini, valeriana + 50 g pane di segale o integrale",
                "spuntino_2": "1 frutto + 1 manciata frutta secca",
                "cena": "100 g ricotta/100 g primo sale senza lattosio + 50 g pane segale + insalata di finocchi cavalo saltato + 50 g pane segale",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "VENERDI": {
                "colazione": "1 fetta pane integrale + velo philadelphia + marmellata",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "150 g gamberetti ½ avocado pomodorini 50 g feta + 2 wasa",
                "spuntino_2": "1 quadrato cioccolato fondente + 3 noci",
                "cena": "Tempeh grigliato con paprika + insalata di finocchi noci e arancia + 3 wasa",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "SABATO": {
                "colazione": "50 g salmone affumicato + ½ avocado",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "Trancio di trota salmonata + broccoli e cavolfiori con uvetta e pinoli + 50 g pane integrale",
                "spuntino_2": "1 frutto + 1 manciata frutta secca",
                "cena": "PASTO LIBERO (con moderazione)",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "DOMENICA": {
                "colazione": "60 g spaghetti di riso con ½ tofu scrambled o gamberetti carote zucchine salsa soia",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "Frittata di spinaci con 2 uova e cubetti di feta + broccoli e carote al vapore",
                "spuntino_2": "1 frutto + 1 pezzo cioccolato",
                "cena": "1 quadrato cioccolato 80% (facoltativo)",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            }
        },
        "SETTIMANA_6": {
            "LUNEDI": {
                "colazione": "60 g riso nero con 70 g salmone affumicato e piselli",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "150 g gamberetti ½ avocado pomodorini 50 g feta + 2 wasa",
                "spuntino_2": "1 ricotta + cacao + stevia + cocco in scaglie",
                "cena": "50 g pane tostato + 50 g salmone affumicato + ½ avocado",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "MARTEDI": {
                "colazione": "Pane integrale 1 fetta + 2 cucchiaini burro arachidi + 2 cucchiaini marmellata",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "60 g riso con 70 g tofu carote zucchine al curry e latte di cocco",
                "spuntino_2": "Yogurt + 1 cucchiaio granola",
                "cena": "Minestrone di legumi 120 g con parmigiano + 30 g crostini",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "MERCOLEDI": {
                "colazione": "1 yogurt intero greco + cereali all bran prebiotic + 2 cucchiaini semi di lino tritati",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "50 g pane di segale + 200 g fiocchi di latte senza lattosio e senza lattosio+ fagioli",
                "spuntino_2": "3-4 noci pecan + 1 banana",
                "cena": "Frittata con 2 uova + zucchine e carote saltate al latte + 2 wasa",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "GIOVEDI": {
                "colazione": "Porridge overnight con kiwi velo di yogurt e gocce di cioccolato",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "60 g miglio o riso con zucca e 120 g ceci",
                "spuntino_2": "Yogurt + 1 cucchiaio granola",
                "cena": "Tempeh grigliato con paprika + insalata di finocchi noci e arancia + 3 wasa",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "VENERDI": {
                "colazione": "Pane segale 50 g + 50 g hummus + pomodorini",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "1 quadrato cioccolato fondente + 3 noci",
                "spuntino_2": "1 quadrato cioccolato fondente + 3 noci",
                "cena": "Zucca in padella al rosmarino o cavolo viola + 2 uova + insalata",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "SABATO": {
                "colazione": "Pane tostato 50 g + 50 g salmone affumicato + ½ avocado",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "Broccoli filanti al forno con formaggio a scelta senza lattosio 80 g + 50 g pane",
                "spuntino_2": "1 frutto + 1 manciata frutta secca",
                "cena": "PASTO LIBERO (con moderazione)",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "DOMENICA": {
                "colazione": "Zucca in padella al rosmarino o cavolo viola + 120 g pesce e 200 g patate + insalata finocchi mela uvetta noci",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "150 g pesce e 200 g patate + insalata finocchi mela uvetta noci",
                "spuntino_2": "1 frutto + 1 pezzo cioccolato",
                "cena": "Vellutata di zucca + 120 g ceci al rosmarino",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            }
        },
        "SETTIMANA_7": {
            "LUNEDI": {
                "colazione": "Porridge con pera e cannella + 1 quadrato cioccolato o crema di mandorle 100%",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "Pane segale 50 g + 120 g hummus cannellini barbabietola + carote",
                "spuntino_2": "1 ricotta + cacao + stevia + cocco in scaglie",
                "cena": "Minestrone di 120 g legumi con parmigiano + 30 g crostini",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "MARTEDI": {
                "colazione": "Pane segale 50 g + 50 g hummus + pomodorini",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "120 g gnocchi con pomodorini saltati e stracciatella senza lattosio",
                "spuntino_2": "Yogurt + 1 cucchiaio granola",
                "cena": "Frittata (2 uova) di spinaci + zucca in padella + 2 wasa",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "MERCOLEDI": {
                "colazione": "Torretta di 4 fette biscottate con strati di yogurt e marmellata 3 cucchiaini",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "Insalata 100 g ceci ½ avocado pomodorini 50 g pomodorini 50 g feta senza lattosio+ 3 wasa",
                "spuntino_2": "Yogurt + 1 cucchiaio granola",
                "cena": "Polpette di tofu al pomodoro 70 g insalata finocchi/ arance e 3 noci + 50 g pane",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "GIOVEDI": {
                "colazione": "Pane tostato 50 g + 1 uovo strapazzate + ½ avocado",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "Insalata 2 mozzarella senza lattosio, scaglie di grana e noci + 50 g pane integrale",
                "spuntino_2": "1 frutto + 1 manciata frutta secca",
                "cena": "Trancio di pesce in umido + insalata di cavolo con aceto + 2 wasa",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "VENERDI": {
                "colazione": "1 toast integrale + 2 fette prosciutto e formaggio",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "60 g riso basmati con cavolo verza e 150 g fagiolini cannellini alla curcuma",
                "spuntino_2": "1 quadrato cioccolato fondente + 3 noci",
                "cena": "50 g pane di segale con crema di ½ avocado e 2 uova + insalata",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "SABATO": {
                "colazione": "Gnocchi 120 g + crema di zucca + capriolo 70 g",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "Orata al forno (circa 150 g a persona) + patate + insalata mista",
                "spuntino_2": "1 frutto + 1 manciata frutta secca",
                "cena": "PASTO LIBERO (con moderazione)",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "DOMENICA": {
                "colazione": "½ panetto cubetti di tofu al latte di cocco e curry + carote/zucchine",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "Pesce al forno + patate + insalata di finocchi mela uvetta noci",
                "spuntino_2": "1 frutto + 1 pezzo cioccolato",
                "cena": "Pesce al forno + patate + insalata di finocchi uvetta noci",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            }
        },
        "SETTIMANA_8": {
            "LUNEDI": {
                "colazione": "Yogurt greco SL + 1 manciata frutta secca + 2 cucchiai granola + uva a pezzetti",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "60 g farro con 2 cucchiai pesto e pomodorini + 70 g cubetti tofu affumicato",
                "spuntino_2": "1 ricotta + cacao + stevia + cocco in scaglie",
                "cena": "120 g coniglio carciofi + 150 g patate con olive",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "MARTEDI": {
                "colazione": "60 g farro con 2 cucchiai pesto e pomodorini + 70 g cubetti tofu affumicato",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "120 g lenticchie con zucca in padella + 2 wasa",
                "spuntino_2": "Yogurt + 1 frutto",
                "cena": "150 g mozzarella senza lattosio, scaglie di grana e noci + 50 g pane integrale",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "MERCOLEDI": {
                "colazione": "50 g pane segale + marmellata e burro arachidi",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "1 piadina integrale con hummus (120 g ceci) + melanzane grigliate",
                "spuntino_2": "3-4 noci pecan + 1 banana",
                "cena": "150 g filetto di trota salmonata + piselli e funghi + 50 g pane segale",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "GIOVEDI": {
                "colazione": "Overnight porridge 30 g fiocchi d'avena + mirtilli e cocco grattugiato",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "60 g riso basmati + 2 uova strapazzate cavolo saltato con olio di cocco",
                "spuntino_2": "Yogurt + 1 cucchiaio granola",
                "cena": "Zuppa di latte di cocco spinaci patate zucca 120 g ceci + 2 wasa",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "VENERDI": {
                "colazione": "3 fette integrali + philadelphia e marmellata",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "60 g riso con zucca e lenticchie 120 g",
                "spuntino_2": "1 quadrato cioccolato fondente + 3 noci",
                "cena": "2 uova all'occhio di bue + 50 g pane segale + ½ avocado + insalata",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "SABATO": {
                "colazione": "1 toast integrale + 2 fette prosciutto e formaggio",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "Broccoli filanti al forno con formaggio a scelta senza lattosio 80 g + 50 g pane",
                "spuntino_2": "1 frutto + 1 manciata frutta secca",
                "cena": "PASTO LIBERO (con moderazione)",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            },
            "DOMENICA": {
                "colazione": "Vellutata di zucca + 120 g ceci al rosmarino",
                "spuntino_1": "2 fette galbusera. Oppure 1 pacchetto crackers di legumi o protein G (es. misura) o integrali galbusera o 30 g chips probios. Se ti svegli dopo: 1 manciata frutta secca + 2 gallette/wasa",
                "pranzo": "1 quadrato cioccolato fondente + 3 noci",
                "spuntino_2": "1 frutto + 1 pezzo cioccolato",
                "cena": "Pesce al forno + patate + insalata di finocchi mela uvetta noci",
                "dopo_cena": "1 quadrato cioccolato 80% (facoltativo)"
            }
        }
    }
}

with open('menu_settimanale.json', 'w', encoding='utf-8') as f:
    json.dump(MENU_COMPLETO, f, ensure_ascii=False, indent=2)

print("✅ Menu completo salvato!")
print("📊 Struttura:")
print(f"  - ESTATE: 4 settimane")
print(f"  - INVERNO: 8 settimane (1-4 da Inverno1, 5-8 da Inverno2)")
