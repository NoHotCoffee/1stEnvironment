import datetime
import json
import os
from typing import Any, Dict

from config import UNUSED_DAYS

INVENTORY_FILE = "inventory.json"
RECIPES_FILE = "recipes.json"
SUMMARY_FILE = "summary.json"


def _load_json(path: str, default: Any):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _save_json(path: str, data: Dict[str, Any]):
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)


def _to_date(date_str):
    try:
        return datetime.date.fromisoformat(str(date_str))
    except Exception:
        return None


def generate_summary() -> Dict[str, Any]:
    inventory = _load_json(INVENTORY_FILE, {})
    _ = _load_json(RECIPES_FILE, [])
    today = datetime.date.today()

    expiring_soon = []
    unused_long = []
    low_stock = []

    for key, item in inventory.items():
        expiry = _to_date(item.get("expiry"))
        if expiry is not None:
            days_left = (expiry - today).days
            if days_left <= 7:
                expiring_soon.append(
                    {"name": item.get("name", key), "days_left": days_left, "qty": item.get("qty")}
                )

        last_used = _to_date(item.get("last_used"))
        if last_used is not None:
            days_unused = (today - last_used).days
            if days_unused >= UNUSED_DAYS:
                unused_long.append(
                    {"name": item.get("name", key), "days_unused": days_unused, "qty": item.get("qty")}
                )

        qty = item.get("qty")
        try:
            if float(qty) < 2:
                low_stock.append({"name": item.get("name", key), "qty": qty})
        except (TypeError, ValueError):
            pass

    data = {
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "expiring_soon": expiring_soon,
        "unused_long": unused_long,
        "low_stock": low_stock,
    }
    _save_json(SUMMARY_FILE, data)
    return data


if __name__ == "__main__":
    summary = generate_summary()
    print(json.dumps(summary, indent=2))
