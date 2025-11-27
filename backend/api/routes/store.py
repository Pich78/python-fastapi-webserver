import json
from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, Callable

from domain.schemas import StoreSavePayload, StoreResponse
from api.dependencies import get_json_saver, get_json_loader

router = APIRouter()

@router.post("/save", response_model=StoreResponse)
def save_document(
    payload: StoreSavePayload,
    saver: Callable[[str, str, Dict[str, Any]], str] = Depends(get_json_saver)
):
    """
    Saves a JSON document to the local data store.
    Structure: ./local_data/{collection}/{filename}.json
    """
    try:
        saved_path = saver(payload.collection, payload.filename, payload.data)
        return StoreResponse(status="success", path=saved_path)
    except Exception as e:
        # Since we control the path generation via schemas, errors here 
        # are likely disk I/O issues (full disk, permission).
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{collection}/{filename}")
def get_document(
    collection: str,
    filename: str,
    loader: Callable[[str, str], Dict[str, Any]] = Depends(get_json_loader)
):
    """
    Retrieves a JSON document.
    Returns 404 if the document does not exist.
    """
    try:
        data = loader(collection, filename)
        return data
        
    except FileNotFoundError:
        raise HTTPException(
            status_code=404, 
            detail=f"Document '{filename}' not found in collection '{collection}'"
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500, 
            detail="The file exists but contains invalid JSON data."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))