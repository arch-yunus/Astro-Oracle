/* Astro-Oracle 3.0: Frontend Logic */

const API_BASE = "http://localhost:8000/api/v1";

// Planet list for dynamic inputs
const planets = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"];

document.addEventListener('DOMContentLoaded', () => {
    initPlanetInputs();
    
    // Event Listeners
    document.getElementById('interpret-btn').addEventListener('click', interpretNatal);
    document.getElementById('send-btn').addEventListener('click', sendAgentQuery);
    document.getElementById('agent-query').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendAgentQuery();
    });
});

function initPlanetInputs() {
    const container = document.getElementById('planet-inputs');
    planets.forEach(planet => {
        const div = document.createElement('div');
        div.className = 'input-group';
        div.innerHTML = `
            <label>${planet}</label>
            <div style="display: flex; gap: 0.5rem;">
                <select id="${planet}-sign">
                    <option value="Aries">Koç</option>
                    <option value="Taurus">Boğa</option>
                    <option value="Gemini">İkizler</option>
                    <option value="Cancer">Yengeç</option>
                    <option value="Leo">Aslan</option>
                    <option value="Virgo">Başak</option>
                    <option value="Libra">Terazi</option>
                    <option value="Scorpio">Akrep</option>
                    <option value="Sagittarius">Yay</option>
                    <option value="Capricorn">Oğlak</option>
                    <option value="Aquarius">Kova</option>
                    <option value="Pisces">Balık</option>
                </select>
                <input type="number" id="${planet}-house" value="1" min="1" max="12" style="width: 60px;">
            </div>
        `;
        container.appendChild(div);
    });
}

async function interpretNatal() {
    const btn = document.getElementById('interpret-btn');
    const originalText = btn.innerText;
    btn.innerText = "Yükleniyor...";
    btn.disabled = true;

    const chartData = {};
    planets.forEach(p => {
        chartData[p.toLowerCase()] = {
            sign: document.getElementById(`${p}-sign`).value,
            house: parseInt(document.getElementById(`${p}-house`).value)
        };
    });

    const payload = {
        user_id: "web-user-" + Date.now(),
        focus_area: document.getElementById('focus-area').value,
        chart_data: chartData
    };

    try {
        const response = await fetch(`${API_BASE}/interpret/natal`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        const data = await response.json();
        displayResults(data);
    } catch (error) {
        alert("Gök bilimi motoruna bağlanılamadı. Lütfen API'nin çalıştığından emin olun.");
        console.error(error);
    } finally {
        btn.innerText = originalText;
        btn.disabled = false;
    }
}

function displayResults(data) {
    const resultsPanel = document.getElementById('results-panel');
    resultsPanel.classList.remove('hidden');
    
    document.getElementById('interpretation-text').innerText = data.interpretation;
    
    const list = document.getElementById('citations-list');
    list.innerHTML = "";
    data.citations.forEach(c => {
        const li = document.createElement('li');
        li.innerHTML = `<strong>${c.source}</strong> (Sayfa ${c.page}): <em>"${c.preview}"</em>`;
        list.appendChild(li);
    });
}

async function sendAgentQuery() {
    const input = document.getElementById('agent-query');
    const query = input.value.trim();
    if (!query) return;

    addMessage(query, 'user');
    input.value = "";

    try {
        const response = await fetch(`${API_BASE}/agent/query?query=${encodeURIComponent(query)}`, {
            method: 'POST'
        });
        const data = await response.json();
        addMessage(data.agent_response, 'bot');
    } catch (error) {
        addMessage("Yıldızlar şu an cevap veremiyor. Bağlantı hatası.", 'bot');
    }
}

function addMessage(text, type) {
    const chat = document.getElementById('chat-messages');
    const div = document.createElement('div');
    div.className = `msg ${type}`;
    div.innerText = text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}
