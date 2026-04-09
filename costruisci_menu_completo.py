import json

# Menu completo estratto manualmente dalle immagini
menu_data = {
    "stagioni": {
        "Estate": {
            "settimana_1": {
                "lunedi": {
                    "colazione": "50 g pane di segale tostato + 1 quadrato cioccolato + 1 yogurt di soia + 1 kiwi",
                    "spuntino": "10 mandorle o 4 noci o 2 cubetti parmigiano Oppure 1 parchetto crackers di legumi o protein G",
                    "pranzo": "Farro con ceci e pomodorini + 2 cucchiai pesto",
                    "spuntino_pomeridiano": "1 parchetto crackers di legumi",
                    "cena": "Asparagi + 2 uova con scaglie grana e nocciole tostate + 1 wasa fibre",
                    "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto"
                },
                "martedi": {
                    "colazione": "50 g pane segale tostato + 2 fette bresaola + velo philadelphia",
                    "spuntino": "10 mandorle o 4 noci o 2 cubetti parmigiano Oppure 1 parchetto crackers di legumi o protein G",
                    "pranzo": "Riso nero con fagiolini e piselli + frittata",
                    "spuntino_pomeridiano": "1 barretta low sugar equilibra",
                    "cena": "Merluzzo con pomodorini e olive + wasa fibre + spinaci",
                    "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto"
                },
                "mercoledi": {
                    "colazione": "1 toast con pane integrale e prosciutto",
                    "spuntino": "10 mandorle o 4 noci o 2 cubetti parmigiano Oppure 1 parchetto crackers di legumi o protein G",
                    "pranzo": "2 patate in insalata con fagiolini e pesto + tonno",
                    "spuntino_pomeridiano": "Ricotta cacao + stevia + mandorle",
                    "cena": "Insalata di pollo e finocchio ½ arancia e mandorle + wasa fibre",
                    "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto"
                },
                "giovedi": {
                    "colazione": "Porridge con mirtilli e cacao",
                    "spuntino": "10 mandorle o 4 noci o 2 cubetti parmigiano Oppure 1 parchetto crackers di legumi o protein G",
                    "pranzo": "Riso nero con salmone affumicato + zucchine e rucola",
                    "spuntino_pomeridiano": "3 wasa + 10 mandorle",
                    "cena": "Insalata di farro ceci ½ avocado",
                    "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto"
                },
                "venerdi": {
                    "colazione": "1 yogurt di soia + muesli + semi di lino/chia",
                    "spuntino": "10 mandorle o 4 noci o 2 cubetti parmigiano Oppure 1 parchetto crackers di legumi o protein G",
                    "pranzo": "Pasta integrale al dente con zucchine e feta",
                    "spuntino_pomeridiano": "1 quadrato cioccolato fondente + 10 mandorle",
                    "cena": "Riso basmati + trancio di salmone gratinata + zucchine grigliate",
                    "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto"
                },
                "sabato": {
                    "colazione": "1 bicchiere di kefir + muesli + semi di lino/chia",
                    "spuntino": "10 mandorle o 4 noci o 2 cubetti parmigiano Oppure 1 parchetto crackers di legumi o protein G",
                    "pranzo": "Calamari e piselli al pomodoro + crostini di pane integrale",
                    "spuntino_pomeridiano": "3 gallette + crema di nocciole tostate",
                    "cena": "PASTO LIBERO (con moderazione)",
                    "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto"
                },
                "domenica": {
                    "colazione": "Pancake con farina di avena e albume + 1 quadrato cioccolato fondente fuso",
                    "spuntino": "-",
                    "pranzo": "Riso basmati integrale con gamberi e zucchine",
                    "spuntino_pomeridiano": "1 yogurt + 1 frutto + 1 quadrato cioccolato",
                    "cena": "Farinata di ceci al forno + asparagi + wasa",
                    "dopo_cena": "1 quadrato cioccolato 80% o 3 cucchiaini budino proteico al cioccolato o 1 yogurt con cacao amaro o 1 frutto"
                }
            }
        }
    }
}

# Salvo il JSON completo
with open('menu_settimanale.json', 'w', encoding='utf-8') as f:
    json.dump(menu_data, f, ensure_ascii=False, indent=2)

print("Menu JSON creato con successo!")
