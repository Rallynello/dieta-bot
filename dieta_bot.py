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
import psycopg2
import psycopg2.extras
import aiohttp
from pathlib import Path
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from bring_api import Bring, BringAuthException, BringRequestException
from cryptography.fernet import Fernet

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================
# ENCRYPTION SETUP
# ============================================================

ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')
if not ENCRYPTION_KEY:
    ENCRYPTION_KEY = Fernet.generate_key()
    logger.warning("⚠️ ENCRYPTION_KEY non trovata, generata una nuova chiave. Salva questa su Railway ENV!")
    logger.warning(f"ENCRYPTION_KEY={ENCRYPTION_KEY.decode()}")

cipher = Fernet(ENCRYPTION_KEY)

# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_db_connection():
    """Crea una connessione al database PostgreSQL"""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise Exception("DATABASE_URL non configurato!")
    
    try:
        conn = psycopg2.connect(database_url)
        return conn
    except Exception as e:
        logger.error(f"Errore connessione DB: {e}")
        raise

def init_db():
    """Crea le tabelle se non esistono"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS settimane (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                nome_settimana VARCHAR(255) NOT NULL,
                settimana_data JSONB NOT NULL,
                data_creazione TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, nome_settimana)
            );
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS liste_spesa (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                nome_lista VARCHAR(255) NOT NULL,
                stagione VARCHAR(50) NOT NULL,
                settimana_num INTEGER NOT NULL,
                ingredienti JSONB NOT NULL,
                data_creazione TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, nome_lista)
            );
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS bring_credentials (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL UNIQUE,
                email_encrypted TEXT NOT NULL,
                password_encrypted TEXT NOT NULL,
                lista_uuid_default TEXT,
                lista_name_default TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        conn.commit()
        cur.close()
        conn.close()
        logger.info("✅ Tabelle inizializzate")
    except Exception as e:
        logger.error(f"Errore init DB: {e}")

# ============================================================
# FUNZIONI DATABASE
# ============================================================

def get_settimane_utente(user_id):
    """Legge tutte le settimane di un utente"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cur.execute(
            "SELECT nome_settimana, settimana_data FROM settimane WHERE user_id = %s ORDER BY data_creazione",
            (user_id,)
        )
        
        result = {}
        for row in cur.fetchall():
            result[row['nome_settimana']] = {
                'settimana': row['settimana_data']['settimana'],
                'data_creazione': str(row['settimana_data'].get('data_creazione', ''))
            }
        
        cur.close()
        conn.close()
        return result
    except Exception as e:
        logger.error(f"Errore get_settimane_utente: {e}")
        return {}

def get_settimana(user_id, nome_settimana):
    """Legge una singola settimana"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cur.execute(
            "SELECT settimana_data FROM settimane WHERE user_id = %s AND nome_settimana = %s",
            (user_id, nome_settimana)
        )
        
        row = cur.fetchone()
        cur.close()
        conn.close()
        
        if row:
            return row['settimana_data']
        return None
    except Exception as e:
        logger.error(f"Errore get_settimana: {e}")
        return None

def save_settimana(user_id, nome_settimana, settimana_data):
    """Salva o aggiorna una settimana"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        from datetime import datetime
        data_creazione = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        data_to_save = {
            'settimana': settimana_data,
            'data_creazione': data_creazione
        }
        
        cur.execute(
            """
            INSERT INTO settimane (user_id, nome_settimana, settimana_data)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id, nome_settimana) DO UPDATE
            SET settimana_data = EXCLUDED.settimana_data
            """,
            (user_id, nome_settimana, json.dumps(data_to_save))
        )
        
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"✅ Settimana salvata: {user_id} - {nome_settimana}")
    except Exception as e:
        logger.error(f"Errore save_settimana: {e}")

def delete_settimana(user_id, nome_settimana):
    """Elimina una settimana"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            "DELETE FROM settimane WHERE user_id = %s AND nome_settimana = %s",
            (user_id, nome_settimana)
        )
        
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"✅ Settimana eliminata: {user_id} - {nome_settimana}")
    except Exception as e:
        logger.error(f"Errore delete_settimana: {e}")

def init_liste_spesa_table():
    """Crea la tabella liste_spesa se non esiste"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS liste_spesa (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                nome_lista VARCHAR(255) NOT NULL,
                stagione VARCHAR(50) NOT NULL,
                settimana_num INTEGER NOT NULL,
                ingredienti JSONB NOT NULL,
                data_creazione TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, nome_lista)
            );
        """)
        
        conn.commit()
        cur.close()
        conn.close()
        logger.info("✅ Tabella liste_spesa inizializzata")
    except Exception as e:
        logger.error(f"Errore init liste_spesa: {e}")

def save_lista_spesa(user_id, nome_lista, stagione, settimana_num, ingredienti):
    """Salva una lista della spesa"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            """
            INSERT INTO liste_spesa (user_id, nome_lista, stagione, settimana_num, ingredienti)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (user_id, nome_lista) DO UPDATE
            SET ingredienti = EXCLUDED.ingredienti, stagione = EXCLUDED.stagione, settimana_num = EXCLUDED.settimana_num
            """,
            (user_id, nome_lista, stagione, settimana_num, json.dumps(ingredienti))
        )
        
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"✅ Lista spesa salvata: {user_id} - {nome_lista}")
    except Exception as e:
        logger.error(f"Errore save_lista_spesa: {e}")

def get_liste_spesa_utente(user_id):
    """Legge tutte le liste della spesa di un utente"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cur.execute(
            "SELECT nome_lista, stagione, settimana_num, ingredienti FROM liste_spesa WHERE user_id = %s ORDER BY data_creazione",
            (user_id,)
        )
        
        result = {}
        for row in cur.fetchall():
            result[row['nome_lista']] = {
                'stagione': row['stagione'],
                'settimana_num': row['settimana_num'],
                'ingredienti': row['ingredienti']
            }
        
        cur.close()
        conn.close()
        return result
    except Exception as e:
        logger.error(f"Errore get_liste_spesa_utente: {e}")
        return {}

def get_lista_spesa(user_id, nome_lista):
    """Legge una singola lista della spesa"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cur.execute(
            "SELECT stagione, settimana_num, ingredienti FROM liste_spesa WHERE user_id = %s AND nome_lista = %s",
            (user_id, nome_lista)
        )
        
        row = cur.fetchone()
        cur.close()
        conn.close()
        
        if row:
            return {
                'stagione': row['stagione'],
                'settimana_num': row['settimana_num'],
                'ingredienti': row['ingredienti']
            }
        return None
    except Exception as e:
        logger.error(f"Errore get_lista_spesa: {e}")
        return None

def delete_lista_spesa(user_id, nome_lista):
    """Elimina una lista della spesa"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            "DELETE FROM liste_spesa WHERE user_id = %s AND nome_lista = %s",
            (user_id, nome_lista)
        )
        
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"✅ Lista spesa eliminata: {user_id} - {nome_lista}")
    except Exception as e:
        logger.error(f"Errore delete_lista_spesa: {e}")

# ============================================================
# BRING CREDENTIALS HELPERS
# ============================================================

def encrypt_password(password: str) -> str:
    """Crittografa una password con Fernet"""
    return cipher.encrypt(password.encode()).decode()

def decrypt_password(encrypted: str) -> str:
    """Decrittografa una password con Fernet"""
    return cipher.decrypt(encrypted.encode()).decode()

def save_bring_credentials(user_id: int, email: str, password: str, lista_uuid: str, lista_name: str):
    """Salva le credenziali Bring criptate nel database"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        email_enc = encrypt_password(email)
        password_enc = encrypt_password(password)
        
        cur.execute(
            """
            INSERT INTO bring_credentials (user_id, email_encrypted, password_encrypted, lista_uuid_default, lista_name_default)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (user_id) DO UPDATE
            SET email_encrypted = EXCLUDED.email_encrypted,
                password_encrypted = EXCLUDED.password_encrypted,
                lista_uuid_default = EXCLUDED.lista_uuid_default,
                lista_name_default = EXCLUDED.lista_name_default,
                updated_at = CURRENT_TIMESTAMP
            """,
            (user_id, email_enc, password_enc, lista_uuid, lista_name)
        )
        
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"✅ Credenziali Bring salvate per user {user_id}")
    except Exception as e:
        logger.error(f"Errore save_bring_credentials: {e}")

def get_bring_credentials(user_id: int) -> dict | None:
    """Legge le credenziali Bring decrittate dal database"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cur.execute(
            "SELECT email_encrypted, password_encrypted, lista_uuid_default, lista_name_default FROM bring_credentials WHERE user_id = %s",
            (user_id,)
        )
        
        row = cur.fetchone()
        cur.close()
        conn.close()
        
        if row:
            return {
                'email': decrypt_password(row['email_encrypted']),
                'password': decrypt_password(row['password_encrypted']),
                'lista_uuid': row['lista_uuid_default'],
                'lista_name': row['lista_name_default']
            }
        return None
    except Exception as e:
        logger.error(f"Errore get_bring_credentials: {e}")
        return None

