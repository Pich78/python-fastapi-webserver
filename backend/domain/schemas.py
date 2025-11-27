from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

# --- System Domain ---

class SystemInfo(BaseModel):
    """Output model for system information."""
    platform: str
    python_version: str
    current_working_directory: str

class OpenExternalPayload(BaseModel):
    """Input model to open a URL or file in the OS default app."""
    url: str = Field(..., min_length=1, description="URL or absolute file path to open")


# --- Raw I/O Domain ---

class FileReadPayload(BaseModel):
    """Input model for reading raw text files."""
    path: str = Field(..., min_length=1, description="Absolute path to the file")

class FileWritePayload(BaseModel):
    """Input model for writing raw text files."""
    path: str = Field(..., min_length=1, description="Absolute path to the file")
    content: str = Field("", description="Text content to write")
    encoding: str = Field("utf-8", description="File encoding")

class FileReadResponse(BaseModel):
    """Output model containing file content."""
    path: str
    content: str


# --- Managed Store Domain ---

class StoreSavePayload(BaseModel):
    """
    Input model for saving structured JSON data.
    
    Constraints:
    - collection: must be alphanumeric (prevent directory traversal).
    - filename: must be alphanumeric or dashes (prevent path injection).
    """
    collection: str = Field(
        ..., 
        min_length=1, 
        pattern=r"^[a-zA-Z0-9_]+$", 
        description="Category folder (e.g., 'boards', 'users')"
    )
    filename: str = Field(
        ..., 
        min_length=1, 
        pattern=r"^[a-zA-Z0-9_\-]+$", 
        description="Document ID (e.g., 'project-alpha')"
    )
    data: Dict[str, Any] = Field(..., description="The complete JSON object to save")

class StoreResponse(BaseModel):
    """Generic acknowledgment for store operations."""
    status: str
    path: Optional[str] = None