// Dati degli ingredienti (di default)
const ingredientiData = {
    "FRUTTA": ["Mela", "Banana", "Arancia", "Fragola", "Melone"],
    "VERDURA": ["Insalata", "Pomodoro", "Carota", "Broccoli", "Spinaci"],
    "PESCE": ["Salmone", "Merluzzo", "Orata", "Sardine", "Tonno"],
    "CARNE": ["Pollo", "Tacchino", "Manzo", "Vitello", "Maiale"],
    "LEGUMI": ["Lenticchie", "Ceci", "Fagioli", "Piselli", "Fave"],
    "CEREALI": ["Riso", "Pasta", "Pane", "Avena", "Farro"],
    "LATTICINI": ["Latte", "Yogurt", "Formaggio", "Ricotta", "Mozzarella"],
    "UOVA": ["Uova intere", "Albume", "Tuorlo"]
};

// Stato della selezione
let selection = {};

// Inizializzazione
window.addEventListener('load', () => {
    const webApp = window.Telegram.WebApp;
    webApp.ready();
    
    // Abilita il MainButton
    webApp.MainButton.text = "Salva Selezione";
    webApp.MainButton.onClick(() => saveSelection());
    
    renderIngredients();
});

// Renderizza gli ingredienti
function renderIngredients() {
    const content = document.getElementById('content');
    let html = '';
    
    for (const [categoria, ingredienti] of Object.entries(ingredientiData)) {
        html += `<div class="category">`;
        html += `<div class="category-title">${categoria}</div>`;
        
        for (const ing of ingredienti) {
            const id = `${categoria}_${ing}`;
            const checked = selection[id] ? 'checked' : '';
            const qty = selection[id] || 0;
            
            html += `
                <div class="ingredient-item">
                    <input type="checkbox" id="${id}" ${checked} 
                           onchange="updateSelection('${id}')">
                    <label class="ingredient-label" for="${id}">${ing}</label>
                    <div class="quantity-controls">
                        <button onclick="changeQty('${id}', -1)">−</button>
                        <div class="quantity-display">${qty}</div>
                        <button onclick="changeQty('${id}', 1)">+</button>
                    </div>
                </div>
            `;
        }
        
        html += `</div>`;
    }
    
    content.innerHTML = html;
}

// Aggiorna selezione
function updateSelection(id) {
    const checkbox = document.getElementById(id);
    if (checkbox.checked) {
        if (!selection[id]) selection[id] = 1;
    } else {
        delete selection[id];
    }
    renderIngredients();
}

// Cambia quantità
function changeQty(id, delta) {
    if (!selection[id]) selection[id] = 1;
    selection[id] = Math.max(1, selection[id] + delta);
    renderIngredients();
}

// Salva la selezione
function saveSelection() {
    const webApp = window.Telegram.WebApp;
    
    // Converti la selezione in formato leggibile
    const ingredienti = [];
    for (const [id, qty] of Object.entries(selection)) {
        const parts = id.split('_');
        const categoria = parts[0];
        const nome = parts.slice(1).join('_');
        for (let i = 0; i < qty; i++) {
            ingredienti.push(nome);
        }
    }
    
    if (ingredienti.length === 0) {
        alert('Seleziona almeno un ingrediente!');
        return;
    }
    
    // Invia i dati al bot
    webApp.sendData(JSON.stringify({
        type: 'ingredienti_selected',
        ingredienti: ingredienti,
        count: ingredienti.length
    }));
}

// Annulla
function cancelSelection() {
    const webApp = window.Telegram.WebApp;
    webApp.close();
}
