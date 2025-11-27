import os
import sys
import threading
import time
import logging

# Configure a logger for lifecycle events
logger = logging.getLogger("uvicorn.error")

# --- Effect Functions (System) ---

def shutdown_process(delay: float = 0.5) -> None:
    """
    Impure: Terminates the current Python process.
    
    Args:
        delay: Seconds to wait before killing the process. 
               Useful to allow the WebSocket close frame to be sent back to the client.
    """
    def _kill():
        logger.info(f"Shutdown triggered. Terminating process in {delay}s...")
        time.sleep(delay)
        
        # os._exit(0) is used here instead of sys.exit()
        # sys.exit() only raises a SystemExit exception, which can be caught 
        # or ignored by running threads (like Uvicorn's).
        # os._exit(0) forces an immediate exit at the OS level.
        os._exit(0)

    # We run the kill sequence in a separate thread so we don't block
    # the current request/websocket handler that called this function.
    threading.Thread(target=_kill, daemon=True).start()