def delete_bring_credentials(user_id: int):
    """Elimina le credenziali Bring di un utente"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("DELETE FROM bring_credentials WHERE user_id = %s", (user_id,))
        
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"✅ Credenziali Bring eliminate per user {user_id}")
    except Exception as e:
        logger.error(f"Errore delete_bring_credentials: {e}")

# ============================================================
# BRING API FUNCTIONS
# ============================================================

async def fetch_bring_lists(email: str, password: str) -> list | None:
    """Fetcha le liste Bring disponibili usando email e password"""
    try:
        async with aiohttp.ClientSession() as session:
            bring = Bring(session, email, password)
            await bring.login()
            result = await bring.load_lists()
            
            # result è un BringListResponse con attributo .lists
            bring_lists = [
                {'name': lst.name, 'listUuid': lst.listUuid}
                for lst in result.lists
            ]
            
            logger.info(f"✅ Fetched {len(bring_lists)} liste da Bring")
            return bring_lists
    except BringAuthException:
        logger.error("❌ Bring auth error: credenziali errate")
        return None
    except BringRequestException as e:
        logger.error(f"❌ Bring request error: {e}")
        return None
    except Exception as e:
        logger.error(f"❌ Errore fetch_bring_lists: {e}")
        return None

async def upload_to_bring(email: str, password: str, lista_uuid: str, ingredienti: list) -> int:
    """Carica gli ingredienti su una lista Bring"""
    try:
        async with aiohttp.ClientSession() as session:
            bring = Bring(session, email, password)
            await bring.login()
            
            items_added = 0
            for ingrediente in ingredienti:
                parts = ingrediente.split(' (x')
                nome = parts[0].strip()
                spec = f"x{parts[1]}" if len(parts) > 1 else ""
                
                try:
                    await bring.save_item(lista_uuid, nome, spec)
                    items_added += 1
                except Exception as e:
                    logger.warning(f"⚠️ Errore caricamento ingrediente '{nome}': {e}")
            
            logger.info(f"✅ Caricati {items_added}/{len(ingredienti)} ingredienti su Bring")
            return items_added
    except BringAuthException:
        logger.error("❌ Bring auth error durante upload")
        return 0
    except BringRequestException as e:
        logger.error(f"❌ Bring request error durante upload: {e}")
        return 0
    except Exception as e:
        logger.error(f"❌ Errore upload_to_bring: {e}")
        return 0

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
        [
            InlineKeyboardButton("☀️ ESTATE", callback_data="stagione_ESTATE"),
            InlineKeyboardButton("🌱 PRIMAVERA", callback_data="stagione_PRIMAVERA"),
            InlineKeyboardButton("❄️ INVERNO", callback_data="stagione_INVERNO")
        ],
        [
            InlineKeyboardButton("🔍 RICERCA INGREDIENTE", callback_data="ricerca_ingrediente_start"),
            InlineKeyboardButton("✨ CREA SETTIMANA", callback_data="crea_settimana_start")
        ],
        [
            InlineKeyboardButton("🛒 LISTA DELLA SPESA", callback_data="lista_spesa_start"),
            InlineKeyboardButton("📁 LE MIE SETTIMANE", callback_data="mie_settimane_start")
        ],
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
    
    # Check obiettivo
    elif data.startswith("check_obiettivo_"):
        nome_settimana = data.replace("check_obiettivo_", "")
        await check_obiettivo_settimana(query, update.effective_user.id, nome_settimana)
    
    # Menu per eliminare giorno
    elif data.startswith("elimina_giorno_menu_"):
        nome_settimana = data.replace("elimina_giorno_menu_", "")
        await mostra_menu_elimina_giorno(query, update.effective_user.id, nome_settimana)
    
    # Elimina un giorno specifico
    elif data.startswith("elimina_giorno_"):
        parts = data.replace("elimina_giorno_", "").split("#")
        nome_settimana = parts[0]
        giorno_idx = int(parts[1])
        await elimina_giorno_da_settimana(query, update.effective_user.id, nome_settimana, giorno_idx)
    
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
        await aggiungi_giorno_a_settimana_start(query, update.effective_user.id, stagione, settimana_num, giorno_idx, context)
    
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
    
    # Crea nuova settimana vuota dal menu di scelta
    elif data.startswith("create_new_empty_week#"):
        parts = data.replace("create_new_empty_week#", "").split("_")
        stagione = parts[0]
        settimana_num = parts[1]
        giorno_idx = int(parts[2])
        context.user_data['creating_empty_week'] = True
        context.user_data['pending_add_to_week'] = f"{stagione}_{settimana_num}_{giorno_idx}"
        await query.edit_message_text(
            "📝 *Scrivi il nome della nuova settimana:*\n\n"
            "(es: 'Pippo', 'La mia', 'Estiva', ecc.)",
            parse_mode="Markdown"
        )
    
    # Lista della spesa - inizio flusso
    elif data == "lista_spesa_start":
        await mostra_liste_spesa_utente(query, update.effective_user.id)
    
    # Lista della spesa - scegli stagione
    elif data.startswith("crea_lista_spesa_"):
        stagione = data.replace("crea_lista_spesa_", "")
        await mostra_settimane_per_lista(query, update.effective_user.id, stagione)
    
    # Lista della spesa - salva lista (clic su settimana)
    elif data.startswith("salva_lista_spesa_"):
        parts = data.replace("salva_lista_spesa_", "").split("_")
        stagione = parts[0]
        settimana_num = int(parts[1])
        await mostra_giorni_per_lista(query, update.effective_user.id, stagione, settimana_num)
    
    # Lista della spesa - mostra lista di un giorno specifico
    elif data.startswith("lista_giorno_"):
        parts = data.replace("lista_giorno_", "").split("_")
        stagione = parts[0]
        settimana_num = int(parts[1])
        giorno = "_".join(parts[2:])  # Il giorno potrebbe avere underscore
        await mostra_lista_giorno_spesa(query, update.effective_user.id, stagione, settimana_num, giorno, context)
    
    # Lista della spesa - toggle ingrediente
    elif data.startswith("toggle_lista_ing_"):
        parts = data.replace("toggle_lista_ing_", "").split("_")
        nome_lista = parts[0]
        ing_idx = int(parts[1])
        await toggle_ingrediente_lista(query, update.effective_user.id, nome_lista, ing_idx, context)
    
    # Lista della spesa - visualizza lista salvata
    elif data.startswith("visualizza_lista_spesa_"):
        nome_lista = data.replace("visualizza_lista_spesa_", "")
        await visualizza_lista_spesa(query, update.effective_user.id, nome_lista, context)
    
    # Lista della spesa - elimina lista
    elif data.startswith("elimina_lista_spesa_"):
        nome_lista = data.replace("elimina_lista_spesa_", "")
        delete_lista_spesa(update.effective_user.id, nome_lista)
        await query.answer(f"✅ Lista '{nome_lista}' eliminata!", show_alert=True)
        await mostra_liste_spesa_utente(query, update.effective_user.id)
    
    # Lista della spesa - scegli da settimana salvata
    elif data == "lista_spesa_da_salvata":
        await mostra_settimane_salvate_per_lista(query, update.effective_user.id)
    
    # Lista della spesa - crea da settimana salvata
    elif data.startswith("lista_spesa_da_salvata_"):
        nome_settimana = data.replace("lista_spesa_da_salvata_", "")
        await mostra_giorni_settimana_salvata_per_lista(query, update.effective_user.id, nome_settimana)
    
    # Lista della spesa - scegli giorno da settimana salvata
    elif data.startswith("lista_spesa_giorno_salvato_"):
        parts = data.replace("lista_spesa_giorno_salvato_", "").split("#")
        nome_settimana = parts[0]
        giorno_idx = int(parts[1])
        await salva_lista_spesa_da_giorno_salvato(query, update.effective_user.id, nome_settimana, giorno_idx, context)
    
    # Bring - inizio flusso DA LISTA DELLA SPESA (con filtro spuntati)
    elif data.startswith("bring_start_lista_"):
        nome_lista = data.replace("bring_start_lista_", "")
        dati_lista = get_lista_spesa(update.effective_user.id, nome_lista)
        
        if not dati_lista:
            await query.answer("❌ Lista non trovata!", show_alert=True)
            return
        
        # Filtra SOLO ingredienti spuntati
        ingredienti_spuntati = [
            ing_data['nome'] for ing_data in dati_lista.get('ingredienti', {}).values()
            if ing_data.get('spuntato', False)
        ]
        
        if not ingredienti_spuntati:
            await query.answer("⚠️ Nessun ingrediente selezionato! Spunta almeno uno.", show_alert=True)
            return
        
        # Salva in context per il flusso Bring
        context.user_data['bring_nome_lista'] = nome_lista
        context.user_data['bring_ingredienti'] = ingredienti_spuntati
        context.user_data['bring_lista_spesa_source'] = nome_lista  # Per resettare dopo
        
        credenziali = get_bring_credentials(update.effective_user.id)
        if credenziali:
            await mostra_liste_bring(query, update.effective_user.id, nome_lista, ingredienti_spuntati, context)
        else:
            context.user_data['in_bring_email'] = True
            await query.edit_message_text(
                "📧 *Dimmi la tua email Bring:*\n\n"
                "(Puoi crearla su https://web.getbring.com)",
                parse_mode="Markdown"
            )
    
    # Bring - inizio flusso STANDARD
    elif data == "bring_start":
        logger.info(f"🔵 DEBUG: bring_start trigger")
        nome_lista = context.user_data.get('current_lista_spesa')
        logger.info(f"🔵 DEBUG: current_lista_spesa = {nome_lista}")
        if not nome_lista:
            logger.error("❌ DEBUG: nome_lista è None!")
            await query.answer("❌ Errore: lista non trovata", show_alert=True)
            return
        
        ingredienti = context.user_data.get(f'lista_ingredienti_{nome_lista}', [])
        if not ingredienti:
            logger.info(f"🔵 DEBUG: Fetching da DB per {nome_lista}")
            dati_lista = get_lista_spesa(update.effective_user.id, nome_lista)
            if dati_lista:
                ingredienti = [ing_data['nome'] for ing_data in dati_lista.get('ingredienti', {}).values()]
        
        logger.info(f"🔵 DEBUG: Trovati {len(ingredienti)} ingredienti")
        credenziali = get_bring_credentials(update.effective_user.id)
        if credenziali:
            logger.info(f"🔵 DEBUG: Credenziali trovate, mostra liste")
            await mostra_liste_bring(query, update.effective_user.id, nome_lista, ingredienti, context)
        else:
            logger.info(f"🔵 DEBUG: No credenziali, richiedo email")
            context.user_data['bring_nome_lista'] = nome_lista
            context.user_data['bring_ingredienti'] = ingredienti
            context.user_data['in_bring_email'] = True
            await query.edit_message_text(
                "📧 *Dimmi la tua email Bring:*\n\n"
                "(Puoi crearla su https://web.getbring.com)",
                parse_mode="Markdown"
            )
    
    # Bring - seleziona lista per upload
    elif data.startswith("bring_upload_"):
        lista_uuid = data.replace("bring_upload_", "")
        nome_lista = context.user_data.get('bring_nome_lista')
        ingredienti = context.user_data.get('bring_ingredienti', [])
        email = context.user_data.get('bring_email')
        password = context.user_data.get('bring_password')
        lista_spesa_source = context.user_data.get('bring_lista_spesa_source')  # Nome lista della spesa originale
        
        # Recupera il VERO nome della lista dal UUID usando la mappa
        uuid_to_name = context.user_data.get('bring_uuid_to_name', {})
        lista_name = uuid_to_name.get(lista_uuid, 'Bring')
        
        if email and password and nome_lista:
            await query.edit_message_text("⏳ *Caricamento ingredienti su Bring...*", parse_mode="Markdown")
            items_added = await upload_to_bring(email, password, lista_uuid, ingredienti)
            
            if items_added > 0:
                save_bring_credentials(update.effective_user.id, email, password, lista_uuid, lista_name)
                
                # Resetta gli spuntati nella lista della spesa originale
                if lista_spesa_source:
                    dati_lista = get_lista_spesa(update.effective_user.id, lista_spesa_source)
                    if dati_lista:
                        ingredienti_dict = dati_lista.get('ingredienti', {})
                        # Resetta TUTTI gli ingredienti a spuntato: False
                        for idx in ingredienti_dict:
                            ingredienti_dict[idx]['spuntato'] = False
                        # Salva nel DB
                        save_lista_spesa(update.effective_user.id, lista_spesa_source, 
                                        dati_lista.get('stagione'), dati_lista.get('settimana_num'), 
                                        ingredienti_dict)
                
                await query.edit_message_text(
                    f"✅ *{items_added} ingredienti inviati a {lista_name}!*\n\n"
                    f"📋 Lista della spesa resettata",
                    parse_mode="Markdown",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 HOME", callback_data="home")]])
                )
            else:
                await query.edit_message_text(
                    "❌ Errore nel caricamento. Controlla credenziali Bring.",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 HOME", callback_data="home")]])
                )
    
    elif data == "reset_bring_credentials":
        delete_bring_credentials(update.effective_user.id)
        await query.answer("✅ Credenziali Bring eliminate! La prossima volta dovrai reinserirle.", show_alert=True)
        await mostra_menu_principale(query)

async def mostra_menu_principale(query):
    """Mostra il menu principale"""
    frase_motivazionale = random.choice(FRASI_MOTIVAZIONALI)
    
    text = f"""
