import uvicorn
import threading
import time
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from services.launcher import find_browser_executable, get_browser_command, launch_process
from api.routes import sys, io, store

# --- Lifespan Logic ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for the application lifecycle.
    1. Startup: Launches the browser.
    2. Shutdown: Clean up (if needed).
    """
    
    def _start_browser():
        # Give Uvicorn a moment to bind to the port
        time.sleep(1.0) 
        
        chrome_path = find_browser_executable()
        if not chrome_path:
            print("[WARNING] No Chromium-based browser found. Open http://localhost:8000 manually.")
            return
            
        cmd = get_browser_command(chrome_path, settings.STARTUP_URL)
        print(f"[Launcher] Opening app with: {cmd}")
        launch_process(cmd)

    # We launch the browser in a separate thread so it doesn't block the server startup
    thread = threading.Thread(target=_start_browser, daemon=True)
    thread.start()
    
    yield
    
    print("[Main] Server shutting down...")


# --- App Configuration ---

app = FastAPI(
    title="Local Platform",
    lifespan=lifespan
)

# 1. CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Register API Routers
app.include_router(sys.router, prefix="/sys", tags=["System"])
app.include_router(io.router, prefix="/io", tags=["IO"])
app.include_router(store.router, prefix="/store", tags=["Store"])

# 3. Serve Frontend Static Files

# MOUNT SDK: Serve /sdk/bridge.js
# This must be defined BEFORE the root mount to ensure specific paths are caught first.
frontend_sdk_dir = os.path.join(settings.FRONTEND_DIR, "sdk")
if os.path.exists(frontend_sdk_dir):
    app.mount("/sdk", StaticFiles(directory=frontend_sdk_dir), name="sdk")
else:
    print(f"[WARNING] SDK directory not found at: {frontend_sdk_dir}")

# MOUNT APP: Serve index.html at root "/"
frontend_app_dir = os.path.join(settings.FRONTEND_DIR, "app")
if os.path.exists(frontend_app_dir):
    app.mount("/", StaticFiles(directory=frontend_app_dir, html=True), name="ui")
else:
    print(f"[WARNING] Frontend App directory not found at: {frontend_app_dir}")


if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host=settings.APP_HOST, 
        port=settings.APP_PORT, 
        reload=True
    )