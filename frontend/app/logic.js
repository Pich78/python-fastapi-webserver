import { Bridge } from '../sdk/bridge.js';

// --- UI Helpers ---
const el = (id) => document.getElementById(id);
const setStatus = (id, msg, isError = false) => {
    const el = document.getElementById(id);
    el.textContent = msg;
    el.style.color = isError ? 'red' : 'green';
    setTimeout(() => { el.style.color = '#666'; }, 3000);
};

// --- Main Initialization ---
async function initApp() {
    // 1. Initialize WebSocket for Lifecycle
    Bridge.init();

    // Update WS status UI
    Bridge.socket.onopen = () => el('ws-status').textContent = "Connected ✅";
    Bridge.socket.onclose = () => el('ws-status').textContent = "Disconnected ❌ (App Closing)";

    // 2. Fetch System Info
    try {
        const info = await Bridge.sys.info();
        el('sys-info').innerHTML = `
            <strong>OS:</strong> ${info.platform} <br/>
            <strong>Python:</strong> ${info.python_version} <br/>
            <strong>CWD:</strong> <code>${info.current_working_directory}</code>
        `;
    } catch (e) {
        el('sys-info').textContent = "Error connecting to API.";
    }
}

// --- Event Listeners: Raw I/O ---

el('btn-io-read').addEventListener('click', async () => {
    const path = el('io-path').value;
    if (!path) return alert("Please enter a path");

    try {
        const content = await Bridge.io.read(path);
        el('io-content').value = content;
        setStatus('io-status', `Loaded: ${path}`);
    } catch (e) {
        console.error(e);
        setStatus('io-status', e.message, true);
    }
});

el('btn-io-save').addEventListener('click', async () => {
    const path = el('io-path').value;
    const content = el('io-content').value;
    if (!path) return alert("Please enter a path");

    try {
        await Bridge.io.write(path, content);
        setStatus('io-status', `Saved to disk: ${path}`);
    } catch (e) {
        console.error(e);
        setStatus('io-status', e.message, true);
    }
});

// --- Event Listeners: Managed Store ---

el('btn-store-save').addEventListener('click', async () => {
    const col = el('store-col').value;
    const id = el('store-id').value;
    let data;

    try {
        data = JSON.parse(el('store-content').value);
    } catch (e) {
        return alert("Invalid JSON format");
    }

    try {
        const res = await Bridge.store.save(col, id, data);
        setStatus('store-status', `Saved JSON to: ${res.path}`);
    } catch (e) {
        setStatus('store-status', e.message, true);
    }
});

el('btn-store-load').addEventListener('click', async () => {
    const col = el('store-col').value;
    const id = el('store-id').value;

    try {
        const data = await Bridge.store.get(col, id);
        el('store-content').value = JSON.stringify(data, null, 2);
        setStatus('store-status', `Loaded ${col}/${id}`);
    } catch (e) {
        setStatus('store-status', e.message, true);
    }
});

// Start
initApp();