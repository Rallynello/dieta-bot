#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

# Carico il file JSON esistente
with open('menu_settimanale.json', 'r', encoding='utf-8') as f:
    menu = json.load(f)

# Aggiungo la sezione PRIMAVERA con dati estratti dal PDF
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
            "pranzo": "60 g riso basmati + 120 g ceci al latte di cocco + chips di carote alla paprika",
            "spuntino_2": "3-4 noci pecan + 1 banana",
            "cena": "Insalata con rucola + 2 mozzarelline + 100 g melone con aceto balsamico + 30 g pane segale + patate lesse 200 g"
        },
        "GIOVEDI": {
            "colazione": "Yogurt greco SL + 1 manciata frutta secca + 2 cucchiai granola + 1 kiwi",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g cous cous con 150 g gamberetti + piselli",
            "spuntino_2": "Yogurt + 1 cucchiaio granola",
            "cena": "1 confezione fiocchi di latte senza lattosio + insalata mela sedano noci"
        },
        "VENERDI": {
            "colazione": "2 fette integrali + marmellata + 2 cucchiaini burro arachidi",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g cous cous con 150 g gamberetti + piselli",
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
            "pranzo": "120 g gnocchi + pomodorini saltati con 70 g feta SL + 1 cucchiaio pesto",
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
            "colazione": "1 yogurt intero greco + cereali all bran prebiotic + 2 cucchiaini semi di lino tritati",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "Insalata di fagiolini + avocado + cipollotto e basilico + 2 uova sode + pane di segale 50-70 g + insalata",
            "spuntino_2": "Yogurt + 1 cucchiaio granola",
            "cena": "Insalata di avocado e rucola + 150 g patate barbabietola con aceto + 2 crostini"
        },
        "MERCOLEDI": {
            "colazione": "Pane integrale 1 fetta + 2 cucchiaini burro arachidi + 2 cucchiaini marmellata",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "1 fresella integrale + pomodori e basilico + insalata + 100 g primosale o mozzarella senza lattosio",
            "spuntino_2": "3-4 noci pecan + 1 banana",
            "cena": "Brazino/orata + 120 g piselli in umido + lievito alimentare + insalata con pomodori e mais + 2 crostini"
        },
        "GIOVEDI": {
            "colazione": "Porridge overnight con kiwi velo di yogurt e gocce di cioccolato",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g riso basmati con 2 uova strapazzate e insalata",
            "spuntino_2": "1 frutto + 1 pezzo cioccolato",
            "cena": "150 g pollo al curry + funghi carote cipolla asparagi + 2 crostini"
        },
        "VENERDI": {
            "colazione": "Pane segale 50 g + 50 g hummus + pomodorini",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "80 g salmone affumicato + 2 uova sode + insalata mista + 200 g patate",
            "spuntino_2": "1 frutto + 1 pezzo cioccolato",
            "cena": "Trancio di trota salmonata + asparagi + 2 crostini + finocchi arancia uvetta + 2 crostini"
        },
        "SABATO": {
            "colazione": "1/3 di tortino fatto in casa",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g cous cous + 120 g lenticchie e fagioli + melanzane al cannellini curry",
            "spuntino_2": "1 frutto + 1 manciata frutta secca",
            "cena": "Burger vegetale + insalata finocchi carote + 2 wasa + crostini"
        },
        "DOMENICA": {
            "colazione": "150 g pollo al curry + funghi carote cipolla + piselli con olio di cocco",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g riso con asparagi e parmigiano",
            "spuntino_2": "1 frutto + 1 pezzo cioccolato",
            "cena": "PASTO LIBERO (con moderazione)"
        }
    },
    "SETTIMANA_3": {
        "LUNEDI": {
            "colazione": "1/3 di tortino fatto in casa",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g pasta + 150 g pesce spada + pomodorini",
            "spuntino_2": "1 ricotta + cacao + stevia + cocco in scaglie",
            "cena": "Insalata 50-60 g feta SL + cipolla cetrioli pomodori + 2 uova + 2 crostini"
        },
        "MARTEDI": {
            "colazione": "Pane segale 50 g + 50 g hummus + pomodorini",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g riso con 120 g piselli zucchine curcuma lievito alimentare",
            "spuntino_2": "Yogurt + 1 cucchiaio granola",
            "cena": "Insalata fagiolini + pomodori + 2 uova + 2 crostini"
        },
        "MERCOLEDI": {
            "colazione": "Pane segale 50 g + 50 g hummus + pomodorini",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g pasta con 50 g feta SL e broccoli",
            "spuntino_2": "3-4 noci pecan + 1 banana",
            "cena": "70 g pasta di lenticchie con pomodoro e parmigiano + insalata di finocchi"
        },
        "GIOVEDI": {
            "colazione": "Pane tostato 50 g + 1 uovo strapazzato + avocado",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g riso basmati + 120 g pollo + zucchine zafferano",
            "spuntino_2": "Yogurt + 1 cucchiaio granola",
            "cena": "150 g pollo con funghi + pane segale 30 g"
        },
        "VENERDI": {
            "colazione": "1 bicchiere di kefir + muesli + semi di lino/chia",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "120 gnocchi zucchine + 100 g caprino senza lattosio zafferano + 2 crostini zucchine",
            "spuntino_2": "1 quadrato cioccolato fondente + 3 noci",
            "cena": "Frittata con 2 uova con porri + spinaci + 30 g pane segale"
        },
        "SABATO": {
            "colazione": "Porridge con mela banana cannella e 1 quadrato cacao",
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
            "colazione": "Overnight porridge con mela cannella + 1 cucchiaino crema di mandorle",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g riso basmati al curry con 120 g ceci + zucchine carote",
            "spuntino_2": "1 ricotta + cacao + stevia + cocco in scaglie",
            "cena": "Insalata cavolo carote yogurt senape limone + 2 uova + 2 wasa"
        },
        "MARTEDI": {
            "colazione": "Yogurt greco SL + 1 manciata frutta secca + 2 cucchiai granola + uva a pezzetti",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "Pane segale tostato 50 g + avocado pomodorini + 70-80 g salmone affumicato + insalata",
            "spuntino_2": "Yogurt + 1 frutto",
            "cena": "Coniglio 120 g con olive carciofi in padella + aceto balsamico + 2 uova + 2 crostini"
        },
        "MERCOLEDI": {
            "colazione": "1 toast integrale + philadelphia e marmellata",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "Insalata 150 g ceci avocado + 1 bocconcino pane integrale",
            "spuntino_2": "3-4 noci pecan + 1 banana",
            "cena": "Burger vegetale + insalata finocchi carote + 2 wasa"
        },
        "GIOVEDI": {
            "colazione": "1 fetta pane integrale 30 g fiocchi di avena + mirtilli + cocco grattugiato",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g riso nero mais + 150 g falafel + insalata pomodori + salsa yogurt",
            "spuntino_2": "1 quadrato cioccolato fondente + 1 frutto",
            "cena": "Farinata di ceci in padella + finocchi carote + 2 crostini"
        },
        "VENERDI": {
            "colazione": "3 fette integrali + philadelphia e uovo + avocado + 1 spremuta",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "Bruschette di pane di segale 50 g + hummus + 200 g patate insalata barbabietola",
            "spuntino_2": "1 frutto + 1 pezzo cioccolato",
            "cena": "100 g tofu con cipolle caramellate + insalata finocchi arancia + 2 crostini"
        },
        "SABATO": {
            "colazione": "1/3 di tortino fatto in casa",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "60 g riso basmati + 100 g falafel + insalata zucchine pomodori + salsa yogurt",
            "spuntino_2": "1 frutto + 1 manciata frutta secca",
            "cena": "Fiocchi di latte senza lattosio + insalata cipolle caramellate carote zucchine + 2 crostini"
        },
        "DOMENICA": {
            "colazione": "3 fette integrali + philadelphia e uovo + avocado + 1 spremuta",
            "spuntino": "1 manciata frutta secca + 2 gallette/wasa",
            "pranzo": "Pane segale tostato 50 g + avocado pomodorini + 70-80 g salmone affumicato + insalata finocchi arance",
            "spuntino_2": "1 frutto + 1 pezzo cioccolato",
            "cena": "Coniglio 120 g con olive carciofi insalata radicchio + arance uvetta + 2 crostini"
        }
    }
}

# Salvo il file aggiornato
with open('menu_settimanale.json', 'w', encoding='utf-8') as f:
    json.dump(menu, f, ensure_ascii=False, indent=2)

print("✅ PRIMAVERA aggiunta a menu_settimanale.json con 4 settimane complete!")
