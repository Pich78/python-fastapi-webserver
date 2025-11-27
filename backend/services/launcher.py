import sys
import os
import subprocess
import shutil
from typing import Optional, List

# --- Constants ---

# Common paths for Chromium-based browsers on different OSs
WIN_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe"),
    os.path.expanduser(r"~\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe"),
]

LINUX_BINARIES = [
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
    "microsoft-edge",
    "brave-browser"
]

MAC_PATHS = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
]

# --- Pure Functions (Logic) ---

def get_browser_command(executable_path: str, url: str) -> List[str]:
    """
    Pure: Generates the command list to start the browser in Application Mode.
    The '--app' flag tells Chromium to open a window without toolbars/address bar.
    """
    return [executable_path, f"--app={url}"]


# --- Effect Functions (System Interaction) ---

def find_browser_executable() -> Optional[str]:
    """
    Impure: Scans the operating system to find a valid Chromium executable.
    Returns the absolute path to the executable or None if not found.
    """
    platform = sys.platform

    if platform.startswith("win"):
        for path in WIN_PATHS:
            if os.path.exists(path):
                return path
                
    elif platform.startswith("linux"):
        for binary in LINUX_BINARIES:
            # shutil.which checks if the binary is in the system PATH
            path = shutil.which(binary)
            if path:
                return path
                
    elif platform == "darwin":  # macOS
        for path in MAC_PATHS:
            if os.path.exists(path):
                return path

    return None


def launch_process(command: List[str]) -> None:
    """
    Impure: Spawns the subprocess.
    Using Popen ensures the server script doesn't block waiting for the browser to close.
    """
    try:
        # close_fds=True is recommended on POSIX, but not supported on Windows 
        # combined with standard stream redirection usually.
        # We just launch it detached.
        subprocess.Popen(command)
    except Exception as e:
        print(f"[Launcher Error] Failed to start browser: {e}")