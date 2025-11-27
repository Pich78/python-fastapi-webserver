from services import filesystem, json_store
import os

def test_is_safe_path():
    # Should be safe (Absolute paths)
    # Note: On Windows, use drive letters. On Linux, use root /
    if os.name == 'nt':
        assert filesystem.is_safe_path("C:\\Users\\test.txt") is True
    else:
        assert filesystem.is_safe_path("/tmp/test.txt") is True

    # Should be unsafe
    assert filesystem.is_safe_path("relative/path.txt") is False
    assert filesystem.is_safe_path("") is False
    assert filesystem.is_safe_path("   ") is False

def test_compute_store_path():
    base = "/data"
    col = "boards"
    doc = "project-1"
    
    expected = os.path.join(base, col, f"{doc}.json")
    result = json_store.compute_store_path(base, col, doc)
    
    assert result == expected