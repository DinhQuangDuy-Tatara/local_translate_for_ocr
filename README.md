# Local Translate Module (ORD)

Local HTTP translation service using Argos Translate. It is designed for OCR text from ORD, but runs independently. It does not use a paid translation API and does not send text to an external translation service. Translation models must be installed before use.

## Requirements

- Python 3.10+
- Argos language packages installed for the desired direction(s)
- CachyOS/Linux recommended; no OCR, overlay, or desktop integration is included

## Install

```bash
python -m venv .venv
source .venv/bin/activate.fish  # Fish shell
python -m pip install -e ".[dev]"
```

For Bash, use `source .venv/bin/activate`.

Install Argos language packages using its supported package-management CLI or Python API. Install the required direct language pair(s) before starting the service. The service never downloads models per request. See Argos Translate documentation: https://argos-translate.readthedocs.io/en/stable/

## Run

```bash
local-translate
# or
python -m translate_module.main
```

The service binds to `127.0.0.1:8765` by default. Do not change the host to `0.0.0.0` unless you deliberately intend to expose it to your network.

## HTTP API

`POST /translate`

```json
{"text":"안녕하세요","source_lang":"ko","target_lang":"vi"}
```

Use `"source_lang":"auto"` for best-effort language detection. Response:

```json
{"translated_text":"Xin chào","source_lang":"ko","target_lang":"vi"}
```

`GET /health` reports service and model availability. `GET /languages` lists installed language codes and direct translation pairs.

## Python client

```python
import httpx

response = httpx.post(
    "http://127.0.0.1:8765/translate",
    json={"text": "안녕하세요", "source_lang": "ko", "target_lang": "vi"},
    timeout=30,
)
response.raise_for_status()
print(response.json()["translated_text"])
```

## Notes

- Available languages/pairs depend on the Argos packages installed on this machine. The service does not claim that every requested pair exists.
- `auto` detection uses installed model languages and is best-effort; for short comic dialogue, explicitly set source language when known.
- Text is not logged or persisted by the application.
- Offline operation is possible after dependencies and model packages have been installed. This repository does not bundle model weights.
- Tests use fake engines and do not require downloaded models or network access.
