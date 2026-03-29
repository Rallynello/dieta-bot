#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🥗 BOT TELEGRAM PER GESTIONE DIETA SETTIMANALE
Menu completo ESTATE + INVERNO con ricerca ingredienti
"""

import json
import logging
import random
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================
# CARICA IL MENU E LE FRASI MOTIVAZIONALI
# ============================================================

with open('menu_settimanale.json', 'r', encoding='utf-8') as f:
    MENU = json.load(f)

# Carica le frasi motivazionali
with open('frasimotivazionali.txt', 'r', encoding='utf-8') as f:
    frasi_raw = f.readlines()
    FRASI_MOTIVAZIONALI = [frase.strip() for frase in frasi_raw if frase.strip()]

GIORNI = ["LUNEDI", "MARTEDI", "MERCOLEDI", "GIOVEDI", "VENERDI", "SABATO", "DOMENICA"]
EMOJI_PASTI = {
    "colazione": "🌅",
    "spuntino_1": "☀️",
    "pranzo": "🍽️",
    "spuntino_2": "🥜",
    "cena": "🌙",
    "dopo_cena": "🍫"
}

# ============================================================
# CATEGORIZZAZIONE INGREDIENTI
# ============================================================

def estrai_e_categorizza_ingredienti():
    """Estrae tutti gli ingredienti dal menu e li categorizza"""
    ingredienti = {}
    
    # Parole chiave per categorie
    verdure_keywords = ['spinaci', 'carote', 'zucchine', 'insalata', 'pomodori', 'asparagi', 'broccoli', 
                        'cavolo', 'melanzane', 'peperoni', 'cipolla', 'aglio', 'lattuga', 'rucola', 'bietola']
    proteine_keywords = ['pollo', 'pesce', 'carne', 'uova', 'tofu', 'salmone', 'merluzzo', 'trota', 'sgombro',
                         'vitello', 'manzo', 'maiale', 'prosciutto', 'petto di pollo', 'fesa di tacchino']
    carboidrati_keywords = ['riso', 'pasta', 'pane', 'patate', 'farro', 'orzo', 'ceci', 'lenticchie', 'fagioli',
                            'grano', 'avena', 'mais', 'polenta', 'couscous']
    latticini_keywords = ['ricotta', 'yogurt', 'formaggio', 'mozzarella', 'grana', 'parmigiano', 'latte', 'burro',
                          'mascarpone', 'pecorino', 'provolone', 'scamorza']
    
    categorie = {
        '🥬 VERDURE': verdure_keywords,
        '🍗 PROTEINE': proteine_keywords,
        '🥕 CARBOIDRATI': carboidrati_keywords,
        '🧀 LATTICINI': latticini_keywords
    }
    
    # Estrai ingredienti da tutte le settimane
    tutti_ingredienti = set()
    
    for stagione_data in MENU.values():
        for settimana_data in stagione_data.values():
            for pasti_dict in settimana_data.values():
                for descrizione in pasti_dict.values():
                    if isinstance(descrizione, str):
                        # Estrai parole (split per • e spazi)
                        parole = descrizione.lower().replace('•', ' ').replace(',', ' ').split()
                        tutti_ingredienti.update(parole)
    
    # Categorizza
    ingredienti_categorizzati = {cat: [] for cat in categorie.keys()}
    
    for ingrediente in sorted(tutti_ingredienti):
        if len(ingrediente) < 2:
            continue
        
        # Pulisci l'ingrediente
        ing_clean = ingrediente.strip()
        
        # Verifica in quale categoria va
        trovato = False
        for categoria, keywords in categorie.items():
            if any(keyword in ing_clean for keyword in keywords):
                if ing_clean not in ingredienti_categorizzati[categoria]:
                    ingredienti_categorizzati[categoria].append(ing_clean)
                trovato = True
                break
        
        # Se non categorizzato, mettilo nei carboidrati (default)
        if not trovato and len(ing_clean) > 2:
            if ing_clean not in ingredienti_categorizzati['🥕 CARBOIDRATI']:
                ingredienti_categorizzati['🥕 CARBOIDRATI'].append(ing_clean)
    
    return ingredienti_categorizzati

INGREDIENTI_CATEGORIZZATI = estrai_e_categorizza_ingredienti()

# ============================================================
# COMANDI
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start - Scelta ESTATE o INVERNO"""
    frase_motivazionale = random.choice(FRASI_MOTIVAZIONALI)
    
    text = f"""
Benvenuta, 🥗 sono il tuo assistente virtuale 🤖 🍽️

{frase_motivazionale}
"""
    keyboard = [
        [InlineKeyboardButton("☀️ ESTATE", callback_data="stagione_ESTATE")],
        [InlineKeyboardButton("❄️ INVERNO", callback_data="stagione_INVERNO")],
        [InlineKeyboardButton("✨ CREA SETTIMANA", callback_data="crea_settimana_start")],
        [InlineKeyboardButton("📁 LE MIE SETTIMANE", callback_data="mie_settimane_start")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /help"""
    text = """
📋 *COMANDI DISPONIBILI:*

/start - Torna al menu principale
/help - Questo messaggio

💡 *RICERCA INGREDIENTI:*
Scrivi semplicemente l'ingrediente che cerchi, ad esempio:
- pollo
- pesce
- riso
- carote
- salmone

Il bot ti mostrerà tutte le settimane e i giorni dove appare!
"""
    await update.message.reply_text(text, parse_mode="Markdown")

async def cerca_ingrediente(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cerca un ingrediente nel menu"""
    ingrediente = update.message.text.lower().strip()
    
    if len(ingrediente) < 2:
        await update.message.reply_text("❌ Scrivi almeno 2 caratteri per cercare un ingrediente!")
        return
    
    risultati = {}
    
    # Cerca in tutte le stagioni, settimane e giorni
    for stagione_key, stagione_data in MENU.items():
        for settimana_key, settimana_data in stagione_data.items():
            for giorno, pasti_dict in settimana_data.items():
                for pasto, descrizione in pasti_dict.items():
                    if ingrediente in descrizione.lower():
                        if stagione_key not in risultati:
                            risultati[stagione_key] = {}
                        if settimana_key not in risultati[stagione_key]:
                            risultati[stagione_key][settimana_key] = {}
                        if giorno not in risultati[stagione_key][settimana_key]:
                            risultati[stagione_key][settimana_key][giorno] = []
                        risultati[stagione_key][settimana_key][giorno].append({
                            "pasto": pasto,
                            "descrizione": descrizione
                        })
    
    if not risultati:
        await update.message.reply_text(f"❌ Non ho trovato '{ingrediente}' nel menu!")
        return
    
    # Formato risposta con bottoni
    text = f"🔍 *RISULTATI PER: {ingrediente.upper()}*\n\n"
    keyboard = []
    
    for stagione_key, stagioni_data in sorted(risultati.items()):
        text += f"📅 *{stagione_key}*\n"
        
        for settimana_key, settimana_data in sorted(stagioni_data.items()):
            settimana_num = settimana_key.split("_")[1]
            text += f"  📌 Settimana {settimana_num}\n"
            
            for giorno in GIORNI:
                if giorno in settimana_data:
                    text += f"    • {giorno}\n"
                    for item in settimana_data[giorno]:
                        emoji = EMOJI_PASTI.get(item["pasto"], "🍴")
                        pasto_nome = item["pasto"].replace("_", " ").capitalize()
                        text += f"      {emoji} {pasto_nome}\n"
                    
                    # Aggiungi bottone per questo giorno
                    giorno_idx = GIORNI.index(giorno)
                    button_text = f"📆 {stagione_key} S{settimana_num} {giorno}"
                    keyboard.append([InlineKeyboardButton(button_text, callback_data=f"giorno_{stagione_key}_{settimana_num}_{giorno_idx}")])
        
        text += "\n"
    
    keyboard.append([InlineKeyboardButton("🏠 HOME", callback_data="home")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gestisce i bottoni inline"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    # Selezione stagione
    if data.startswith("stagione_"):
        stagione = data.split("_")[1]
        await mostra_settimane(query, stagione)
    
    # Selezione settimana
    elif data.startswith("settimana_"):
        parts = data.split("_")
        stagione = parts[1]
        settimana = parts[2]
        await mostra_giorni_settimana(query, stagione, f"SETTIMANA_{settimana}")
    
    # Selezione giorno
    elif data.startswith("giorno_"):
        parts = data.split("_")
        stagione = parts[1]
        settimana = parts[2]
        giorno_idx = int(parts[3])
        await mostra_menu_giorno(query, stagione, f"SETTIMANA_{settimana}", giorno_idx)
    
    # Torna a inizio
    elif data == "home":
        await mostra_menu_principale(query)
    
    # Torna alle settimane
    elif data.startswith("back_settimane_"):
        stagione = data.split("_")[2]
        await mostra_settimane(query, stagione)
    
    # Torna ai giorni
    elif data.startswith("back_giorni_"):
        parts = data.split("_")
        stagione = parts[2]
        settimana = parts[3]
        await mostra_giorni_settimana(query, stagione, f"SETTIMANA_{settimana}")
    
    # CREA SETTIMANA PERSONALIZZATA
    elif data == "crea_settimana_start":
        await mostra_categorie_crea_settimana(query, update.effective_user.id)
    
    # LE MIE SETTIMANE
    elif data == "mie_settimane_start":
        await mostra_mie_settimane(query, update.effective_user.id)
    
    # Selezione categoria per creare settimana
    elif data.startswith("seleziona_cat_"):
        categoria = data.replace("seleziona_cat_", "")
        await mostra_ingredienti_categoria(query, categoria, update.effective_user.id, context)
    
    # Toggle ingrediente
    elif data.startswith("toggle_ing_"):
        parts = data.split("_", 2)
        categoria = parts[2].rsplit("_", 1)[0]
        ingrediente = parts[2].rsplit("_", 1)[1]
        await toggle_ingrediente(query, categoria, ingrediente, update.effective_user.id, context)
    
    # Continua con prossima categoria
    elif data.startswith("continua_categoria_"):
        categoria = data.replace("continua_categoria_", "")
        await mostra_prossima_categoria(query, categoria, update.effective_user.id, context)
    
    # Crea settimana
    elif data == "crea_settimana_finale":
        await genera_e_salva_settimana(query, update.effective_user.id, context)

async def mostra_menu_principale(query):
    """Mostra il menu principale"""
    frase_motivazionale = random.choice(FRASI_MOTIVAZIONALI)
    
    text = f"""
Benvenuta, 🥗 sono il tuo assistente virtuale 🤖 🍽️

{frase_motivazionale}
"""
    keyboard = [
        [InlineKeyboardButton("☀️ ESTATE", callback_data="stagione_ESTATE")],
        [InlineKeyboardButton("❄️ INVERNO", callback_data="stagione_INVERNO")],
        [InlineKeyboardButton("✨ CREA SETTIMANA", callback_data="crea_settimana_start")],
        [InlineKeyboardButton("📁 LE MIE SETTIMANE", callback_data="mie_settimane_start")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def mostra_settimane(query, stagione):
    """Mostra le settimane della stagione scelta"""
    stagione_data = MENU[stagione]
    num_settimane = len(stagione_data)
    
    text = f"*{stagione}*\n\nScegli una settimana:\n"
    
    keyboard = []
    for i in range(1, num_settimane + 1):
        keyboard.append([InlineKeyboardButton(f"📅 Settimana {i}", callback_data=f"settimana_{stagione}_{i}")])
    
    keyboard.append([InlineKeyboardButton("🏠 HOME", callback_data="home")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def mostra_giorni_settimana(query, stagione, settimana):
    """Mostra i giorni della settimana"""
    text = f"*{stagione} - {settimana.replace('_', ' ')}*\n\nScegli un giorno:\n"
    
    keyboard = []
    for idx, giorno in enumerate(GIORNI):
        settimana_num = settimana.split("_")[1]
        keyboard.append([InlineKeyboardButton(f"📆 {giorno}", callback_data=f"giorno_{stagione}_{settimana_num}_{idx}")])
    
    keyboard.append([InlineKeyboardButton("⬅️ Indietro", callback_data=f"back_settimane_{stagione}")])
    keyboard.append([InlineKeyboardButton("🏠 HOME", callback_data="home")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def mostra_menu_giorno(query, stagione, settimana, giorno_idx):
    """Mostra il menu di un giorno specifico"""
    giorno = GIORNI[giorno_idx]
    menu_giorno = MENU[stagione][settimana][giorno]
    
    text = f"*{stagione} - {settimana.replace('_', ' ')} - {giorno}*\n\n"
    
    # Ordine corretto dei pasti
    ordine_pasti = ["colazione", "spuntino_1", "pranzo", "spuntino_2", "cena", "dopo_cena"]
    
    for pasto in ordine_pasti:
        if pasto in menu_giorno:
            emoji = EMOJI_PASTI.get(pasto, "🍴")
            piatto = menu_giorno.get(pasto, "N/A")
            pasto_nome = pasto.upper().replace("_", " ")
            text += f"{emoji} *{pasto_nome}*\n{piatto}\n\n"
    
    settimana_num = settimana.split("_")[1]
    keyboard = [
        [InlineKeyboardButton("⬅️ Giorno Precedente" if giorno_idx > 0 else "⬅️", 
                             callback_data=f"giorno_{stagione}_{settimana_num}_{giorno_idx - 1}" if giorno_idx > 0 else "skip"),
         InlineKeyboardButton("Giorno Successivo ➡️" if giorno_idx < len(GIORNI) - 1 else "➡️",
                             callback_data=f"giorno_{stagione}_{settimana_num}_{giorno_idx + 1}" if giorno_idx < len(GIORNI) - 1 else "skip")],
        [InlineKeyboardButton("⬅️ Giorni", callback_data=f"back_giorni_{stagione}_{settimana_num}")],
        [InlineKeyboardButton("🏠 HOME", callback_data="home")],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

# ============================================================
# CREA SETTIMANA PERSONALIZZATA
# ============================================================

async def mostra_categorie_crea_settimana(query, user_id):
    """Mostra le categorie per creare una settimana personalizzata"""
    text = """
✨ *CREA SETTIMANA PERSONALIZZATA*

Scegli una categoria per selezionare gli ingredienti:
"""
    
    keyboard = []
    for categoria in INGREDIENTI_CATEGORIZZATI.keys():
        keyboard.append([InlineKeyboardButton(categoria, callback_data=f"seleziona_cat_{categoria}")])
    
    keyboard.append([InlineKeyboardButton("🏠 HOME", callback_data="home")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

# ============================================================
# GENERAZIONE SETTIMANA PERSONALIZZATA
# ============================================================

def trova_giorni_con_ingrediente(ingrediente):
    """Trova tutti i giorni che contengono un ingrediente"""
    giorni_trovati = []
    
    for stagione_key, stagione_data in MENU.items():
        for settimana_key, settimana_data in stagione_data.items():
            for giorno, pasti_dict in settimana_data.items():
                for pasto, descrizione in pasti_dict.items():
                    if isinstance(descrizione, str) and ingrediente.lower() in descrizione.lower():
                        giorni_trovati.append({
                            'stagione': stagione_key,
                            'settimana': settimana_key,
                            'giorno': giorno,
                            'menu': pasti_dict
                        })
                        break
    
    return giorni_trovati

def genera_settimana_personalizzata(ingredienti_richiesti):
    """Genera una settimana cercando di matchare gli ingredienti richiesti"""
    settimana_generata = {}
    ingredienti_usati = set()
    giorni_usati = set()
    
    # STEP 1: Trova giorni che matchano gli ingredienti
    for ingrediente in ingredienti_richiesti:
        giorni_disponibili = trova_giorni_con_ingrediente(ingrediente)
        
        # Filtra i giorni già usati
        giorni_disponibili = [g for g in giorni_disponibili if (g['stagione'], g['settimana'], g['giorno']) not in giorni_usati]
        
        if giorni_disponibili:
            # Scegli un giorno casuale
            giorno_scelto = random.choice(giorni_disponibili)
            key = (giorno_scelto['stagione'], giorno_scelto['settimana'], giorno_scelto['giorno'])
            
            if len(settimana_generata) < 7:  # Max 7 giorni
                settimana_generata[len(settimana_generata)] = giorno_scelto
                giorni_usati.add(key)
                ingredienti_usati.add(ingrediente)
    
    # STEP 2: Riempi i giorni rimanenti con giorni casuali
    while len(settimana_generata) < 7:
        stagione_random = random.choice(list(MENU.keys()))
        settimana_random_key = random.choice(list(MENU[stagione_random].keys()))
        giorno_random = random.choice(GIORNI)
        
        key = (stagione_random, settimana_random_key, giorno_random)
        if key not in giorni_usati:
            menu_giorno = MENU[stagione_random][settimana_random_key].get(giorno_random, {})
            if menu_giorno:
                settimana_generata[len(settimana_generata)] = {
                    'stagione': stagione_random,
                    'settimana': settimana_random_key,
                    'giorno': giorno_random,
                    'menu': menu_giorno
                }
                giorni_usati.add(key)
    
    return settimana_generata, ingredienti_usati

def genera_settimana_personalizzata(ingredienti_richiesti):
    """Genera una settimana cercando di matchare gli ingredienti richiesti"""
    settimana_generata = {}
    ingredienti_usati = set()
    giorni_usati = set()
    
    # STEP 1: Trova giorni che matchano gli ingredienti
    for ingrediente in ingredienti_richiesti:
        giorni_disponibili = trova_giorni_con_ingrediente(ingrediente)
        
        # Filtra i giorni già usati
        giorni_disponibili = [g for g in giorni_disponibili if (g['stagione'], g['settimana'], g['giorno']) not in giorni_usati]
        
        if giorni_disponibili:
            # Scegli un giorno casuale
            giorno_scelto = random.choice(giorni_disponibili)
            key = (giorno_scelto['stagione'], giorno_scelto['settimana'], giorno_scelto['giorno'])
            
            if len(settimana_generata) < 7:  # Max 7 giorni
                settimana_generata[len(settimana_generata)] = giorno_scelto
                giorni_usati.add(key)
                ingredienti_usati.add(ingrediente)
    
    # STEP 2: Riempi i giorni rimanenti con giorni casuali
    while len(settimana_generata) < 7:
        stagione_random = random.choice(list(MENU.keys()))
        settimana_random_key = random.choice(list(MENU[stagione_random].keys()))
        giorno_random = random.choice(GIORNI)
        
        key = (stagione_random, settimana_random_key, giorno_random)
        if key not in giorni_usati:
            menu_giorno = MENU[stagione_random][settimana_random_key].get(giorno_random, {})
            if menu_giorno:
                settimana_generata[len(settimana_generata)] = {
                    'stagione': stagione_random,
                    'settimana': settimana_random_key,
                    'giorno': giorno_random,
                    'menu': menu_giorno
                }
                giorni_usati.add(key)
    
    return settimana_generata, ingredienti_usati

async def toggle_ingrediente(query, categoria, ingrediente, user_id, context):
    """Toggle un ingrediente (aggiunge/rimuove dalla selezione)"""
    if 'ingredienti_selezionati' not in context.user_data:
        context.user_data['ingredienti_selezionati'] = {}
    
    if categoria not in context.user_data['ingredienti_selezionati']:
        context.user_data['ingredienti_selezionati'][categoria] = set()
    
    if ingrediente in context.user_data['ingredienti_selezionati'][categoria]:
        context.user_data['ingredienti_selezionati'][categoria].remove(ingrediente)
    else:
        context.user_data['ingredienti_selezionati'][categoria].add(ingrediente)
    
    # Rimostri la categoria con gli aggiornamenti
    await mostra_ingredienti_categoria(query, categoria, user_id, context)

async def mostra_prossima_categoria(query, categoria_corrente, user_id, context):
    """Mostra la prossima categoria o il sommario"""
    categorie_list = list(INGREDIENTI_CATEGORIZZATI.keys())
    idx_corrente = categorie_list.index(categoria_corrente)
    
    if idx_corrente < len(categorie_list) - 1:
        # Vai alla prossima categoria
        prossima_categoria = categorie_list[idx_corrente + 1]
        await mostra_ingredienti_categoria(query, prossima_categoria, user_id, context)
    else:
        # Fine selezione - mostra sommario e bottone CREA
        await mostra_sommario_e_crea(query, user_id, context)

async def mostra_sommario_e_crea(query, user_id, context):
    """Mostra il sommario degli ingredienti selezionati e bottone CREA"""
    text = "✨ *SOMMARIO INGREDIENTI SELEZIONATI*\n\n"
    
    totale_ingredienti = 0
    for categoria, ingredienti in context.user_data.get('ingredienti_selezionati', {}).items():
        if ingredienti:
            text += f"{categoria}\n"
            for ing in ingredienti:
                text += f"  ☑️ {ing}\n"
            totale_ingredienti += len(ingredienti)
    
    if totale_ingredienti == 0:
        text += "❌ Nessun ingrediente selezionato!\n\nSeleziona almeno un ingrediente per creare la settimana."
    else:
        text += f"\n*Totale: {totale_ingredienti} ingredienti selezionati*\n\nClicca CREA SETTIMANA per generarla!"
    
    keyboard = []
    if totale_ingredienti > 0:
        keyboard.append([InlineKeyboardButton("🎯 CREA SETTIMANA", callback_data="crea_settimana_finale")])
    keyboard.append([InlineKeyboardButton("⬅️ Modifica", callback_data="crea_settimana_start")])
    keyboard.append([InlineKeyboardButton("🏠 HOME", callback_data="home")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def genera_e_salva_settimana(query, user_id, context):
    """Genera la settimana e chiede il nome per salvarla"""
    # Raccogli tutti gli ingredienti selezionati
    ingredienti_richiesti = []
    for categoria, ingredienti in context.user_data.get('ingredienti_selezionati', {}).items():
        ingredienti_richiesti.extend(list(ingredienti))
    
    if not ingredienti_richiesti:
        await query.edit_message_text("❌ Nessun ingrediente selezionato!")
        return
    
    # Genera la settimana
    settimana, ingredienti_usati = genera_settimana_personalizzata(ingredienti_richiesti)
    
    # Salva in context per uso successivo
    context.user_data['settimana_generata'] = settimana
    
    # Mostra la settimana generata
    text = "🎉 *SETTIMANA GENERATA!*\n\n"
    for idx, giorno_data in settimana.items():
        giorno_num = idx + 1
        text += f"*Giorno {giorno_num}: {giorno_data['giorno']}*\n"
        text += f"({giorno_data['stagione']} - {giorno_data['settimana']})\n\n"
    
    keyboard = [
        [InlineKeyboardButton("💾 SALVA SETTIMANA", callback_data="salva_settimana_nome")],
        [InlineKeyboardButton("🏠 HOME", callback_data="home")],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def mostra_mie_settimane(query, user_id):
    """Mostra le settimane salvate dall'utente"""
    text = """
📁 *LE MIE SETTIMANE*

Funzionalità in fase di sviluppo.
Presto potrai visualizzare, salvare e eliminare le tue settimane personalizzate!
"""
    
    keyboard = [
        [InlineKeyboardButton("🏠 HOME", callback_data="home")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

# ============================================================
# MAIN
# ============================================================

def main():
    """Avvia il bot"""
    TOKEN = os.getenv("TOKEN")
    
    if not TOKEN:
        print("❌ ERRORE: Variabile TOKEN non trovata!")
        return
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, cerca_ingrediente))
    
    print("🚀 Bot avviato! Premi Ctrl+C per fermare.")
    app.run_polling()

if __name__ == "__main__":
    main()