Benvenuta, 🥗 sono il tuo assistente virtuale 🤖 🍽️

{frase_motivazionale}
"""
    keyboard = [
        [
            InlineKeyboardButton("☀️ ESTATE", callback_data="stagione_ESTATE"),
            InlineKeyboardButton("🌱 PRIMAVERA", callback_data="stagione_PRIMAVERA"),
            InlineKeyboardButton("❄️ INVERNO", callback_data="stagione_INVERNO")
        ],
        [
            InlineKeyboardButton("🔍 RICERCA INGREDIENTE", callback_data="ricerca_ingrediente_start"),
            InlineKeyboardButton("✨ CREA SETTIMANA", callback_data="crea_settimana_start")
        ],
        [
            InlineKeyboardButton("🛒 LISTA DELLA SPESA", callback_data="lista_spesa_start"),
            InlineKeyboardButton("📁 LE MIE SETTIMANE", callback_data="mie_settimane_start")
        ],
        [InlineKeyboardButton("🔄 RESETTA BRING", callback_data="reset_bring_credentials")],
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
    
    # Bottone mini app (nuovo!)
    keyboard.append([InlineKeyboardButton(
        "🎨 Seleziona su Web (NUOVO!)", 
        web_app=WebAppInfo(url="https://dieta-bot.up.railway.app/")
    )])
    
    keyboard.append([InlineKeyboardButton("🔽 Oppure scegli da categoria:", callback_data="dummy")])
    
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
    
    # Salva nel database PostgreSQL
    try:
        save_settimana(user_id, nome_settimana, settimana)
    except Exception as e:
        logger.error(f"Errore salva_settimana_con_nome: {e}")
        await update.message.reply_text(f"❌ Errore nel salvataggio: {e}")
        return
    
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
    utente_settimane = get_settimane_utente(user_id)
    
    if not utente_settimane:
        text = "📁 LE MIE SETTIMANE\n\n❌ Non hai ancora salvato nessuna settimana!"
        keyboard = [[InlineKeyboardButton("🏠 HOME", callback_data="home")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)
        return
    
    text = "📁 LE MIE SETTIMANE\n\n"
    keyboard = []
    
    for idx, (nome_settimana, dati) in enumerate(utente_settimane.items()):
        text += f"{idx + 1}. {nome_settimana}\n\n"
        keyboard.append([InlineKeyboardButton(f"📖 Visualizza: {nome_settimana}", callback_data=f"visualizza_settimana_{nome_settimana}")])
    
    keyboard.append([InlineKeyboardButton("🏠 HOME", callback_data="home")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup)

async def visualizza_settimana_salvata(query, user_id, nome_settimana):
    """Visualizza una settimana salvata con bottoni per i giorni"""
    dati_settimana = get_settimana(user_id, nome_settimana)
    
    if not dati_settimana:
        await query.edit_message_text(f"❌ Settimana '{nome_settimana}' non trovata!")
        return
    
    settimana = dati_settimana.get('settimana', {})
    
    if not settimana:
        await query.edit_message_text("❌ Dati settimana non validi!")
        return
    
    text = f"📖 *{nome_settimana}*\n\n*Scegli un giorno:*"
    
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
    
    keyboard.append([InlineKeyboardButton("🗑️ ELIMINA SETTIMANA", callback_data=f"elimina_settimana_{nome_settimana}")])
    keyboard.append([InlineKeyboardButton("🗑️ ELIMINA GIORNO", callback_data=f"elimina_giorno_menu_{nome_settimana}")])
    keyboard.append([InlineKeyboardButton("✅ CHECK OBIETTIVO", callback_data=f"check_obiettivo_{nome_settimana}")])
    keyboard.append([InlineKeyboardButton("⬅️ Indietro", callback_data="mie_settimane_start")])
    keyboard.append([InlineKeyboardButton("🏠 HOME", callback_data="home")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def elimina_settimana_salvata(query, user_id, nome_settimana):
    """Elimina una settimana salvata"""
    try:
        delete_settimana(user_id, nome_settimana)
        await query.edit_message_text(f"✅ Settimana '{nome_settimana}' eliminata!")
        await mostra_mie_settimane(query, user_id)
    except Exception as e:
        logger.error(f"Errore elimina_settimana_salvata: {e}")
        await query.edit_message_text("❌ Errore nell'eliminazione della settimana!")

async def visualizza_giorno_settimana_salvata(query, user_id, nome_settimana, giorno_idx):
    """Visualizza un giorno specifico di una settimana salvata"""
    dati_settimana = get_settimana(user_id, nome_settimana)
    
    if not dati_settimana:
        await query.edit_message_text("❌ Settimana non trovata!")
        return
    
    settimana = dati_settimana.get('settimana', {})
    giorno_data = settimana.get(str(giorno_idx))
    
    if not giorno_data:
        await query.edit_message_text(f"❌ Giorno non trovato!")
        return
    
    giorno_num = int(giorno_idx) + 1
    giorno_nome = giorno_data.get('giorno', 'Sconosciuto')
    
    text = f"📅 *Giorno {giorno_num}: {giorno_nome}*\n\n"
    
    # Ordine corretto dei pasti
    ordine_pasti = ["colazione", "spuntino", "pranzo", "spuntino_2", "cena", "dopo_cena"]
    
    # Mostra il menu con ordine e emoji corretti
    menu = giorno_data.get('menu', {})
    if menu:
        for pasto in ordine_pasti:
            if pasto in menu:
                descrizione = menu.get(pasto, "N/A")
                if isinstance(descrizione, str):
                    emoji = EMOJI_PASTI.get(pasto, "🍽️")
                    pasto_nome = pasto.upper().replace("_", " ")
                    text += f"{emoji} *{pasto_nome}*\n{descrizione}\n\n"
    
    keyboard = [
        [InlineKeyboardButton("⬅️ Indietro", callback_data=f"visualizza_settimana_{nome_settimana}")],
        [InlineKeyboardButton("🏠 HOME", callback_data="home")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def salva_settimana_con_nome_wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Wrapper per gestire il salvataggio, ricerca ingrediente, creazione settimana vuota, o credenziali Bring"""
    if context.user_data.get('in_bring_email'):
        context.user_data['bring_email'] = update.message.text.strip()
        context.user_data['in_bring_email'] = False
        context.user_data['in_bring_password'] = True
        await update.message.reply_text("🔐 *Ora la password:*", parse_mode="Markdown")
    elif context.user_data.get('in_bring_password'):
        context.user_data['bring_password'] = update.message.text.strip()
        context.user_data['in_bring_password'] = False
        
        email = context.user_data.get('bring_email')
        password = context.user_data.get('bring_password')
        nome_lista = context.user_data.get('bring_nome_lista')
        ingredienti = context.user_data.get('bring_ingredienti', [])
        
        await update.message.reply_text("⏳ *Verifico credenziali Bring...*", parse_mode="Markdown")
        bring_lists = await fetch_bring_lists(email, password)
        
        if bring_lists:
            await mostra_liste_bring_da_message(update, context, email, password, nome_lista, ingredienti, bring_lists)
        else:
            await update.message.reply_text(
                "❌ *Credenziali errate!*\n\nRiprova con una nuova email.",
                parse_mode="Markdown"
            )
            context.user_data['in_bring_email'] = True
    elif context.user_data.get('creating_empty_week'):
        await crea_settimana_vuota(update, context)
    elif context.user_data.get('in_salvataggio'):
        await salva_settimana_con_nome(update, context)
    else:
        await cerca_ingrediente(update, context)

