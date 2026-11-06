def test_translate_endpoint(client):
    response = client.post("/translate", json={
        "text": "안녕하세요", "source_lang": "ko", "target_lang": "vi"
    })
    assert response.status_code == 200
    assert response.json() == {
        "translated_text": "translated:안녕하세요",
        "source_lang": "ko",
        "target_lang": "vi",
    }


def test_health(client):
    assert client.get("/health").json() == {
        "status": "ok", "engine": "argos", "models_loaded": True
    }


def test_languages(client):
    body = client.get("/languages").json()
    assert "ko" in body["languages"]
    assert {"source_lang": "ko", "target_lang": "vi"} in body["pairs"]
