import sys
import os
import pytest
from fastapi.testclient import TestClient

# --- FIX IMPORT PATHS ---
# Aggiungiamo la cartella "backend" al sys.path di Python.
# Questo permette ai test di importare "main", "core", "services" come se fossero moduli locali.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Ora possiamo importare main senza errori
from main import app
from core.config import settings

@pytest.fixture(scope="session")
def test_client():
    """
    Creates a TestClient instance.
    We mock the shutdown trigger to avoid killing the test runner.
    """
    from api.dependencies import get_shutdown_trigger
    
    # Mock shutdown to do nothing (lambda che restituisce una lambda che non fa nulla)
    app.dependency_overrides[get_shutdown_trigger] = lambda: lambda: None
    
    with TestClient(app) as client:
        yield client
    
    # Clean up overrides
    app.dependency_overrides = {}

@pytest.fixture(scope="function")
def temp_data_dir(tmp_path):
    """
    Overrides the DATA_DIR setting to use a temporary directory 
    for each test function.
    """
    original_dir = settings.DATA_DIR
    settings.DATA_DIR = str(tmp_path)
    
    yield str(tmp_path)
    
    # Cleanup (restore original)
    settings.DATA_DIR = original_dir