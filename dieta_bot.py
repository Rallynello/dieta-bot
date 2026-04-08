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
from pathlib import Path
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================
# OTTIENI IL PERCORSO DELLO SCRIPT
# ============================================================
SCRIPT_DIR = Path(__file__).parent
MENU_FILE = SCRIPT_DIR / 'menu_settimanale.json'
INGREDIENTI_FILE = SCRIPT_DIR / 'ingredienti_definitivi.json'
FRASI_FILE = SCRIPT_DIR / 'frasimotivazionali.txt'

print(f"📂 Script directory: {SCRIPT_DIR}")
print(f"📄 Menu file: {MENU_FILE} (esiste: {MENU_FILE.exists()})")
print(f"🥗 Ingredienti file: {INGREDIENTI_FILE} (esiste: {INGREDIENTI_FILE.exists()})")

# ============================================================
# CARICA IL MENU E LE FRASI MOTIVAZIONALI
# ============================================================

with open(MENU_FILE, 'r', encoding='utf-8') as f:
    MENU = json.load(f)

# Carica le frasi motivazionali
with open(FRASI_FILE, 'r', encoding='utf-8') as f:
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
    """Carica gli ingredienti dal file pulito"""
    try:
        with open(INGREDIENTI_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"✅ Ingredienti caricati da {INGREDIENTI_FILE}")
            return data
    except FileNotFoundError:
        print(f"❌ File {INGREDIENTI_FILE} non trovato! Usando fallback.")
        return {
            '🥬 VERDURE': ['Carote', 'Spinaci', 'Broccoli', 'Zucchine', 'Pomodori'],
            '🍗 PROTEINE': ['Pollo', 'Pesce', 'Uova', 'Carne', 'Tacchino'],
            '🥕 CARBOIDRATI': ['Riso', 'Pasta', 'Pane', 'Patate', 'Farro'],
            '🧀 LATTICINI': ['Yogurt', 'Ricotta', 'Formaggio', 'Mozzarella', 'Latte']
        }
    except json.JSONDecodeError as e:
        print(f"❌ Errore JSON in {INGREDIENTI_FILE}: {e}")
        return {
            '🥬 VERDURE': ['Carote', 'Spinaci', 'Broccoli', 'Zucchine', 'Pomodori'],
            '🍗 PROTEINE': ['Pollo', 'Pesce', 'Uova', 'Carne', 'Tacchino'],
            '🥕 CARBOIDRATI': ['Riso', 'Pasta', 'Pane', 'Patate', 'Farro'],
            '🧀 LATTICINI': ['Yogurt', 'Ricotta', 'Formaggio', 'Mozzarella', 'Latte']
        }

INGREDIENTI_CATEGORIZZATI = estrai_e_categorizza_ingredienti()

# ============================================================
# COMANDI
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start - Scelta ESTATE, PRIMAVERA o INVERNO"""
    frase_motivazionale = random.choice(FRASI_MOTIVAZIONALI)
    
    text = f"""
Benvenuta, 🥗 sono il tuo assistente virtuale 🤖 🍽️

