import json
import os
import urllib.error
import urllib.parse
import urllib.request

from config import BARCODE_API_KEY, BARCODE_API_URL, BARCODE_TIMEOUT

BARCODE_FILE = "barcode_map.json"


def _load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _normalize(name: str) -> str:
    return name.strip().lower()


def lookup_barcode(barcode: str) -> str | None:
    """Lookup a barcode via API if configured; fallback to local map."""
    name = None
    if BARCODE_API_KEY and BARCODE_API_KEY != "REPLACE_WITH_API_KEY":
        try:
            query = urllib.parse.urlencode({"upc": barcode, "key": BARCODE_API_KEY})
            url = f"{BARCODE_API_URL}?{query}"
            with urllib.request.urlopen(url, timeout=BARCODE_TIMEOUT) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    name = data.get("name") or data.get("product") or data.get("title")
        except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError):
            name = None

    if not name:
        barcode_map = _load_json(BARCODE_FILE, {})
        name = barcode_map.get(barcode)

    return _normalize(name) if isinstance(name, str) else None
