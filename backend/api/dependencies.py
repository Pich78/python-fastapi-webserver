from typing import Callable, Dict, Any
from fastapi import Depends

from core.config import settings
from services import filesystem, json_store, lifecycle

# --- Raw I/O Dependencies ---

def get_file_reader() -> Callable[[str], str]:
    """
    Returns the function responsible for reading raw text files.
    Signature: (path: str) -> str
    """
    return filesystem.read_text_file

def get_file_writer() -> Callable[[str, str], None]:
    """
    Returns the function responsible for writing raw text files.
    Signature: (path: str, content: str) -> None
    """
    return filesystem.write_text_file


# --- Managed Store Dependencies ---

def get_json_saver() -> Callable[[str, str, Dict[str, Any]], str]:
    """
    Returns a callable that saves JSON data to the configured DATA_DIR.
    
    This dependency 'curries' the base_dir setting, so the router 
    doesn't need to know where the local_data folder is located.
    
    Signature: (collection, filename, data) -> saved_path
    """
    def _saver(collection: str, filename: str, data: Dict[str, Any]) -> str:
        # 1. Compute the path (Pure Logic)
        path = json_store.compute_store_path(settings.DATA_DIR, collection, filename)
        # 2. Perform the I/O (Side Effect)
        json_store.save_json_to_disk(path, data)
        return path
        
    return _saver

def get_json_loader() -> Callable[[str, str], Dict[str, Any]]:
    """
    Returns a callable that loads JSON data from the configured DATA_DIR.
    
    Signature: (collection, filename) -> dict
    """
    def _loader(collection: str, filename: str) -> Dict[str, Any]:
        # 1. Compute the path (Pure Logic)
        path = json_store.compute_store_path(settings.DATA_DIR, collection, filename)
        # 2. Perform the I/O (Side Effect)
        return json_store.load_json_from_disk(path)
        
    return _loader


# --- Lifecycle Dependencies ---

def get_shutdown_trigger() -> Callable[[], None]:
    """
    Returns the function responsible for terminating the process.
    """
    return lifecycle.shutdown_process