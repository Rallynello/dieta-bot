#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

with open('menu_settimanale.json', 'r', encoding='utf-8') as f:
    menu = json.load(f)

# Sostituisco tutto PRIMAVERA con i dati letti dalle immagini
menu['PRIMAVERA'] = {
    "SETTIMANA_1": {
        "LUNEDI": {
            "colazione": "Pane segale 50 g + 50-60 g hummus + pomodorini saltati",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g cous cous + 120 g lenticchie + pomodori secchi + pesto",
            "spuntino_2": "1 ricotta + cacao + stevia + cocco in scaglie",
            "cena": "Trancio di pesce infarinato con farina di mais 150 g + zucchine + 2 crostini integrali"
        },
        "MARTEDI": {
            "colazione": "Overnight porridge con mela cannella + 1 cucchiaino crema di mandorle",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "Insalata con sedano + 1/2 mela + 3 noci + 100 g tofu in friggitrice + pane 50 g",
            "spuntino_2": "Yogurt + 1 cucchiaio granola",
            "cena": "30 g triangolini mais con guacamole pomodorini + 1 rustichella di pollo + insalata di carote"
        },
        "MERCOLEDI": {
            "colazione": "50 g segale + ricotta + miele + 2 noci",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g riso con 80 g tonno e zucchine carote",
            "spuntino_2": "3-4 noci pecan + 1 banana",
            "cena": "Frittata di spinaci + chips di carote alla paprika + 2 crostini integrali"
        },
        "GIOVEDI": {
            "colazione": "Yogurt greco SL + 1 manciata frutta secca + 2 cucchiai burro arachidi + 1 kiwi",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g riso basmati + 120 g ceci al latte di cocco + chips di carote alla paprika",
            "spuntino_2": "Yogurt + 1 cucchiaio granola",
            "cena": "1 confezione fiocchi di latte senza lattosio + insalata mela sedano noci + patate lesse 200 g"
        },
        "VENERDI": {
            "colazione": "2 fette integrali + marmellata + 2 cucchiaini burro arachidi",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g cous cous con 150 g gamberetti + piselli",
            "spuntino_2": "1 quadrato cioccolato fondente + 3 noci",
            "cena": "1 confezione fiocchi di latte senza lattosio + insalata mela sedano noci + patate lesse 200 g"
        },
        "SABATO": {
            "colazione": "1/3 di tortino fatto in casa",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g pasta di piselli con funghi e panna vegetale o latte di cocco",
            "spuntino_2": "1 frutto + 1 manciata frutta secca",
            "cena": "PASTO LIBERO (con moderazione)"
        },
        "DOMENICA": {
            "colazione": "1/3 di tortino fatto in casa",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "120 g gnocchi + pomodorini saltati con 70 g feta SL + 1 cucchiaio pesto",
            "spuntino_2": "1 frutto + 1 pezzo cioccolato",
            "cena": "150 g pollo infarinato al limone e curry + piselli e carote saltati al rosmarino"
        }
    },
    "SETTIMANA_2": {
        "LUNEDI": {
            "colazione": "1 yogurt intero greco + cereali all bran prebiotic + 2 cucchiaini semi di lino tritati",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "1 piadina integrale + 80 g salmone affumicato e crema di 1/2 avocado e insalata",
            "spuntino_2": "1 ricotta + cacao + stevia + cocco in scaglie",
            "cena": "Tofu 100 g strapazzato con piselli e carote al curry + 2 crostini"
        },
        "MARTEDI": {
            "colazione": "Pane integrale 1 fetta + 2 cucchiaini burro arachidi + 2 cucchiaini marmellata",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "Insalata di fagiolini + 1/2 avocado + cipollotto e 2 uova sode + pane di segale 50-70 g",
            "spuntino_2": "Yogurt + 1 cucchiaio granola",
            "cena": "Brazino/orata + insalata di 1/2 avocado e rucola + 150 g patate barbabietola con aceto + 2 crostini"
        },
        "MERCOLEDI": {
            "colazione": "1 yogurt intero greco + cereali all bran prebiotic + 2 cucchiaini semi di lino tritati",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "1 fresella integrale + pomodori e basilico + 150 g fagioli cannellini",
            "spuntino_2": "3-4 noci pecan + 1 banana",
            "cena": "Piselli in umido + 120 g + lievito alimentare + insalata barbabietola con aceto + 2 crostini"
        },
        "GIOVEDI": {
            "colazione": "Porridge overnight con kiwi velo di yogurt e gocce di cioccolato",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g cous cous con 120 g lenticchie e melanzane al curry",
            "spuntino_2": "Yogurt + 1 cucchiaio granola",
            "cena": "100 g primosale o mozzarella senza lattosio + insalata con pomodori e mais + 2 crostini"
        },
        "VENERDI": {
            "colazione": "Pane segale 50 g + 50 g hummus + pomodorini",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g riso basmati con 2 uova strapazzate e piselli",
            "spuntino_2": "1 quadrato cioccolato fondente + 3 noci",
            "cena": "Trancio di trota salmonata + asparagi + 2 crostini integrali"
        },
        "SABATO": {
            "colazione": "Pane tostato 50 g + 50 g salmone affumicato + 1/2 avocado",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "150 g pollo al curry + funghi, carote, cipolla con olio di cocco",
            "spuntino_2": "1 frutto + 1 manciata frutta secca",
            "cena": "PASTO LIBERO (con moderazione)"
        },
        "DOMENICA": {
            "colazione": "1/3 di tortino fatto in casa",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g riso con asparagi e parmigiano",
            "spuntino_2": "1 frutto + 1 pezzo cioccolato",
            "cena": "Burger vegetale + insalata finocchi arancia + 3 noci tostate"
        }
    },
    "SETTIMANA_3": {
        "LUNEDI": {
            "colazione": "1/3 di tortino fatto in casa",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g pasta + 150 g pesce spada + pomodorini",
            "spuntino_2": "1 ricotta + cacao + stevia + cocco in scaglie",
            "cena": "Insalata 50-60 g feta SL cipolla cetrioli pomodori + 2 crostini"
        },
        "MARTEDI": {
            "colazione": "Pane segale 50 g + 50 g hummus + pomodorini",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g riso con 120 g piselli zucchine curcuma lievito alimentare",
            "spuntino_2": "Yogurt + 1 cucchiaio granola",
            "cena": "Insalata fagiolini + pomodori + 2 uova + 2 crostini"
        },
        "MERCOLEDI": {
            "colazione": "Torretta di 4 fette biscottate con strati di yogurt e marmellata + 3 cucchiaini",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g pasta con 50 g feta SL e broccoli",
            "spuntino_2": "3-4 noci pecan + 1 banana",
            "cena": "70 g pasta di lenticchie con pomodoro e parmigiano + insalata di finocchi + 2 crostini"
        },
        "GIOVEDI": {
            "colazione": "Pane tostato 50 g + 1 uovo strapazzato + 1/2 avocado",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g riso basmati + 120 g pollo + zucchine zafferano",
            "spuntino_2": "Yogurt + 1 cucchiaio granola",
            "cena": "150 g pollo con funghi + pane segale 30 g"
        },
        "VENERDI": {
            "colazione": "1 bicchiere di kefir + muesli + semi di lino/chia",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "120 g gnocchi zucchine + 100 g caprino senza lattosio zafferano",
            "spuntino_2": "1 quadrato cioccolato fondente + 3 noci",
            "cena": "Frittata con 2 uova con porri + spinaci + 30 g pane segale"
        },
        "SABATO": {
            "colazione": "Porridge con 1/2 banana cannella e 1 quadrato cacao",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "Insalata verdure miste con 70 g salmone + 1/2 avocado rucola + 2 crostini",
            "spuntino_2": "1 frutto + 1 manciata frutta secca",
            "cena": "PASTO LIBERO (con moderazione)"
        },
        "DOMENICA": {
            "colazione": "1/3 di tortino fatto in casa",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g spaghetti tipo di riso con 150 g gamberi + carote zucchine",
            "spuntino_2": "1 frutto + 1 pezzo cioccolato",
            "cena": "Tempeh grigliato 70-80 g con paprika in insalata con pomodorini + salsa yogurt + 2 crostini"
        }
    },
    "SETTIMANA_4": {
        "LUNEDI": {
            "colazione": "Yogurt greco SL + 1 manciata frutta secca + 2 cucchiai granola + uva a pezzetti",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "Pane segale tostato 50-60 g + 1/2 avocado + 70-80 g salmone affumicato + insalata finocchi e arance",
            "spuntino_2": "1 ricotta + cacao + stevia + cocco in scaglie",
            "cena": "Insalata cavolo carote yogurt senape limone + 2 uova + 2 crostini"
        },
        "MARTEDI": {
            "colazione": "Overnight porridge con mela cannella + 1 cucchiaino crema di mandorle",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "Insalata 150 g ceci pomodorini 1/2 avocado + 1 bocconcino integrale",
            "spuntino_2": "Yogurt + 1 frutto",
            "cena": "Coniglio 120 g con olive + carciofi in padella o radicchio con aceto balsamico + 2 wasa"
        },
        "MERCOLEDI": {
            "colazione": "50 g pane segale + marmellata e burro arachidi",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g riso nero + 150 g gamberetti zucchine",
            "spuntino_2": "3-4 noci pecan + 1 banana",
            "cena": "Burger vegetale + insalata finocchi arance uvetta + 2 crostini"
        },
        "GIOVEDI": {
            "colazione": "Overnight porridge 30 g fiocchi di avena + mirtilli + cocco grattugiato",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g riso basmati al curry con 120 g ceci zucchine carote",
            "spuntino_2": "Yogurt + 1 cucchiaio granola",
            "cena": "Farinata di ceci in padella + finocchi in insalata + carote + 2 wasa"
        },
        "VENERDI": {
            "colazione": "3 fette integrali + philadelphia e marmellata",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "1 piadina piccola mais + 150 g falafel insalata pomodori + salsa yogurt",
            "spuntino_2": "1 quadrato cioccolato fondente + 3 noci",
            "cena": "100 g tofu con cipolle caramellate + carote zucchine + 2 crostini"
        },
        "SABATO": {
            "colazione": "1 toast integrale + 2 fette prosciutto e formaggio",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "Bruschette di pane di segale 50 g + 100 g hummus + insalata barbabietola",
            "spuntino_2": "1 frutto + 1 manciata frutta secca",
            "cena": "PASTO LIBERO (con moderazione)"
        },
        "DOMENICA": {
            "colazione": "1 fetta pane integrale + 1 uovo + 1/2 avocado + 1 spremuta",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "200 g pesce al forno + insalata mista + 200 g patate",
            "spuntino_2": "1 frutto + 1 pezzo cioccolato",
            "cena": "Fiocchi di latte senza lattosio in insalata + pomodorini + 150 g confezione + 2 crostini"
        }
    }
}

with open('menu_settimanale.json', 'w', encoding='utf-8') as f:
    json.dump(menu, f, ensure_ascii=False, indent=2)

print("Completo! PRIMAVERA aggiornato nel JSON con tutte le 4 settimane!")
