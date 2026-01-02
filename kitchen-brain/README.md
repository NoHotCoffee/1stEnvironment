# Kitchen Brain

A local, always-on food memory + meal suggestion helper (minimal).

## Quick start (Windows)

1. Install Python 3.10+.
2. Open PowerShell in this project folder.
3. python -m venv .venv
4. .\.venv\Scripts\Activate
5. pip install -r requirements.txt
6. Edit config.py and set AUTH_TOKEN to a long random string.
7. python server.py
8. Find your PC IP with `ipconfig` and use it in your phone Shortcuts.

## Endpoints

- POST /add_items       (headers: Authorization: Bearer <token>, body: {"items":[{"name": "...", "qty":1, "expiry":"YYYY-MM-DD"}]})
- POST /add_barcode     (headers: Authorization: Bearer <token>, body: {"barcode":"0123456789012", "qty":1})
- GET  /suggest
- GET  /inventory
- GET  /summary

## Notes

- inventory.json is intentionally ignored (it stores your private inventory).
- The server is local-first and expects to run on your LAN.
- Replace AUTH_TOKEN in config.py with a strong secret before using the write endpoints.
