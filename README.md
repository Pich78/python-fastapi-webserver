# Local Web Platform & Thick Client Framework

**A lightweight, modular framework for building Hybrid Desktop Applications using Python (FastAPI) and modern Web Technologies (HTML/JS).**

This framework allows you to build desktop apps that feel native but use standard web technologies for the UI. It runs locally using Google Chrome (or Edge/Brave) in **Application Mode**, removing the need for heavy runtimes like Electron.

---

## 📖 Core Philosophy: "The Thick Client"

The architecture enforces a strict separation of concerns to ensure scalability and reusability:

1.  **The Backend (Python)** is a generic **Local OS Abstraction Layer**.
    *   It is *application-agnostic*. It doesn't know what a "Kanban Board" is.
    *   It provides stable services: **File I/O**, **JSON Storage**, **System Commands**.
    *   It manages the **Application Lifecycle** (starts the browser, shuts down the PC process when the window closes).

2.  **The Frontend (JavaScript)** contains 100% of the **Business Logic**.
    *   It handles state, validation, and UI rendering.
    *   It communicates with the backend via a standardized **SDK Bridge**, never calling raw HTTP fetch endpoints directly.

---

## 📂 Project Structure

```text
/project-root
├── /backend                    # PYTHON: The OS Layer
│   ├── main.py                 # Entry point (App assembly & Lifecycle)
│   ├── core/
│   │   ├── config.py           # Configuration (Ports, Directories)
│   │   └── exceptions.py       # Custom error handlers
│   ├── domain/
│   │   └── schemas.py          # Pydantic Models (Data Contracts)
│   ├── services/               # FUNCTIONAL CORE (Pure Logic + IO Wrappers)
│   │   ├── filesystem.py       # Raw file reading/writing
│   │   ├── json_store.py       # Managed JSON storage logic
│   │   ├── launcher.py         # Browser detection & spawning
│   │   └── lifecycle.py        # Shutdown signal handling
│   ├── api/
│   │   ├── dependencies.py     # Dependency Injection Container
│   │   └── routes/             # REST Controllers
│   │       ├── sys.py          # System Info & WebSocket
│   │       ├── io.py           # Raw File Access
│   │       └── store.py        # Managed JSON Store
│   │
│   └── /tests                  # TEST SUITE
│       ├── conftest.py         # Test configuration & Fixtures
│       ├── unit/               # Pure logic tests
│       └── integration/        # API Endpoint tests
│
├── /frontend                   # JAVASCRIPT: The Application Layer
│   ├── /sdk
│   │   └── bridge.js           # API Adapter (The "Bridge")
│   ├── /app
│   │   ├── index.html          # Entry Point
│   │   └── logic.js            # App Logic
│
├── requirements.txt            # Python Dependencies
└── README.md
```

## 🚀 How to Run

### 1. Prerequisites
* Python 3.10 or higher.
* Google Chrome, Microsoft Edge, or Brave Browser installed on your system.

### 2. Installation
Open your terminal in the project-root folder.

**Create a Virtual Environment (Recommended):**

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / Mac
python3 -m venv venv
source venv/bin/activate
```

**Install Dependencies:**

```bash
pip install -r requirements.txt
```

### 3. Running the Application
Execute the following command from the root directory:

```bash
python backend/main.py
```

**What happens next?**
* The FastAPI server starts on `http://127.0.0.1:8000`.
* The script automatically finds your browser and launches it in App Mode (no address bar).
* The Frontend loads and establishes a WebSocket connection to the backend.
* **To Stop:** Simply close the browser window. The backend detects the disconnection and terminates the Python process automatically.

## 🧪 Running Tests

This project includes a complete test suite (using pytest) to ensure file operations are safe and the API contract is respected.

### 1. Run All Tests

```bash
pytest backend/tests
```

### 2. Run with Detailed Output

```bash
pytest backend/tests -v
```

**What is tested?**
* **Unit Tests (`tests/unit`)**: Verify the logic of path calculations and security checks without touching the disk.
* **Integration Tests (`tests/integration`)**: Use the FastAPI TestClient to simulate real API calls.
    * *Note: Integration tests use a Temporary Directory fixture. They create and delete files in a temp folder, ensuring your actual local_data is never touched during testing.*

## 🔌 API Reference (The "Stable Base")

The Backend exposes three standard domains. These endpoints remain stable regardless of the application you build (Text Editor, Kanban, Dashboard, etc.).

### A. System Domain (`/sys`)
* **WS `/sys/lifecycle`**: Keeps the app alive.
* **GET `/sys/info`**: Returns OS platform, Python version, CWD.
* **POST `/sys/open-external`**: Opens a URL or File Path in the default OS application.

### B. Raw I/O Domain (`/io`)
*Best for: Code Editors, Log Viewers, IDEs.*
* **POST `/io/read_text`**: Reads raw content from an absolute path.
* **POST `/io/write_text`**: Overwrites a file at an absolute path.

### C. Managed Store Domain (`/store`)
*Best for: Kanban Boards, To-Do Lists, Dashboards.*
The backend acts as a local NoSQL database, saving data as JSON in `./local_data/`.
* **POST `/store/save`**: Saves a JSON payload.
    * Input: `{ "collection": "boards", "filename": "project_a", "data": {...} }`
* **GET `/store/{collection}/{filename}`**: Retrieves the JSON object.

## 🧱 Frontend Development (The Bridge)

If you are building a new app in `frontend/app`, do not call `fetch` directly. Use the provided SDK.

**Example Usage:**

```javascript
import { Bridge } from '../sdk/bridge.js';

async function init() {
    // 1. Connect to Backend (Required for "Kill Switch")
    Bridge.init();

    // 2. Get System Info
    const sysInfo = await Bridge.sys.info();
    console.log(sysInfo);

    // 3. Save a Kanban Board (Managed Store)
    await Bridge.store.save('boards', 'my-project', { tasks: [] });

    // 4. Read a local text file (Raw I/O)
    const content = await Bridge.io.read('C:/Users/Me/notes.txt');
}

init();
```

## 🛠 Troubleshooting

**Browser doesn't open:**
* Check if Chrome/Edge is installed in the default location.
* Open `http://127.0.0.1:8000` manually in your browser.

**"Connection Refused" in Console:**
* Ensure `backend/main.py` is running in the terminal.

**404 on `/sdk/bridge.js`:**
* Ensure you have updated `backend/main.py` to mount the SDK directory correctly (see `app.mount("/sdk", ...)`).