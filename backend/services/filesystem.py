import os

# --- Pure Functions (Validation & Logic) ---

def is_safe_path(path: str) -> bool:
    """
    Pure: Checks if the path is suitable for raw I/O.
    For this 'Raw I/O' domain, we generally require absolute paths 
    to avoid ambiguity regarding the server's Current Working Directory.
    """
    # 1. Must be absolute (e.g. C:/Users/... or /home/user/...)
    if not os.path.isabs(path):
        return False
    
    # 2. Basic check to prevent empty paths
    if not path.strip():
        return False
        
    return True


# --- Effect Functions (Side Effects / IO) ---

def read_text_file(path: str, encoding: str = "utf-8") -> str:
    """
    Impure: Reads the content of a file from the disk.
    Raises:
        ValueError: If path is not absolute.
        FileNotFoundError: If file doesn't exist.
        PermissionError: If access is denied.
        UnicodeDecodeError: If encoding is wrong.
    """
    if not is_safe_path(path):
        raise ValueError(f"Path must be absolute: {path}")

    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    with open(path, 'r', encoding=encoding) as f:
        return f.read()


def write_text_file(path: str, content: str, encoding: str = "utf-8") -> None:
    """
    Impure: Writes content to the disk, overwriting existing files.
    Raises:
        ValueError: If path is not absolute.
        PermissionError: If access is denied.
    """
    if not is_safe_path(path):
        raise ValueError(f"Path must be absolute: {path}")

    # Ensure the directory exists before writing
    # This is a 'convenience' side effect that makes the API friendlier
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    with open(path, 'w', encoding=encoding) as f:
        f.write(content)