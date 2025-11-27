def test_system_info(test_client):
    response = test_client.get("/sys/info")
    assert response.status_code == 200
    data = response.json()
    assert "platform" in data
    assert "python_version" in data

def test_store_workflow(test_client, temp_data_dir):
    """
    Test saving and then loading a JSON object.
    Uses temp_data_dir so it doesn't touch real files.
    """
    payload = {
        "collection": "tests",
        "filename": "integration_test",
        "data": {"foo": "bar", "count": 1}
    }

    # 1. SAVE
    save_resp = test_client.post("/store/save", json=payload)
    assert save_resp.status_code == 200
    assert save_resp.json()["status"] == "success"

    # 2. LOAD
    load_resp = test_client.get("/store/tests/integration_test")
    assert load_resp.status_code == 200
    loaded_data = load_resp.json()
    
    assert loaded_data["foo"] == "bar"
    assert loaded_data["count"] == 1

def test_store_not_found(test_client, temp_data_dir):
    response = test_client.get("/store/tests/non_existent")
    assert response.status_code == 404