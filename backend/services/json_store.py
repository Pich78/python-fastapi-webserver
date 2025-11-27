import json
import os
from typing import Dict, Any

# --- Pure Functions (Logic) ---

def compute_store_path(base_dir: str, collection: str, filename: str) -> str:
    """
    Pure: Deterministically calculates the full file path.
    Logic: base_dir / collection / filename.json
    """
    # Note: Pydantic schemas already validate that 'collection' and 'filename' 
    # contain safe characters, so we can join them safely here.
    return os.path.join(base_dir, collection, f"{filename}.json")


# --- Effect Functions (IO) ---

def save_json_to_disk(path: str, data: Dict[str, Any]) -> None:
    """
    Impure: Writes the dictionary as a formatted JSON file to the disk.
    Automatically creates the 'collection' folder if it doesn't exist.
    """
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_json_from_disk(path: str) -> Dict[str, Any]:
    """
    Impure: Reads a JSON file from disk and parses it.
    
    Raises:
        FileNotFoundError: If the document doesn't exist.
        json.JSONDecodeError: If the file content is corrupted.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Document not found at path: {path}")

    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)