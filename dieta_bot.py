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