# ============================================================
# AGGIUNGI GIORNO A SETTIMANA
# ============================================================

async def aggiungi_giorno_a_settimana_start(query, user_id, stagione, settimana_num, giorno_idx, context):
    """Mostra la lista delle settimane salvate per aggiungere il giorno"""
    # Carica le settimane salvate dell'utente dal database
    user_settimane = get_settimane_utente(user_id)
    
    if not user_settimane:
        text = "❌ *Non hai ancora settimane salvate!*\n\nDevi prima creare una settimana.\n\nScrivi il nome della nuova settimana (es: 'Mia Settimana', 'Pippo', ecc.)"
        keyboard = [[InlineKeyboardButton("🏠 HOME", callback_data="home")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")
        context.user_data['creating_empty_week'] = True
        context.user_data['pending_add_to_week'] = f"{stagione}_{settimana_num}_{giorno_idx}"
        return
    
    # Salva il giorno selezionato in context
    giorno = GIORNI[giorno_idx]
    settimana = f"SETTIMANA_{settimana_num}"
    menu_giorno = MENU[stagione][settimana][giorno]
    
    text = f"*Aggiungi a quale settimana?*\n\nGiorno selezionato: {stagione} - {giorno}\n\n"
    keyboard = []
    
    for nome_settimana in sorted(user_settimane.keys()):
        keyboard.append([InlineKeyboardButton(nome_settimana, 
                                             callback_data=f"select_dest_week_{nome_settimana}#{stagione}_{settimana_num}_{giorno_idx}")])
    
    keyboard.append([InlineKeyboardButton("➕ Crea nuova settimana", callback_data=f"create_new_empty_week#{stagione}_{settimana_num}_{giorno_idx}")])
    keyboard.append([InlineKeyboardButton("⬅️ Indietro", callback_data=f"back_settimane_{stagione}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def select_dest_week(query, context, nome_settimana, stagione, settimana_num, giorno_idx):
    """Mostra lo stato della settimana di destinazione con gli slot vuoti"""
    user_id = query.from_user.id
    
    # Carica le settimane salvate dal database
    user_settimane = get_settimane_utente(user_id)
    settimana_dest_data = user_settimane.get(nome_settimana, {})
    settimana_dest = settimana_dest_data.get('settimana', {})
    
    # Mostra lo stato della settimana con slot vuoti e pieni
    text = f"*Settimana: {nome_settimana}*\n\n"
    text += f"*Aggiungi il giorno:* {GIORNI[giorno_idx]}\n\n"
    
    # Mappa i giorni della settimana salvata
    giorni_occupati = set()
    for idx, giorno_data in settimana_dest.items():
        giorno_nome = giorno_data.get('giorno', '')
        if giorno_nome:
            giorni_occupati.add(giorno_nome)
    
    for i, giorno in enumerate(GIORNI):
        if giorno in giorni_occupati:
            emoji = "✅"
            text += f"{emoji} *{giorno}*: riempito\n"
        else:
            emoji = "⬜"
            text += f"{emoji} *{giorno}*: vuoto\n"
    
    keyboard = []
    # Mostra i pulsanti solo per gli slot vuoti
    row = []
    for i, giorno in enumerate(GIORNI):
        if giorno not in giorni_occupati:
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
    
    # Carica le settimane dal database
    user_settimane = get_settimane_utente(user_id)
    
    # Ottieni il giorno da aggiungere
    giorno_source = GIORNI[giorno_idx]
    settimana_source = f"SETTIMANA_{settimana_num}"
    menu_giorno = MENU[stagione][settimana_source][giorno_source]
    
    # Ottieni il giorno slot dove aggiungere
    giorno_dest = GIORNI[slot_idx]
    
    # Aggiungi il giorno alla settimana di destinazione
    if nome_settimana not in user_settimane:
        user_settimane[nome_settimana] = {'settimana': {}, 'data_creazione': 'N/A'}
    
    settimana_dest = user_settimane[nome_settimana].get('settimana', {})
    settimana_dest[str(slot_idx)] = {
        'giorno': giorno_dest,
        'menu': menu_giorno
    }
    
    # Salva nel database
    save_settimana(user_id, nome_settimana, settimana_dest)
    
    await query.answer(f"✅ {giorno_source} aggiunto a {nome_settimana} come {giorno_dest}!", show_alert=True)
    
    # Mostra di nuovo la settimana
    await select_dest_week(query, context, nome_settimana, stagione, settimana_num, giorno_idx)

async def crea_settimana_vuota(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Crea una nuova settimana vuota con il nome inserito"""
    user_id = update.effective_user.id
    nome_settimana = update.message.text.strip()
    
    if not nome_settimana or len(nome_settimana) < 2:
        await update.message.reply_text("❌ Il nome deve avere almeno 2 caratteri!")
        return
    
    # Carica le settimane dal database
    user_settimane = get_settimane_utente(user_id)
    
    # Verifica se esiste già
    if nome_settimana in user_settimane:
        await update.message.reply_text(f"⚠️ La settimana '{nome_settimana}' esiste già!")
        return
    
    # Crea la nuova settimana vuota nel database
    save_settimana(user_id, nome_settimana, {})
    
    # Se è stato chiamato dal flusso "aggiungi a settimana", torna a quel flusso
    if 'pending_add_to_week' in context.user_data:
        parts = context.user_data['pending_add_to_week'].split('_')
        stagione = parts[0]
        settimana_num = parts[1]
        giorno_idx = int(parts[2])
        
        # Pulisci il context
        context.user_data['creating_empty_week'] = False
        context.user_data.pop('pending_add_to_week', None)
        
        # Crea un oggetto query finto per poter usare select_dest_week
        class FakeQuery:
            def __init__(self, message):
                self.from_user = message.from_user
            
            async def edit_message_text(self, text, reply_markup=None, parse_mode=None):
                await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=parse_mode)
        
        fake_query = FakeQuery(update.message)
        await select_dest_week(fake_query, context, nome_settimana, stagione, settimana_num, giorno_idx)
    else:
        # Se era la prima creazione, torna al menu principale
        context.user_data['creating_empty_week'] = False
        await update.message.reply_text("✅ Settimana creata!")

async def check_obiettivo_settimana(query, user_id, nome_settimana):
    """Controlla se la settimana rispetta gli obiettivi settimanali"""
    # Obiettivi settimanali
    OBIETTIVI = {
        'pesce': 3,
        'uova': 4,
        'legumi': 5,
        'carne bianca': 1,
        'formaggi': (1, 2)  # range 1-2
    }
    
    # Carica ingredienti per categorizzazione
    try:
        with open(SCRIPT_DIR / 'ingredienti_definitivi.json', 'r', encoding='utf-8') as f:
            ingredienti_db = json.load(f)
    except FileNotFoundError:
        await query.answer("❌ File ingredienti non trovato!", show_alert=True)
        return
    
    # Carica settimana dal database
    dati_settimana = get_settimana(user_id, nome_settimana)
    
    if not dati_settimana:
        await query.answer("❌ Settimana non trovata!", show_alert=True)
        return
    
    settimana = dati_settimana.get('settimana', {})
    
    if not settimana:
        await query.answer("❌ Settimana vuota!", show_alert=True)
        return
    
    # Raccogli tutti i piatti della settimana in minuscolo
    testo_settimana = ""
    for idx, giorno_data in settimana.items():
        menu = giorno_data.get('menu', {})
        if menu:
            for pasto, descrizione in menu.items():
                if isinstance(descrizione, str):
                    testo_settimana += descrizione.lower() + " "
    
    # Conta occorrenze e traccia ingredienti trovati
    conteggi = {
        'pesce': 0,
        'uova': 0,
        'legumi': 0,
        'carne bianca': 0,
        'formaggi': 0
    }
    
    ingredienti_trovati = {
        'pesce': [],
        'uova': [],
        'legumi': [],
        'carne bianca': [],
        'formaggi': []
    }
    
    # Conta per pesce (PROTEINE che contengono pesce)
    pesce_items = ['Salmone', 'Branzino', 'Merluzzo', 'Nasello', 'Orata', 'Pesce', 'Pesce spada', 
                   'Polipo', 'Rombo', 'Sardine', 'Sgombro', 'Sogliola', 'Spigola', 'Tonno', 'Trota', 'Acciughe', 'Cernia', 'Dentice']
    for ing in pesce_items:
        count = testo_settimana.count(ing.lower())
        if count > 0:
            conteggi['pesce'] += count
            ingredienti_trovati['pesce'].append(f"{ing} ({count}x)")
    
    # Conta per uova (PROTEINE - uova)
    for keyword in ['uova', 'frittata']:
        count = testo_settimana.count(keyword)
        if count > 0:
            conteggi['uova'] += count
            ingredienti_trovati['uova'].append(f"{keyword.capitalize()} ({count}x)")
    
    # Conta per legumi (CARBOIDRATI - legumi)
    legumi_items = ['Ceci', 'Fagioli', 'Lenticchie']
    for ing in legumi_items:
        count = testo_settimana.count(ing.lower())
        if count > 0:
            conteggi['legumi'] += count
            ingredienti_trovati['legumi'].append(f"{ing} ({count}x)")
    
    # Conta per carne bianca (PROTEINE - pollo, tacchino, coniglio)
    carne_bianca_items = ['Pollo', 'Tacchino', 'Coniglio']
    for ing in carne_bianca_items:
        count = testo_settimana.count(ing.lower())
        if count > 0:
            conteggi['carne bianca'] += count
            ingredienti_trovati['carne bianca'].append(f"{ing} ({count}x)")
    
    # Conta per formaggi (LATTICINI)
    for ing in ingredienti_db.get('🧀 LATTICINI', []):
        count = testo_settimana.count(ing.lower())
        if count > 0:
            conteggi['formaggi'] += count
            ingredienti_trovati['formaggi'].append(f"{ing} ({count}x)")
    
    # Genera report
    text = f"📊 *REPORT OBIETTIVI - {nome_settimana}*\n\n"
    
    for categoria, target in OBIETTIVI.items():
        conteggio = conteggi[categoria]
        trovati = ingredienti_trovati[categoria]
        
        if isinstance(target, tuple):
            # Range (es: formaggi 1-2)
            min_target, max_target = target
            if min_target <= conteggio <= max_target:
                emoji = "✅"
                status = f"{conteggio} ({min_target}-{max_target})"
            else:
                emoji = "❌"
                status = f"{conteggio} ({min_target}-{max_target})"
        else:
            # Valore fisso
            if conteggio >= target:
                emoji = "✅"
            else:
                emoji = "❌"
            status = f"{conteggio}/{target}"
        
        text += f"{emoji} *{categoria.upper()}*: {status}\n"
        if trovati:
            text += f"   {', '.join(trovati)}\n"
        text += "\n"
    
    keyboard = [[InlineKeyboardButton("⬅️ Indietro", callback_data=f"visualizza_settimana_{nome_settimana}")],
               [InlineKeyboardButton("🏠 HOME", callback_data="home")]]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def mostra_menu_elimina_giorno(query, user_id, nome_settimana):
    """Mostra il menu per scegliere quale giorno eliminare"""
    dati_settimana = get_settimana(user_id, nome_settimana)
    
    if not dati_settimana:
        await query.answer("❌ Settimana non trovata!", show_alert=True)
        return
    
    settimana = dati_settimana.get('settimana', {})
    
    if not settimana:
        await query.answer("❌ Settimana vuota!", show_alert=True)
        return
    
    text = f"*Elimina quale giorno?*\n\n"
    keyboard = []
    
    for idx in sorted([int(i) for i in settimana.keys()]):
        giorno_data = settimana[str(idx)]
        giorno_nome = giorno_data.get('giorno', 'Giorno sconosciuto')
        
        keyboard.append([InlineKeyboardButton(
            f"🗑️ {giorno_nome}",
            callback_data=f"elimina_giorno_{nome_settimana}#{idx}"
        )])
    
    keyboard.append([InlineKeyboardButton("⬅️ Indietro", callback_data=f"visualizza_settimana_{nome_settimana}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def elimina_giorno_da_settimana(query, user_id, nome_settimana, giorno_idx):
    """Elimina un giorno specifico dalla settimana"""
    dati_settimana = get_settimana(user_id, nome_settimana)
    
    if not dati_settimana:
        await query.answer("❌ Settimana non trovata!", show_alert=True)
        return
    
    settimana = dati_settimana.get('settimana', {})
    
    if str(giorno_idx) not in settimana:
        await query.answer("❌ Giorno non trovato!", show_alert=True)
        return
    
    # Ottieni il nome del giorno da eliminare
    giorno_nome = settimana[str(giorno_idx)].get('giorno', 'Giorno')
    
    # Elimina il giorno
    del settimana[str(giorno_idx)]
    
    # Salva nel database
    save_settimana(user_id, nome_settimana, settimana)
    
    await query.answer(f"✅ {giorno_nome} eliminato!", show_alert=True)
    
    # Torna al menu della settimana
    await visualizza_settimana_salvata(query, user_id, nome_settimana)

# ============================================================
# LISTA DELLA SPESA
# ============================================================

async def mostra_liste_spesa_utente(query, user_id):
    """Mostra il menu principale della lista della spesa"""
    liste_salvate = get_liste_spesa_utente(user_id)
    
    text = "🛒 *LISTA DELLA SPESA*\n\n"
    keyboard = []
    
    if liste_salvate:
        text += "*Tue liste salvate:*\n\n"
        for nome_lista in sorted(liste_salvate.keys()):
            keyboard.append([InlineKeyboardButton(f"📋 {nome_lista}", callback_data=f"visualizza_lista_spesa_{nome_lista}")])
        text += f"Hai {len(liste_salvate)} list{'a' if len(liste_salvate) == 1 else 'e'} salvata{'e' if len(liste_salvate) != 1 else ''}.\n\n"
    else:
        text += "Non hai ancora liste della spesa.\n\n"
    
    text += "*Crea una nuova lista da settimane predefinite:*\n"
    keyboard.append([
        InlineKeyboardButton("☀️ ESTATE", callback_data="crea_lista_spesa_ESTATE"),
        InlineKeyboardButton("🌱 PRIMAVERA", callback_data="crea_lista_spesa_PRIMAVERA"),
        InlineKeyboardButton("❄️ INVERNO", callback_data="crea_lista_spesa_INVERNO")
    ])
    
    text += "\n*Oppure da settimane salvate:*\n"
    keyboard.append([InlineKeyboardButton("📁 Da settimana salvata", callback_data="lista_spesa_da_salvata")])
    keyboard.append([InlineKeyboardButton("🏠 HOME", callback_data="home")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def mostra_settimane_per_lista(query, user_id, stagione):
    """Mostra le settimane della stagione per creare lista"""
    text = f"*Scegli una settimana da {stagione}:*\n\n"
    keyboard = []
    
    settimane_disponibili = MENU.get(stagione, {})
    for settimana_key in sorted(settimane_disponibili.keys()):
        settimana_num = settimana_key.split("_")[1]
        keyboard.append([InlineKeyboardButton(f"Settimana {settimana_num}", callback_data=f"salva_lista_spesa_{stagione}_{settimana_num}")])
    
    keyboard.append([InlineKeyboardButton("⬅️ Indietro", callback_data="lista_spesa_start")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def mostra_giorni_per_lista(query, user_id, stagione, settimana_num):
    """Mostra i 7 giorni della settimana per selezionare quale giorno"""
    text = f"*{stagione} - Settimana {settimana_num}*\n\n"
    text += "Seleziona il giorno per vedere la lista della spesa:\n\n"
    
    keyboard = []
    for giorno in GIORNI:
        giorno_display = giorno.capitalize()
        keyboard.append([InlineKeyboardButton(f"📅 {giorno_display}", callback_data=f"lista_giorno_{stagione}_{settimana_num}_{giorno}")])
    
    keyboard.append([InlineKeyboardButton("⬅️ Indietro", callback_data="lista_spesa_start")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def mostra_lista_giorno_spesa(query, user_id, stagione, settimana_num, giorno, context):
    """Estrae ingredienti solo del giorno selezionato e mostra lista"""
    settimana_key = f"SETTIMANA_{settimana_num}"
    settimana_data = MENU.get(stagione, {}).get(settimana_key, {})
    menu_giorno = settimana_data.get(giorno, {})
    
    if not menu_giorno:
        await query.answer("❌ Giorno non trovato!", show_alert=True)
        return
    
    # Carica ingredienti da categorizzare
    try:
        with open(SCRIPT_DIR / 'ingredienti_definitivi.json', 'r', encoding='utf-8') as f:
            ingredienti_db = json.load(f)
    except FileNotFoundError:
        await query.answer("❌ File ingredienti non trovato!", show_alert=True)
        return
    
    # Crea mappa di ingredienti per ricerca veloce
    ingredienti_map = {}
    for categoria, items in ingredienti_db.items():
        for item in items:
            ingredienti_map[item.lower()] = categoria
    
    # Estrai ingredienti SOLO di questo giorno
    ingredienti_contati = {}  # {categoria: {ingrediente: count}}
    
    for pasto, descrizione in menu_giorno.items():
        if isinstance(descrizione, str):
            componenti = descrizione.lower().replace(' con ', ',').replace(' e ', ',').split(',')
            
            for componente in componenti:
                componente = componente.strip()
                ingredienti_ordinati = sorted(ingredienti_map.keys(), key=len, reverse=True)
                
                for ingrediente_nome in ingredienti_ordinati:
                    if ingrediente_nome in componente:
                        categoria = ingredienti_map[ingrediente_nome]
                        
                        if categoria not in ingredienti_contati:
                            ingredienti_contati[categoria] = {}
                        
                        ing_display = next(
                            (item for item in ingredienti_db[categoria] if item.lower() == ingrediente_nome),
                            ingrediente_nome.capitalize()
                        )
                        
                        if ing_display not in ingredienti_contati[categoria]:
                            ingredienti_contati[categoria][ing_display] = 0
                        ingredienti_contati[categoria][ing_display] += 1
                        break
    
    # Costruisci dict finale
    ingredienti_dict = {}
    idx = 0
    for categoria in sorted(ingredienti_contati.keys()):
        for ingrediente, count in sorted(ingredienti_contati[categoria].items()):
            display = f"{ingrediente} (x{count})" if count > 1 else ingrediente
            ingredienti_dict[idx] = {
                'nome': display,
                'categoria': categoria,
                'spuntato': False
            }
            idx += 1
    
    # Salva con nome che include il giorno
    nome_lista = f"{stagione} S{settimana_num} - {giorno.capitalize()}"
    save_lista_spesa(user_id, nome_lista, stagione, settimana_num, ingredienti_dict)
    
    # Salva in context
    ingredienti_lista = [ing_data['nome'] for ing_data in ingredienti_dict.values()]
    context.user_data[f'lista_ingredienti_{nome_lista}'] = ingredienti_lista
    context.user_data['current_giorno_lista'] = giorno
    
    await query.answer(f"✅ Lista di {giorno.capitalize()} caricata!", show_alert=False)
    await visualizza_lista_spesa(query, user_id, nome_lista, context)

async def salva_lista_spesa_da_settimana(query, user_id, stagione, settimana_num, context):
    """Estrae ingredienti intelligenti da una settimana e crea una lista categorizzata"""
    settimana_key = f"SETTIMANA_{settimana_num}"
    settimana_data = MENU.get(stagione, {}).get(settimana_key, {})
    
    if not settimana_data:
        await query.answer("❌ Settimana non trovata!", show_alert=True)
        return
    
    # Carica ingredienti da categorizzare
    try:
        with open(SCRIPT_DIR / 'ingredienti_definitivi.json', 'r', encoding='utf-8') as f:
            ingredienti_db = json.load(f)
    except FileNotFoundError:
        await query.answer("❌ File ingredienti non trovato!", show_alert=True)
        return
    
    # Crea mappa di ingredienti per ricerca veloce (categoria → lista ingredienti lowercase)
    ingredienti_map = {}
    for categoria, items in ingredienti_db.items():
        for item in items:
            ingredienti_map[item.lower()] = categoria
    
    # Estrai ingredienti dalla settimana
    ingredienti_contati = {}  # {categoria: {ingrediente: count}}
    
    for giorno in GIORNI:
        menu_giorno = settimana_data.get(giorno, {})
        for pasto, descrizione in menu_giorno.items():
            if isinstance(descrizione, str):
                # Splitti intelligente: per virgole e "con"
                componenti = descrizione.lower().replace(' con ', ',').replace(' e ', ',').split(',')
                
                for componente in componenti:
                    componente = componente.strip()
                    
                    # Cerca ingredienti noti in questo componente
                    # Ordina per lunghezza decrescente per evitare match parziali
                    ingredienti_ordinati = sorted(ingredienti_map.keys(), key=len, reverse=True)
                    
                    for ingrediente_nome in ingredienti_ordinati:
                        # Match esatto di parola (non substring)
                        if ingrediente_nome in componente:
                            categoria = ingredienti_map[ingrediente_nome]
                            
                            if categoria not in ingredienti_contati:
                                ingredienti_contati[categoria] = {}
                            
                            # Capitalizza per display
                            ing_display = next(
                                (item for item in ingredienti_db[categoria] if item.lower() == ingrediente_nome),
                                ingrediente_nome.capitalize()
                            )
                            
                            if ing_display not in ingredienti_contati[categoria]:
                                ingredienti_contati[categoria][ing_display] = 0
                            ingredienti_contati[categoria][ing_display] += 1
                            break  # Prendi il primo match in questo componente
    
    # Costruisci dict finale con categoria e conteggio
    ingredienti_dict = {}
    idx = 0
    for categoria in sorted(ingredienti_contati.keys()):
        for ingrediente, count in sorted(ingredienti_contati[categoria].items()):
            display = f"{ingrediente} (x{count})" if count > 1 else ingrediente
            ingredienti_dict[idx] = {
                'nome': display,
                'categoria': categoria,
                'spuntato': False
            }
            idx += 1
    
    # Salva con nome auto-generato
    nome_lista = f"{stagione} S{settimana_num}"
    save_lista_spesa(user_id, nome_lista, stagione, settimana_num, ingredienti_dict)
    
    # Salva ingredienti in context per eventuale upload su Bring
    ingredienti_lista = [ing_data['nome'] for ing_data in ingredienti_dict.values()]
    context.user_data[f'lista_ingredienti_{nome_lista}'] = ingredienti_lista
    
    await query.answer(f"✅ Lista '{nome_lista}' creata con {len(ingredienti_dict)} ingredienti!", show_alert=True)
    await visualizza_lista_spesa(query, user_id, nome_lista, context)

async def visualizza_lista_spesa(query, user_id, nome_lista, context=None):
    """Visualizza una lista della spesa categorizzata con checkbox deflaggabili"""
    dati_lista = get_lista_spesa(user_id, nome_lista)
    
    # Salva nome_lista in context per Bring
    if context:
        context.user_data['current_lista_spesa'] = nome_lista
    
    if not dati_lista:
        await query.answer("❌ Lista non trovata!", show_alert=True)
        return
    
    ingredienti = dati_lista.get('ingredienti', {})
    
    text = f"🛒 *{nome_lista}*\n\n"
    non_spuntati = len([i for i in ingredienti.values() if not i.get('spuntato', False)])
    text += f"*Ingredienti ({non_spuntati}/{len(ingredienti)}):*\n\n"
    
    keyboard = []
    
    # Raggruppa per categoria
    categorie_ordinata = {}
    for idx, ing_data in sorted(ingredienti.items(), key=lambda x: int(x[0])):
        categoria = ing_data.get('categoria', '❓ ALTRO')
        if categoria not in categorie_ordinata:
            categorie_ordinata[categoria] = []
        categorie_ordinata[categoria].append((idx, ing_data))
    
    # Mostra ingredienti per categoria
    for categoria in sorted(categorie_ordinata.keys()):
        text += f"*{categoria}*\n"
        for idx, ing_data in categorie_ordinata[categoria]:
            nome = ing_data.get('nome', 'Ingrediente')
            spuntato = ing_data.get('spuntato', False)
            emoji = "✅" if spuntato else "⬜"
            
            text += f"{emoji} {nome}\n"
            keyboard.append([InlineKeyboardButton(f"{'✅' if spuntato else '⬜'} {nome}", callback_data=f"toggle_lista_ing_{nome_lista}_{idx}")])
        
        text += "\n"
    
    keyboard.append([InlineKeyboardButton("🗑️ ELIMINA", callback_data=f"elimina_lista_spesa_{nome_lista}")])
    keyboard.append([InlineKeyboardButton("📤 INVIA A BRING", callback_data=f"bring_start_lista_{nome_lista}")])
    keyboard.append([InlineKeyboardButton("⬅️ Indietro", callback_data="lista_spesa_start")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def toggle_ingrediente_lista(query, user_id, nome_lista, ing_idx, context=None):
    """Toggle lo stato di un ingrediente (spuntato/non spuntato)"""
    dati_lista = get_lista_spesa(user_id, nome_lista)
    
    if not dati_lista:
        await query.answer("❌ Lista non trovata!", show_alert=True)
        return
    
    ingredienti = dati_lista.get('ingredienti', {})
    ing_idx_str = str(ing_idx)
    
    if ing_idx_str in ingredienti:
        ingredienti[ing_idx_str]['spuntato'] = not ingredienti[ing_idx_str].get('spuntato', False)
        save_lista_spesa(user_id, nome_lista, dati_lista['stagione'], dati_lista['settimana_num'], ingredienti)
    
    await visualizza_lista_spesa(query, user_id, nome_lista, context)

async def mostra_settimane_salvate_per_lista(query, user_id):
    """Mostra le settimane salvate per crearne una lista"""
    settimane_utente = get_settimane_utente(user_id)
    
    text = "*Scegli una settimana salvata:*\n\n"
    keyboard = []
    
    if not settimane_utente:
        text = "❌ Non hai ancora settimane salvate!"
        keyboard.append([InlineKeyboardButton("⬅️ Indietro", callback_data="lista_spesa_start")])
    else:
        for nome_settimana in sorted(settimane_utente.keys()):
            keyboard.append([InlineKeyboardButton(f"📋 {nome_settimana}", callback_data=f"lista_spesa_da_salvata_{nome_settimana}")])
        keyboard.append([InlineKeyboardButton("⬅️ Indietro", callback_data="lista_spesa_start")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def mostra_giorni_settimana_salvata_per_lista(query, user_id, nome_settimana):
    """Mostra i giorni di una settimana salvata per scegliere quale giorno usare per la lista"""
    dati_settimana = get_settimana(user_id, nome_settimana)
    
    if not dati_settimana:
        await query.answer("❌ Settimana non trovata!", show_alert=True)
        return
    
    settimana = dati_settimana.get('settimana', {})
    
    if not settimana:
        await query.edit_message_text("❌ Dati settimana non validi!")
        return
    
    text = f"📖 *{nome_settimana}*\n\n*Scegli un giorno:*"
    
    keyboard = []
    
    # Crea bottoni per ogni giorno
    for idx in sorted([int(i) for i in settimana.keys()]):
        giorno_data = settimana[str(idx)]
        giorno_num = idx + 1
        giorno_nome = giorno_data.get('giorno', 'Giorno sconosciuto')
        
        keyboard.append([InlineKeyboardButton(
            f"📅 Giorno {giorno_num}: {giorno_nome}",
            callback_data=f"lista_spesa_giorno_salvato_{nome_settimana}#{idx}"
        )])
    
    keyboard.append([InlineKeyboardButton("⬅️ Indietro", callback_data="lista_spesa_da_salvata")])
    keyboard.append([InlineKeyboardButton("🏠 HOME", callback_data="home")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def salva_lista_spesa_da_giorno_salvato(query, user_id, nome_settimana, giorno_idx, context):
    """Estrae ingredienti da un giorno specifico della settimana salvata e crea una lista"""
    dati_settimana = get_settimana(user_id, nome_settimana)
    
    if not dati_settimana:
        await query.answer("❌ Settimana non trovata!", show_alert=True)
        return
    
    settimana = dati_settimana.get('settimana', {})
    giorno_data = settimana.get(str(giorno_idx), {})
    
    if not giorno_data:
        await query.answer("❌ Giorno non trovato!", show_alert=True)
        return
    
    # Carica ingredienti da categorizzare
    try:
        with open(SCRIPT_DIR / 'ingredienti_definitivi.json', 'r', encoding='utf-8') as f:
            ingredienti_db = json.load(f)
    except FileNotFoundError:
        await query.answer("❌ File ingredienti non trovato!", show_alert=True)
        return
    
    # Crea mappa di ingredienti per ricerca veloce
    ingredienti_map = {}
    for categoria, items in ingredienti_db.items():
        for item in items:
            ingredienti_map[item.lower()] = categoria
    
    # Estrai ingredienti dal giorno selezionato
    ingredienti_contati = {}  # {categoria: {ingrediente: count}}
    
    menu = giorno_data.get('menu', {})
    for pasto, descrizione in menu.items():
        if isinstance(descrizione, str):
            # Splitti intelligente: per virgole e "con"
            componenti = descrizione.lower().replace(' con ', ',').replace(' e ', ',').split(',')
            
            for componente in componenti:
                componente = componente.strip()
                
                # Cerca ingredienti noti in questo componente
                ingredienti_ordinati = sorted(ingredienti_map.keys(), key=len, reverse=True)
                
                for ingrediente_nome in ingredienti_ordinati:
                    if ingrediente_nome in componente:
                        categoria = ingredienti_map[ingrediente_nome]
                        
                        if categoria not in ingredienti_contati:
                            ingredienti_contati[categoria] = {}
                        
                        # Capitalizza per display
                        ing_display = next(
                            (item for item in ingredienti_db[categoria] if item.lower() == ingrediente_nome),
                            ingrediente_nome.capitalize()
                        )
                        
                        if ing_display not in ingredienti_contati[categoria]:
                            ingredienti_contati[categoria][ing_display] = 0
                        ingredienti_contati[categoria][ing_display] += 1
                        break  # Prendi il primo match in questo componente
    
    # Costruisci dict finale
    ingredienti_dict = {}
    idx = 0
    for categoria in sorted(ingredienti_contati.keys()):
        for ingrediente, count in sorted(ingredienti_contati[categoria].items()):
            display = f"{ingrediente} (x{count})" if count > 1 else ingrediente
            ingredienti_dict[idx] = {
                'nome': display,
                'categoria': categoria,
                'spuntato': False
            }
            idx += 1
    
    # Salva con nome specifico
    giorno_nome = giorno_data.get('giorno', 'Giorno')
    nome_lista_spesa = f"Lista - {nome_settimana} - {giorno_nome}"
    save_lista_spesa(user_id, nome_lista_spesa, "SALVATA", 0, ingredienti_dict)
    
    # Salva ingredienti in context per eventuale upload su Bring
    ingredienti_lista = [ing_data['nome'] for ing_data in ingredienti_dict.values()]
    context.user_data[f'lista_ingredienti_{nome_lista_spesa}'] = ingredienti_lista
    
    await query.answer(f"✅ Lista '{nome_lista_spesa}' creata con {len(ingredienti_dict)} ingredienti!", show_alert=True)
    await visualizza_lista_spesa(query, user_id, nome_lista_spesa)

async def salva_lista_spesa_da_settimana_salvata(query, user_id, nome_settimana, context):
    """Estrae ingredienti dalla settimana salvata e crea una lista"""
    dati_settimana = get_settimana(user_id, nome_settimana)
    
    if not dati_settimana:
        await query.answer("❌ Settimana non trovata!", show_alert=True)
        return
    
    # Carica ingredienti da categorizzare
    try:
        with open(SCRIPT_DIR / 'ingredienti_definitivi.json', 'r', encoding='utf-8') as f:
            ingredienti_db = json.load(f)
    except FileNotFoundError:
        await query.answer("❌ File ingredienti non trovato!", show_alert=True)
        return
    
    # Crea mappa di ingredienti per ricerca veloce
    ingredienti_map = {}
    for categoria, items in ingredienti_db.items():
        for item in items:
            ingredienti_map[item.lower()] = categoria
    
    # Estrai ingredienti dalla settimana salvata
    ingredienti_contati = {}  # {categoria: {ingrediente: count}}
    
    settimana = dati_settimana.get('settimana', {})
    for slot_idx, giorno_data in settimana.items():
        menu = giorno_data.get('menu', {})
        for pasto, descrizione in menu.items():
            if isinstance(descrizione, str):
                # Splitti intelligente: per virgole e "con"
                componenti = descrizione.lower().replace(' con ', ',').replace(' e ', ',').split(',')
                
                for componente in componenti:
                    componente = componente.strip()
                    
                    # Cerca ingredienti noti in questo componente
                    ingredienti_ordinati = sorted(ingredienti_map.keys(), key=len, reverse=True)
                    
                    for ingrediente_nome in ingredienti_ordinati:
                        if ingrediente_nome in componente:
                            categoria = ingredienti_map[ingrediente_nome]
                            
                            if categoria not in ingredienti_contati:
                                ingredienti_contati[categoria] = {}
                            
                            # Capitalizza per display
                            ing_display = next(
                                (item for item in ingredienti_db[categoria] if item.lower() == ingrediente_nome),
                                ingrediente_nome.capitalize()
                            )
                            
                            if ing_display not in ingredienti_contati[categoria]:
                                ingredienti_contati[categoria][ing_display] = 0
                            ingredienti_contati[categoria][ing_display] += 1
                            break  # Prendi il primo match in questo componente
    
    # Costruisci dict finale
    ingredienti_dict = {}
    idx = 0
    for categoria in sorted(ingredienti_contati.keys()):
        for ingrediente, count in sorted(ingredienti_contati[categoria].items()):
            display = f"{ingrediente} (x{count})" if count > 1 else ingrediente
            ingredienti_dict[idx] = {
                'nome': display,
                'categoria': categoria,
                'spuntato': False
            }
            idx += 1
    
    # Salva con nome specifico
    nome_lista_spesa = f"Lista - {nome_settimana}"
    save_lista_spesa(user_id, nome_lista_spesa, "SALVATA", 0, ingredienti_dict)
    
    # Salva ingredienti in context per eventuale upload su Bring
    ingredienti_lista = [ing_data['nome'] for ing_data in ingredienti_dict.values()]
    context.user_data[f'lista_ingredienti_{nome_lista_spesa}'] = ingredienti_lista
    
    await query.answer(f"✅ Lista '{nome_lista_spesa}' creata con {len(ingredienti_dict)} ingredienti!", show_alert=True)
    await visualizza_lista_spesa(query, user_id, nome_lista_spesa, context)

# ============================================================
# BRING INTEGRATION - UI FUNCTIONS
# ============================================================

async def mostra_liste_bring(query, user_id, nome_lista, ingredienti, context):
    """Mostra le liste Bring disponibili per upload"""
    email = context.user_data.get('bring_email')
    password = context.user_data.get('bring_password')
    
    bring_lists = await fetch_bring_lists(email, password)
    
    if not bring_lists:
        await query.edit_message_text(
            "❌ *Nessuna lista trovata su Bring*\n\n"
            "Crea una lista su https://web.getbring.com e riprova.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 HOME", callback_data="home")]])
        )
        return
    
    text = f"*📱 Seleziona lista Bring*\n\n"
    text += f"Ingredienti da caricare: {len(ingredienti)}\n\n"
    
    keyboard = []
    # Salva mappa UUID -> nome per recuperare dopo
    bring_uuid_to_name = {}
    for bring_list in bring_lists:
        bring_uuid_to_name[bring_list['listUuid']] = bring_list['name']
        keyboard.append([
            InlineKeyboardButton(
                f"📋 {bring_list['name']}", 
                callback_data=f"bring_upload_{bring_list['listUuid']}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton("🏠 HOME", callback_data="home")])
    
    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    # Salva in context
    context.user_data['bring_nome_lista'] = nome_lista
    context.user_data['bring_ingredienti'] = ingredienti
    context.user_data['bring_uuid_to_name'] = bring_uuid_to_name  # Mappa per recuperare nomi

async def mostra_liste_bring_da_message(update, context, email, password, nome_lista, ingredienti, bring_lists):
    """Mostra le liste Bring quando richiesto via message handler"""
    if not bring_lists:
        await update.message.reply_text(
            "❌ *Nessuna lista trovata su Bring*\n\n"
            "Crea una lista su https://web.getbring.com e riprova.",
            parse_mode="Markdown"
        )
        return
    
    text = f"*📱 Seleziona lista Bring per caricamento*\n\n"
    text += f"Ingredienti da caricare: {len(ingredienti)}\n\n"
    
    keyboard = []
    for bring_list in bring_lists:
        keyboard.append([
            InlineKeyboardButton(
                f"📋 {bring_list['name']}", 
                callback_data=f"bring_upload_{bring_list['listUuid']}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton("🏠 HOME", callback_data="home")])
    
    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    context.user_data['bring_lista_name_target'] = bring_lists[0]['name'] if bring_lists else 'Bring'

# ============================================================
# MAIN
# ============================================================

def main():
    """Avvia il bot"""
    TOKEN = os.getenv("TOKEN")
    
    if not TOKEN:
        print("❌ ERRORE: Variabile TOKEN non trovata!")
        return
    
    # Inizializza il database
    init_db()
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, salva_settimana_con_nome_wrapper))
    
    print("🚀 Bot avviato! Premi Ctrl+C per fermare.")
    app.run_polling()

if __name__ == "__main__":
    main()
