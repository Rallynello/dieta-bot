# 🥗 BOT TELEGRAM GESTIONE DIETA

Un bot Telegram intelligente per visualizzare il tuo menu settimanale giorno per giorno con ricerca ingredienti!

## 📋 Funzionalità

- 📅 Visualizza il menu di 4 settimane
- 🍽️ Mostra colazione, pranzo, cena e spuntini per ogni giorno
- ⬅️ ➡️ Naviga facilmente tra i giorni
- 🔍 **NUOVA!** Ricerca ingredienti - Digita qualsiasi ingrediente (es: "pollo", "pesce", "avocado") e il bot ti mostra dove appare!
- 🎯 Interfaccia intuitiva con bottoni inline

## 🚀 Come Usare

### 1. Ottieni un Token Telegram

1. Apri Telegram e cerca `@BotFather`
2. Scrivi `/newbot` e segui le istruzioni
3. Copia il token ricevuto (sarà qualcosa come `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

### 2. Configura il Bot

Apri `dieta_bot.py` e sostituisci:
```python
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
```
con il tuo token reale:
```python
TOKEN = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
```

### 3. Avvia il Bot

```bash
python dieta_bot.py
```

Vedrai:
```
🚀 Bot avviato! Premi Ctrl+C per fermare.
```

### 4. Usa il Bot

Su Telegram:
1. Cerca il tuo bot (@tuonome_bot)
2. Scrivi `/start`
3. Scegli una settimana
4. Scegli un giorno
5. Visualizza il menu!

## 📝 Comandi

- `/start` - Menu principale
- `/help` - Lista comandi
- Digita qualsiasi ingrediente per cercarlo nel menu

## 🔍 Ricerca Ingredienti

Una delle funzioni più utili! Semplicemente digita quello che cerchi:

- Scrivi `pollo` → Vedi tutti i giorni dove c'è il pollo
- Scrivi `pesce` → Vedi tutti i giorni dove c'è il pesce  
- Scrivi `riso` → Vedi tutte le ricette con il riso
- Scrivi `avocado` → Vedi dove usare l'avocado
- Scrivi `salmone` → Vedi tutte le preparazioni con salmone

Il bot mostra:
- 📅 La settimana
- 📆 Il giorno
- 🍽️ Il pasto (colazione, pranzo, cena, spuntino)
- 📝 La ricetta completa

## 📊 Menu Disponibile

Il file `menu_settimanale.json` contiene il menu DETTAGLIATO per 4 settimane con:
- Quantità in grammi
- Ingredienti specifici
- Metodi di preparazione
- Spezie e condimenti

**Per modificare il menu:**

Modifica il file `estrai_menu_da_pdf.py` aggiornando il dizionario `MENU_SETTIMANALE`, quindi esegui:
```bash
python estrai_menu_da_pdf.py
```

Esempio formato menu:
```json
{
  "SETTIMANA_1": {
    "LUNEDI": {
      "colazione": "Descrizione colazione",
      "spuntino_1": "Descrizione spuntino mattina",
      "pranzo": "Descrizione pranzo",
      "spuntino_2": "Descrizione spuntino pomeriggio",
      "cena": "Descrizione cena",
      "dopo_cena": "Dessert facoltativo"
    },
    ...
  }
}
```

## 🛠️ Requisiti

- Python 3.7+
- `python-telegram-bot`

Installati con:
```bash
pip install python-telegram-bot
```

## 📁 File Importanti

- `dieta_bot.py` - Il bot principale
- `menu_settimanale.json` - Menu settimanale (generato automaticamente)
- `estrai_menu_da_pdf.py` - Script per generare/modificare il menu

## 💡 Tips

- Puoi lasciare il bot in esecuzione sempre (se su un server)
- Per fermare il bot: `Ctrl+C`
- La ricerca ingredienti è case-insensitive (minuscolo/maiuscolo non importa)
- La ricerca trova anche parole parziali (es: scrivi "ranu" e troverà anche "gamberetti")

---

**Buon appetito! 🍴**