{frase_motivazionale}
"""
    keyboard = [
        [InlineKeyboardButton("☀️ ESTATE", callback_data="stagione_ESTATE")],
        [InlineKeyboardButton("🌱 PRIMAVERA", callback_data="stagione_PRIMAVERA")],
        [InlineKeyboardButton("❄️ INVERNO", callback_data="stagione_INVERNO")],
        [InlineKeyboardButton("🔍 RICERCA INGREDIENTE", callback_data="ricerca_ingrediente_start")],
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
    
    # Salva i risultati per uso futuro
    context.user_data['ingrediente_cercato'] = ingrediente
    context.user_data['risultati_ingrediente'] = risultati
    
    # Formato risposta con testo riepilogativo
    text = f"🔍 *RISULTATI PER: {ingrediente.upper()}*\n\n"
    
    # Crea riepilogo per stagione
    for stagione_key in sorted(risultati.keys()):
        stagione_data = risultati[stagione_key]
        num_settimane = len(stagione_data)
        giorni_totali = sum(len(giorni) for settimana in stagione_data.values() for giorni in [settimana])
        text += f"📅 *{stagione_key}*: {num_settimane} settimane\n"
    
    text += "\n_Clicca su una stagione per vedere i dettagli_"
    
    # Bottoni per le stagioni
    keyboard = []
    for stagione_key in sorted(risultati.keys()):
        keyboard.append([InlineKeyboardButton(f"📅 {stagione_key}", callback_data=f"ingrediente_stagione_{stagione_key}")])
    
    keyboard.append([InlineKeyboardButton("🏠 HOME", callback_data="home")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def mostra_ingrediente_per_stagione(query, context, stagione):
    """Mostra i giorni di una stagione che contengono l'ingrediente cercato"""
    ingrediente = context.user_data.get('ingrediente_cercato')
    risultati = context.user_data.get('risultati_ingrediente', {})
    
    if stagione not in risultati:
        await query.edit_message_text("❌ Stagione non trovata!")
        return
    
    stagione_data = risultati[stagione]
    text = f"🔍 *{ingrediente.upper()}* in *{stagione}*\n\n"
    keyboard = []
    
    for settimana_key in sorted(stagione_data.keys()):
        settimana_num = settimana_key.split("_")[1]
        text += f"📌 *Settimana {settimana_num}*\n"
        
        for giorno in GIORNI:
            if giorno in stagione_data[settimana_key]:
                text += f"  • *{giorno}*\n"
                for item in stagione_data[settimana_key][giorno]:
                    emoji = EMOJI_PASTI.get(item["pasto"], "🍴")
                    pasto_nome = item["pasto"].replace("_", " ").capitalize()
                    text += f"    {emoji} {pasto_nome}\n"
                
                # Bottone per il giorno (con callback per ricerca ingrediente)
                giorno_idx = GIORNI.index(giorno)
                button_text = f"📆 S{settimana_num} {giorno}"
                keyboard.append([InlineKeyboardButton(button_text, callback_data=f"ingrediente_giorno_{stagione}_{settimana_num}_{giorno_idx}")])
        
        text += "\n"
    
    keyboard.append([InlineKeyboardButton("⬅️ Indietro", callback_data="ingrediente_indietro")])
    keyboard.append([InlineKeyboardButton("🏠 HOME", callback_data="home")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

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
    
    # Ricerca ingrediente
    elif data == "ricerca_ingrediente_start":
        await query.edit_message_text("🔍 Scrivi l'ingrediente che cerchi (es. salmone, riso, pollo...)")
    
    # Visualizza ingrediente per stagione
    elif data.startswith("ingrediente_stagione_"):
        stagione = data.replace("ingrediente_stagione_", "")
        await mostra_ingrediente_per_stagione(query, context, stagione)
    
    # Torna al riepilogo ingrediente
    elif data == "ingrediente_indietro":
        ingrediente = context.user_data.get('ingrediente_cercato')
        risultati = context.user_data.get('risultati_ingrediente', {})
        
        text = f"🔍 *RISULTATI PER: {ingrediente.upper()}*\n\n"
        for stagione_key in sorted(risultati.keys()):
            stagione_data = risultati[stagione_key]
            num_settimane = len(stagione_data)
            text += f"📅 *{stagione_key}*: {num_settimane} settimane\n"
        
        text += "\n_Clicca su una stagione per vedere i dettagli_"
        
        keyboard = []
        for stagione_key in sorted(risultati.keys()):
            keyboard.append([InlineKeyboardButton(f"📅 {stagione_key}", callback_data=f"ingrediente_stagione_{stagione_key}")])
        
        keyboard.append([InlineKeyboardButton("🏠 HOME", callback_data="home")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")
    
    # Torna alla stagione della ricerca
    elif data.startswith("ingrediente_indietro_stagione_"):
        stagione = data.replace("ingrediente_indietro_stagione_", "")
        await mostra_ingrediente_per_stagione(query, context, stagione)
    
    # Visualizza giorno da ricerca ingrediente
    elif data.startswith("ingrediente_giorno_"):
        parts = data.split("_")
        stagione = parts[2]
        settimana = parts[3]
        giorno_idx = int(parts[4])
        await mostra_menu_giorno_da_ricerca(query, context, stagione, f"SETTIMANA_{settimana}", giorno_idx)
    
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
    
    # Visualizza settimana salvata
    elif data.startswith("visualizza_settimana_"):
        nome_settimana = data.replace("visualizza_settimana_", "")
        await visualizza_settimana_salvata(query, update.effective_user.id, nome_settimana)
    
    # Elimina settimana salvata
    elif data.startswith("elimina_settimana_"):
        nome_settimana = data.replace("elimina_settimana_", "")
        await elimina_settimana_salvata(query, update.effective_user.id, nome_settimana)
    
    # Visualizza una settimana salvata
    elif data.startswith("visualizza_settimana_"):
        nome_settimana = data.replace("visualizza_settimana_", "")
        await visualizza_settimana_salvata(query, update.effective_user.id, nome_settimana)
    
    # Visualizza giorno di una settimana salvata
    elif data.startswith("visualizza_giorno_salvato_"):
        # Formato: visualizza_giorno_salvato_{nome_settimana}#{indice_giorno}
        parts = data.replace("visualizza_giorno_salvato_", "").split("#")
        if len(parts) == 2:
            nome_settimana = parts[0]
            giorno_idx = parts[1]
            await visualizza_giorno_settimana_salvata(query, update.effective_user.id, nome_settimana, giorno_idx)
    
    # Aggiungi giorno a settimana - seleziona settimana
    elif data.startswith("add_to_settimana_"):
        parts = data.replace("add_to_settimana_", "").split("_")
        stagione = parts[0]
        settimana_num = parts[1]
        giorno_idx = int(parts[2])
        await aggiungi_giorno_a_settimana_start(query, update.effective_user.id, stagione, settimana_num, giorno_idx)
    
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
    
    # Aumenta quantità ingrediente
    elif data.startswith("inc_ing_"):
        parts = data.replace("inc_ing_", "").rsplit("_", 1)
        categoria = parts[0]
        ingrediente = parts[1]
        await modifica_quantita_ingrediente(query, categoria, ingrediente, 1, update.effective_user.id, context)
    
    # Diminuisce quantità ingrediente
    elif data.startswith("dec_ing_"):
        parts = data.replace("dec_ing_", "").rsplit("_", 1)
        categoria = parts[0]
        ingrediente = parts[1]
        await modifica_quantita_ingrediente(query, categoria, ingrediente, -1, update.effective_user.id, context)
    
    # Mostra ingrediente (nessuna azione)
    elif data.startswith("show_ing_"):
        pass
    
    # Continua con prossima categoria
    elif data.startswith("continua_categoria_"):
        categoria = data.replace("continua_categoria_", "")
        await mostra_prossima_categoria(query, categoria, update.effective_user.id, context)
    
    # Crea settimana
    elif data == "crea_settimana_finale":
        await genera_e_salva_settimana(query, update.effective_user.id, context)
    
    # Salva settimana con nome
    elif data == "salva_settimana_nome":
        context.user_data['in_salvataggio'] = True
        await query.edit_message_text(
            "💾 *Inserisci il nome per la settimana:*\n\n"
            "(Scrivi il nome e invialo come messaggio)",
            parse_mode="Markdown"
        )
    
    # Seleziona settimana di destinazione per aggiungere giorno
    elif data.startswith("select_dest_week_"):
        parts = data.replace("select_dest_week_", "").split("#")
        nome_settimana = parts[0]
        giorno_parts = parts[1].split("_")
        stagione = giorno_parts[0]
        settimana_num = giorno_parts[1]
        giorno_idx = int(giorno_parts[2])
        await select_dest_week(query, context, nome_settimana, stagione, settimana_num, giorno_idx)
    
    # Aggiungi giorno allo slot scelto
    elif data.startswith("add_day_slot_"):
        parts = data.replace("add_day_slot_", "").split("#")
        nome_settimana = parts[0]
        giorno_parts = parts[1].split("_")
        stagione = giorno_parts[0]
        settimana_num = giorno_parts[1]
        giorno_idx = int(giorno_parts[2])
        slot_idx = int(parts[2])
        await add_day_to_week_slot(query, context, nome_settimana, stagione, settimana_num, giorno_idx, slot_idx)

async def mostra_menu_principale(query):
    """Mostra il menu principale"""
    frase_motivazionale = random.choice(FRASI_MOTIVAZIONALI)
    
    text = f"""
Benvenuta, 🥗 sono il tuo assistente virtuale 🤖 🍽️

{frase_motivazionale}
"""
    keyboard = [
        [InlineKeyboardButton("☀️ ESTATE", callback_data="stagione_ESTATE")],
        [InlineKeyboardButton("🌱 PRIMAVERA", callback_data="stagione_PRIMAVERA")],
        [InlineKeyboardButton("❄️ INVERNO", callback_data="stagione_INVERNO")],
        [InlineKeyboardButton("🔍 RICERCA INGREDIENTE", callback_data="ricerca_ingrediente_start")],
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
    ordine_pasti = ["colazione", "spuntino", "pranzo", "spuntino_2", "cena", "dopo_cena"]
    
    for pasto in ordine_pasti:
        if pasto in menu_giorno:
            emoji = EMOJI_PASTI.get(pasto, "🍴")
            piatto = menu_giorno.get(pasto, "N/A")
            pasto_nome = pasto.upper().replace("_", " ")
            text += f"{emoji} *{pasto_nome}*\n{piatto}\n\n"
    
    settimana_num = settimana.split("_")[1]
    keyboard = [
        [InlineKeyboardButton("➕ Aggiungi a settimana", callback_data=f"add_to_settimana_{stagione}_{settimana_num}_{giorno_idx}")],
        [InlineKeyboardButton("⬅️ Giorno Precedente" if giorno_idx > 0 else "⬅️", 
                             callback_data=f"giorno_{stagione}_{settimana_num}_{giorno_idx - 1}" if giorno_idx > 0 else "skip"),
         InlineKeyboardButton("Giorno Successivo ➡️" if giorno_idx < len(GIORNI) - 1 else "➡️",
                             callback_data=f"giorno_{stagione}_{settimana_num}_{giorno_idx + 1}" if giorno_idx < len(GIORNI) - 1 else "skip")],
        [InlineKeyboardButton("⬅️ Giorni", callback_data=f"back_giorni_{stagione}_{settimana_num}")],
        [InlineKeyboardButton("🏠 HOME", callback_data="home")],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def mostra_menu_giorno_da_ricerca(query, context, stagione, settimana, giorno_idx):
    """Mostra il menu di un giorno specifico da ricerca ingrediente (con torna alla ricerca)"""
    giorno = GIORNI[giorno_idx]
    menu_giorno = MENU[stagione][settimana][giorno]
    
    text = f"*{stagione} - {settimana.replace('_', ' ')} - {giorno}*\n\n"
    
    # Ordine corretto dei pasti
    ordine_pasti = ["colazione", "spuntino", "pranzo", "spuntino_2", "cena", "dopo_cena"]
    
    for pasto in ordine_pasti:
        if pasto in menu_giorno:
            emoji = EMOJI_PASTI.get(pasto, "🍴")
            piatto = menu_giorno.get(pasto, "N/A")
            pasto_nome = pasto.upper().replace("_", " ")
            text += f"{emoji} *{pasto_nome}*\n{piatto}\n\n"
    
    settimana_num = settimana.split("_")[1]
    keyboard = [
        [InlineKeyboardButton("➕ Aggiungi a settimana", callback_data=f"add_to_settimana_{stagione}_{settimana_num}_{giorno_idx}")],
        [InlineKeyboardButton("⬅️ Torna alla ricerca", callback_data=f"ingrediente_indietro_stagione_{stagione}")],
        [InlineKeyboardButton("🏠 HOME", callback_data="home")],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")


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

async def mostra_ingredienti_categoria(query, categoria, user_id, context):
    """Mostra gli ingredienti della categoria scelta con opzioni di quantità"""
    ingredienti = INGREDIENTI_CATEGORIZZATI.get(categoria, [])
    
    if not ingredienti:
        await query.edit_message_text("❌ Nessun ingrediente trovato in questa categoria!")
        return
    
    # Inizializza le scelte dell'utente se non esistono
    if 'ingredienti_selezionati' not in context.user_data:
        context.user_data['ingredienti_selezionati'] = {}
    
    if categoria not in context.user_data['ingredienti_selezionati']:
        context.user_data['ingredienti_selezionati'][categoria] = {}
    
    text = f"""
*{categoria}*

Seleziona gli ingredienti che vuoi nella tua settimana:
(Clicca sul numero per la quantità nella settimana)
"""
    
    keyboard = []
    for ingrediente in sorted(ingredienti)[:12]:  # Limita a 12
        quantita = context.user_data['ingredienti_selezionati'][categoria].get(ingrediente, 0)
        label = f"{ingrediente} (x{quantita})" if quantita > 0 else ingrediente
        keyboard.append([
            InlineKeyboardButton(f"➕", callback_data=f"inc_ing_{categoria}_{ingrediente}"),
            InlineKeyboardButton(label, callback_data=f"show_ing_{categoria}_{ingrediente}"),
            InlineKeyboardButton(f"➖", callback_data=f"dec_ing_{categoria}_{ingrediente}")
        ])
    
    keyboard.append([InlineKeyboardButton("✅ CONTINUA", callback_data=f"continua_categoria_{categoria}")])
    keyboard.append([InlineKeyboardButton("⬅️ Indietro", callback_data="crea_settimana_start")])
    keyboard.append([InlineKeyboardButton("🏠 HOME", callback_data="home")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def modifica_quantita_ingrediente(query, categoria, ingrediente, delta, user_id, context):
    """Modifica la quantità di un ingrediente (aumenta o diminuisce)"""
    if 'ingredienti_selezionati' not in context.user_data:
        context.user_data['ingredienti_selezionati'] = {}
    
    if categoria not in context.user_data['ingredienti_selezionati']:
        context.user_data['ingredienti_selezionati'][categoria] = {}
    
    quantita_attuale = context.user_data['ingredienti_selezionati'][categoria].get(ingrediente, 0)
    nuova_quantita = max(0, quantita_attuale + delta)
    
    if nuova_quantita > 0:
        context.user_data['ingredienti_selezionati'][categoria][ingrediente] = nuova_quantita
    elif ingrediente in context.user_data['ingredienti_selezionati'][categoria]:
        del context.user_data['ingredienti_selezionati'][categoria][ingrediente]
    
    # Ricarica la vista
    await mostra_ingredienti_categoria(query, categoria, user_id, context)

async def mostra_prossima_categoria(query, categoria_attuale, user_id, context):
    """Mostra la prossima categoria o il riepilogo finale"""
    categorie = list(INGREDIENTI_CATEGORIZZATI.keys())
    idx_attuale = categorie.index(categoria_attuale)
    
    if idx_attuale + 1 < len(categorie):
        # Mostra prossima categoria
        prossima_categoria = categorie[idx_attuale + 1]
        await mostra_ingredienti_categoria(query, prossima_categoria, user_id, context)
    else:
        # Mostra riepilogo e opzione per creare settimana
        await mostra_riepilogo_ingredienti(query, user_id, context)

async def mostra_riepilogo_ingredienti(query, user_id, context):
    """Mostra il riepilogo degli ingredienti selezionati"""
    if 'ingredienti_selezionati' not in context.user_data or not context.user_data['ingredienti_selezionati']:
        await query.edit_message_text("❌ Nessun ingrediente selezionato!")
        return
    
    text = "*📋 RIEPILOGO INGREDIENTI*\n\n"
    
    ingredienti_totali = []
    for categoria, ingredienti in context.user_data['ingredienti_selezionati'].items():
        if ingredienti:
            text += f"{categoria}\n"
            for ingrediente, quantita in sorted(ingredienti.items()):
                text += f"  • {ingrediente} (x{quantita})\n"
                ingredienti_totali.extend([ingrediente] * quantita)
            text += "\n"
    
    text += f"\n*Totale richieste: {len(ingredienti_totali)}*"
    
    keyboard = [
        [InlineKeyboardButton("✅ CREA SETTIMANA", callback_data="crea_settimana_finale")],
        [InlineKeyboardButton("⬅️ Modifica", callback_data="crea_settimana_start")],
        [InlineKeyboardButton("🏠 HOME", callback_data="home")]
    ]
    
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
    ingredienti_usati = []
    giorni_usati = set()
    
    # STEP 1: Ordina gli ingredienti e cerca di matchare il più possibile
    ingredienti_da_matchare = ingredienti_richiesti.copy()
    
    for ingrediente in ingredienti_da_matchare:
        if len(settimana_generata) >= 7:  # Max 7 giorni
            break
        
        giorni_disponibili = trova_giorni_con_ingrediente(ingrediente)
        
        # Filtra i giorni già usati
        giorni_disponibili = [g for g in giorni_disponibili if (g['stagione'], g['settimana'], g['giorno']) not in giorni_usati]
        
        if giorni_disponibili:
            # Scegli un giorno casuale
            giorno_scelto = random.choice(giorni_disponibili)
            key = (giorno_scelto['stagione'], giorno_scelto['settimana'], giorno_scelto['giorno'])
            
            # Verifica se il giorno è già nella settimana (per aggiungere ingredienti nello stesso giorno se possibile)
            giorno_aggiunto = False
            for idx, giorno in settimana_generata.items():
                if (giorno['stagione'], giorno['settimana'], giorno['giorno']) == key:
                    # Giorno già nella settimana, marca come usato
                    giorno_aggiunto = True
                    ingredienti_usati.append(ingrediente)
                    break
            
            if not giorno_aggiunto:
                settimana_generata[len(settimana_generata)] = giorno_scelto
                giorni_usati.add(key)
                ingredienti_usati.append(ingrediente)
    
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
    # Raccogli tutti gli ingredienti selezionati con le quantità
    ingredienti_richiesti = []
    for categoria, ingredienti_dict in context.user_data.get('ingredienti_selezionati', {}).items():
        # ingredienti_dict è ora un dizionario con {ingrediente: quantita}
        for ingrediente, quantita in ingredienti_dict.items():
            ingredienti_richiesti.extend([ingrediente] * quantita)
    
    if not ingredienti_richiesti:
        await query.edit_message_text("❌ Nessun ingrediente selezionato!")
        return
    
    # Genera la settimana
    settimana, ingredienti_usati = genera_settimana_personalizzata(ingredienti_richiesti)
    
    # Salva in context per uso successivo
    context.user_data['settimana_generata'] = settimana
    
    # Mostra la settimana generata
    text = "🎉 SETTIMANA GENERATA!\n\n"
    for idx, giorno_data in settimana.items():
        giorno_num = idx + 1
        text += f"Giorno {giorno_num}: {giorno_data['giorno']}\n"
        text += f"({giorno_data['stagione']} - {giorno_data['settimana']})\n\n"
    
    keyboard = [
        [InlineKeyboardButton("💾 SALVA SETTIMANA", callback_data="salva_settimana_nome")],
        [InlineKeyboardButton("🏠 HOME", callback_data="home")],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup)

async def salva_settimana_con_nome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Salva la settimana generata con il nome fornito"""
    if not context.user_data.get('in_salvataggio'):
        return
    
    nome_settimana = update.message.text.strip()
    
    if not nome_settimana or len(nome_settimana) < 2:
        await update.message.reply_text("❌ Il nome deve avere almeno 2 caratteri!")
        return
    
    user_id = update.effective_user.id
    settimana = context.user_data.get('settimana_generata', {})
    
    if not settimana:
        await update.message.reply_text("❌ Nessuna settimana da salvare!")
        return
    
    # Carica o crea il file settimane_salvate.json
    try:
        with open('settimane_salvate.json', 'r', encoding='utf-8') as f:
            settimane_salvate = json.load(f)
    except FileNotFoundError:
        settimane_salvate = {}
    
    # Aggiungi l'utente se non esiste
    if str(user_id) not in settimane_salvate:
        settimane_salvate[str(user_id)] = {}
    
    # Salva la settimana con il nome
    settimane_salvate[str(user_id)][nome_settimana] = {
        'data_creazione': str(__import__('datetime').datetime.now()),
        'settimana': settimana
    }
    
    # Scrivi su file
    with open('settimane_salvate.json', 'w', encoding='utf-8') as f:
        json.dump(settimane_salvate, f, ensure_ascii=False, indent=2)
    
    # Pulisci il flag
    context.user_data['in_salvataggio'] = False
    context.user_data['settimana_generata'] = {}
    
    # Invia conferma
    text = f"""
✅ *SETTIMANA SALVATA!*

Nome: {nome_settimana}
Data: {__import__('datetime').datetime.now().strftime('%d/%m/%Y %H:%M')}

La tua settimana è stata salvata con successo!
Puoi visualizzarla in "LE MIE SETTIMANE"
"""
    
    keyboard = [
        [InlineKeyboardButton("📁 LE MIE SETTIMANE", callback_data="mie_settimane_start")],
        [InlineKeyboardButton("🏠 HOME", callback_data="home")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def mostra_mie_settimane(query, user_id):
    """Mostra le settimane salvate dall'utente"""
    try:
        with open('settimane_salvate.json', 'r', encoding='utf-8') as f:
            settimane_salvate = json.load(f)
    except FileNotFoundError:
        text = "📁 LE MIE SETTIMANE\n\n❌ Non hai ancora salvato nessuna settimana!"
        keyboard = [[InlineKeyboardButton("🏠 HOME", callback_data="home")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)
        return
    
    utente_settimane = settimane_salvate.get(str(user_id), {})
    
    if not utente_settimane:
        text = "📁 LE MIE SETTIMANE\n\n❌ Non hai ancora salvato nessuna settimana!"
        keyboard = [[InlineKeyboardButton("🏠 HOME", callback_data="home")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)
        return
    
    text = "📁 LE MIE SETTIMANE\n\n"
    keyboard = []
    
    for idx, (nome_settimana, dati) in enumerate(utente_settimane.items()):
        data_creazione = dati.get('data_creazione', 'N/A')
        text += f"{idx + 1}. {nome_settimana}\n   ({data_creazione})\n\n"
        keyboard.append([InlineKeyboardButton(f"📖 Visualizza: {nome_settimana}", callback_data=f"visualizza_settimana_{nome_settimana}")])
    
    keyboard.append([InlineKeyboardButton("🏠 HOME", callback_data="home")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup)

async def visualizza_settimana_salvata(query, user_id, nome_settimana):
    """Visualizza una settimana salvata con bottoni per i giorni"""
    try:
        with open('settimane_salvate.json', 'r', encoding='utf-8') as f:
            settimane_salvate = json.load(f)
    except FileNotFoundError:
        await query.edit_message_text("❌ File settimane non trovato!")
        return
    except Exception as e:
        await query.edit_message_text(f"❌ Errore lettura file: {str(e)}")
        return
    
    dati_settimana = settimane_salvate.get(str(user_id), {}).get(nome_settimana)
    
    if not dati_settimana:
        await query.edit_message_text(f"❌ Settimana '{nome_settimana}' non trovata!")
        return
    
    settimana = dati_settimana.get('settimana', {})
    data_creazione = dati_settimana.get('data_creazione', 'N/A')
    
    if not settimana:
        await query.edit_message_text("❌ Dati settimana non validi!")
        return
    
    text = f"📖 *{nome_settimana}*\n\nData creazione: {data_creazione}\n\n*Scegli un giorno:*"
    
    keyboard = []
    
    # Crea bottoni per ogni giorno
    for idx in sorted([int(i) for i in settimana.keys()]):
        giorno_data = settimana[str(idx)]
        giorno_num = idx + 1
        giorno_nome = giorno_data.get('giorno', 'Giorno sconosciuto')
        
        keyboard.append([InlineKeyboardButton(
            f"📅 Giorno {giorno_num}: {giorno_nome}",
            callback_data=f"visualizza_giorno_salvato_{nome_settimana}#{idx}"
        )])
    
    keyboard.append([InlineKeyboardButton("🗑️ ELIMINA", callback_data=f"elimina_settimana_{nome_settimana}")])
    keyboard.append([InlineKeyboardButton("⬅️ Indietro", callback_data="mie_settimane_start")])
    keyboard.append([InlineKeyboardButton("🏠 HOME", callback_data="home")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def elimina_settimana_salvata(query, user_id, nome_settimana):
    """Elimina una settimana salvata"""
    try:
        with open('settimane_salvate.json', 'r', encoding='utf-8') as f:
            settimane_salvate = json.load(f)
    except FileNotFoundError:
        await query.edit_message_text("❌ Errore: file settimane non trovato!")
        return
    
    if str(user_id) in settimane_salvate and nome_settimana in settimane_salvate[str(user_id)]:
        del settimane_salvate[str(user_id)][nome_settimana]
        
        with open('settimane_salvate.json', 'w', encoding='utf-8') as f:
            json.dump(settimane_salvate, f, ensure_ascii=False, indent=2)
        
        await query.edit_message_text(f"✅ Settimana '{nome_settimana}' eliminata!")
        await mostra_mie_settimane(query, user_id)
    else:
        await query.edit_message_text("❌ Settimana non trovata!")

async def visualizza_giorno_settimana_salvata(query, user_id, nome_settimana, giorno_idx):
    """Visualizza un giorno specifico di una settimana salvata"""
    try:
        with open('settimane_salvate.json', 'r', encoding='utf-8') as f:
            settimane_salvate = json.load(f)
    except FileNotFoundError:
        await query.edit_message_text("❌ File settimane non trovato!")
        return
    
    settimana = settimane_salvate.get(str(user_id), {}).get(nome_settimana, {}).get('settimana', {})
    giorno_data = settimana.get(str(giorno_idx))
    
    if not giorno_data:
        # Debug: mostra le chiavi disponibili
        chiavi = list(settimana.keys())
        await query.edit_message_text(f"❌ Giorno non trovato!\nChiavi disponibili: {chiavi}\nRicercando: {str(giorno_idx)}")
        return
    
    giorno_num = int(giorno_idx) + 1
    giorno_nome = giorno_data.get('giorno', 'Sconosciuto')
    stagione = giorno_data.get('stagione', 'Sconosciuta')
    settimana_nome = giorno_data.get('settimana', 'Sconosciuta')
    
    text = f"📅 <b>Giorno {giorno_num}: {giorno_nome}</b>\n\n"
    text += f"({stagione} - {settimana_nome})\n\n"
    
    # Mostra i pasti del giorno
    for pasto, descrizione in giorno_data.items():
        if pasto not in ['giorno', 'stagione', 'settimana', 'menu']:
            if isinstance(descrizione, str):
                text += f"<b>{pasto.upper()}</b>\n{descrizione}\n\n"
    
    # Se non hai trovato pasti personali, mostra il menu
    if not any(k not in ['giorno', 'stagione', 'settimana', 'menu'] for k in giorno_data.keys()):
        menu = giorno_data.get('menu', {})
        if menu:
            for pasto, descrizione in menu.items():
                if isinstance(descrizione, str):
                    text += f"<b>{pasto.upper()}</b>\n{descrizione}\n\n"
    
    keyboard = [
        [InlineKeyboardButton("⬅️ Indietro", callback_data=f"visualizza_settimana_{nome_settimana}")],
        [InlineKeyboardButton("🏠 HOME", callback_data="home")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="HTML")

async def salva_settimana_con_nome_wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Wrapper per gestire il salvataggio o ricerca ingrediente"""
    if context.user_data.get('in_salvataggio'):
        await salva_settimana_con_nome(update, context)
    else:
        await cerca_ingrediente(update, context)

# ============================================================
# AGGIUNGI GIORNO A SETTIMANA
# ============================================================

async def aggiungi_giorno_a_settimana_start(query, user_id, stagione, settimana_num, giorno_idx):
    """Mostra la lista delle settimane salvate per aggiungere il giorno"""
    # Carica le settimane salvate dell'utente
    try:
        with open(SCRIPT_DIR / 'settimane_utenti.json', 'r', encoding='utf-8') as f:
            settimane_utenti = json.load(f)
    except FileNotFoundError:
        await query.answer("❌ Nessuna settimana salvata ancora!", show_alert=True)
        return
    
    user_settimane = settimane_utenti.get(str(user_id), {})
    if not user_settimane:
        await query.answer("❌ Nessuna settimana salvata ancora!", show_alert=True)
        return
    
    # Salva il giorno selezionato in context
    giorno = GIORNI[giorno_idx]
    settimana = f"SETTIMANA_{settimana_num}"
    menu_giorno = MENU[stagione][settimana][giorno]
    
    # Crea la struttura del giorno per il salvataggio
    giorno_data = {
        "stagione": stagione,
        "settimana": settimana,
        "giorno": giorno,
        "menu": menu_giorno
    }
    
    text = f"*Aggiungi a quale settimana?*\n\nGiorno selezionato: {stagione} - {giorno}\n\n"
    keyboard = []
    
    for nome_settimana in sorted(user_settimane.keys()):
        keyboard.append([InlineKeyboardButton(nome_settimana, 
                                             callback_data=f"select_dest_week_{nome_settimana}#{stagione}_{settimana_num}_{giorno_idx}")])
    
    keyboard.append([InlineKeyboardButton("⬅️ Indietro", callback_data=f"back_settimane_{stagione}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def select_dest_week(query, context, nome_settimana, stagione, settimana_num, giorno_idx):
    """Mostra lo stato della settimana di destinazione con gli slot vuoti"""
    user_id = query.from_user.id
    
    # Carica le settimane salvate
    try:
        with open(SCRIPT_DIR / 'settimane_utenti.json', 'r', encoding='utf-8') as f:
            settimane_utenti = json.load(f)
    except FileNotFoundError:
        await query.answer("❌ Errore nel caricamento!", show_alert=True)
        return
    
    user_settimane = settimane_utenti.get(str(user_id), {})
    settimana_dest = user_settimane.get(nome_settimana, {})
    
    # Mostra lo stato della settimana con slot vuoti e pieni
    text = f"*Settimana: {nome_settimana}*\n\n"
    text += f"*Aggiungi il giorno:* {GIORNI[giorno_idx]}\n\n"
    
    for i, giorno in enumerate(GIORNI):
        if giorno in settimana_dest:
            emoji = "✅"
            text += f"{emoji} *{giorno}*: {list(settimana_dest[giorno].values())[0] if isinstance(settimana_dest[giorno], dict) else settimana_dest[giorno]}\n"
        else:
            emoji = "⬜"
            text += f"{emoji} *{giorno}*: vuoto\n"
    
    keyboard = []
    # Mostra i pulsanti solo per gli slot vuoti
    row = []
    for i, giorno in enumerate(GIORNI):
        if giorno not in settimana_dest:
            row.append(InlineKeyboardButton(f"➕ {giorno}", 
                                           callback_data=f"add_day_slot_{nome_settimana}#{stagione}_{settimana_num}_{giorno_idx}#{i}"))
            if len(row) == 2:
                keyboard.append(row)
                row = []
    if row:
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("⬅️ Indietro", callback_data="home")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def add_day_to_week_slot(query, context, nome_settimana, stagione, settimana_num, giorno_idx, slot_idx):
    """Aggiunge il giorno allo slot scelto della settimana"""
    user_id = query.from_user.id
    
    try:
        with open(SCRIPT_DIR / 'settimane_utenti.json', 'r', encoding='utf-8') as f:
            settimane_utenti = json.load(f)
    except FileNotFoundError:
        settimane_utenti = {}
    
    user_settimane = settimane_utenti.get(str(user_id), {})
    
    # Ottieni il giorno da aggiungere
    giorno_source = GIORNI[giorno_idx]
    settimana_source = f"SETTIMANA_{settimana_num}"
    menu_giorno = MENU[stagione][settimana_source][giorno_source]
    
    # Ottieni il giorno slot dove aggiungere
    giorno_dest = GIORNI[slot_idx]
    
    # Aggiungi il giorno alla settimana di destinazione
    if nome_settimana not in user_settimane:
        user_settimane[nome_settimana] = {}
    
    user_settimane[nome_settimana][giorno_dest] = menu_giorno
    settimane_utenti[str(user_id)] = user_settimane
    
    # Salva
    with open(SCRIPT_DIR / 'settimane_utenti.json', 'w', encoding='utf-8') as f:
        json.dump(settimane_utenti, f, ensure_ascii=False, indent=2)
    
    await query.answer(f"✅ {giorno_source} aggiunto a {nome_settimana} come {giorno_dest}!", show_alert=True)
    
    # Mostra di nuovo la settimana
    await select_dest_week(query, context, nome_settimana, stagione, settimana_num, giorno_idx)

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
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, salva_settimana_con_nome_wrapper))
    
    print("🚀 Bot avviato! Premi Ctrl+C per fermare.")
    app.run_polling()

if __name__ == "__main__":
    main()
