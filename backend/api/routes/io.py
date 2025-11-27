from fastapi import APIRouter, HTTPException, Depends
from typing import Callable

from domain.schemas import FileReadPayload, FileWritePayload, FileReadResponse
from api.dependencies import get_file_reader, get_file_writer

router = APIRouter()

@router.post("/read_text", response_model=FileReadResponse)
def read_text_file(
    payload: FileReadPayload,
    reader: Callable[[str], str] = Depends(get_file_reader)
):
    """
    Reads the raw content of a text file from the local file system.
    """
    try:
        content = reader(payload.path)
        return FileReadResponse(path=payload.path, content=content)
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Permission denied")
    except ValueError as e:
        # Usually happens if path is not absolute
        raise HTTPException(status_code=400, detail=str(e))
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=422, 
            detail="Cannot decode file. It might be binary or use a different encoding."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/write_text")
def write_text_file(
    payload: FileWritePayload,
    writer: Callable[[str, str], None] = Depends(get_file_writer)
):
    """
    Writes text content to a file. Overwrites if it exists.
    Creates parent directories if missing.
    """
    try:
        writer(payload.path, payload.content)
        return {"status": "success", "path": payload.path}
        
    except PermissionError:
        raise HTTPException(status_code=403, detail="Permission denied")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))