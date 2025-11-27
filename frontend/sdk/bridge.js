/**
 * Local Platform Bridge SDK
 * Acts as the adapter between the Browser UI and the Python Backend.
 */

const API_BASE = ""; // Relative path since we are served by FastAPI
const WS_BASE = `ws://${window.location.host}`;

class PlatformBridge {
    constructor() {
        this.socket = null;
    }

    /**
     * Initializes the connection to the backend.
     * Must be called when the app starts.
     */
    init() {
        console.log("[Bridge] Initializing Lifecycle Connection...");
        this.socket = new WebSocket(`${WS_BASE}/sys/lifecycle`);

        this.socket.onopen = () => {
            console.log("[Bridge] Connected to Backend.");
        };

        this.socket.onclose = () => {
            console.warn("[Bridge] Disconnected from Backend. Application might be shutting down.");
            // Optional: UI indication that connection is lost
            document.body.style.opacity = "0.5";
            document.title = "[Disconnected] " + document.title;
        };
    }

    /**
     * Internal helper for HTTP requests.
     */
    async _request(method, endpoint, body = null) {
        const headers = { 'Content-Type': 'application/json' };
        const config = { method, headers };

        if (body) {
            config.body = JSON.stringify(body);
        }

        const response = await fetch(`${API_BASE}${endpoint}`, config);

        // Check for HTTP errors
        if (!response.ok) {
            let errorMsg = response.statusText;
            try {
                const errorBody = await response.json();
                if (errorBody.detail) errorMsg = errorBody.detail;
            } catch (e) { /* ignore JSON parse error */ }

            throw new Error(`[API Error ${response.status}] ${errorMsg}`);
        }

        return response.json();
    }

    // --- System Domain ---
    sys = {
        info: async () => {
            return await this._request('GET', '/sys/info');
        },
        openExternal: async (urlOrPath) => {
            return await this._request('POST', '/sys/open-external', { url: urlOrPath });
        }
    };

    // --- Raw I/O Domain (Text Editor) ---
    io = {
        read: async (path) => {
            const result = await this._request('POST', '/io/read_text', { path });
            return result.content;
        },
        write: async (path, content) => {
            return await this._request('POST', '/io/write_text', { path, content });
        }
    };

    // --- Managed Store Domain (Kanban/Apps) ---
    store = {
        /**
         * Saves a generic JSON object.
         * @param {string} collection - The category (e.g., 'boards')
         * @param {string} filename - The ID (e.g., 'project-1')
         * @param {object} data - The data object
         */
        save: async (collection, filename, data) => {
            return await this._request('POST', '/store/save', {
                collection,
                filename,
                data
            });
        },

        /**
         * Loads a JSON object.
         * @param {string} collection 
         * @param {string} filename 
         */
        get: async (collection, filename) => {
            return await this._request('GET', `/store/${collection}/${filename}`);
        }
    };
}

// Export a singleton instance
export const Bridge = new PlatformBridge();