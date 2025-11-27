import sys
import os
import webbrowser
from typing import Callable
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends

from domain.schemas import SystemInfo, OpenExternalPayload
from api.dependencies import get_shutdown_trigger

router = APIRouter()

@router.get("/info", response_model=SystemInfo)
def get_system_info():
    """
    Returns metadata about the host environment.
    Useful for the frontend to know it's running in the correct context.
    """
    return SystemInfo(
        platform=sys.platform,
        python_version=sys.version,
        current_working_directory=os.getcwd()
    )

@router.post("/open-external")
def open_external_resource(payload: OpenExternalPayload):
    """
    Opens a URL or a local file using the operating system's default application.
    Examples:
    - "https://google.com" -> Opens default browser.
    - "C:/Users/Docs/report.pdf" -> Opens PDF viewer.
    - "C:/Users/Docs" -> Opens File Explorer/Finder.
    """
    # webbrowser.open is a standard Python function that attempts to open
    # the given URL or path in the registered default application.
    webbrowser.open(payload.url)
    return {"status": "opened", "target": payload.url}

@router.websocket("/lifecycle")
async def lifecycle_endpoint(
    websocket: WebSocket,
    shutdown: Callable[[], None] = Depends(get_shutdown_trigger)
):
    """
    The 'Heartbeat' connection.
    1. Frontend connects on startup.
    2. Backend accepts and holds the connection.
    3. If Frontend disconnects (User closes window), Backend triggers shutdown.
    """
    await websocket.accept()
    try:
        while True:
            # We sit here and wait. The frontend might send 'ping' messages,
            # but fundamentally we just want to block until the connection drops.
            await websocket.receive_text()
    except WebSocketDisconnect:
        print("[Lifecycle] Frontend disconnected. Triggering shutdown...")
        shutdown()