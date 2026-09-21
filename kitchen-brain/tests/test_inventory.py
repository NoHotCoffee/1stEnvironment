import json
import os
import tempfile
import unittest
from datetime import date, timedelta

import server


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.inv_path = os.path.join(self.tempdir.name, "inventory.json")
        self.recipes_path = os.path.join(self.tempdir.name, "recipes.json")
        self.barcode_path = os.path.join(self.tempdir.name, "barcode_map.json")

        server.INVENTORY_FILE = self.inv_path
        server.RECIPES_FILE = self.recipes_path
        server.BARCODE_FILE = self.barcode_path

        with open(self.inv_path, "w", encoding="utf-8") as f:
            json.dump({}, f)
        with open(self.recipes_path, "w", encoding="utf-8") as f:
            json.dump([], f)
        with open(self.barcode_path, "w", encoding="utf-8") as f:
            json.dump({}, f)

    def tearDown(self):
        self.tempdir.cleanup()

    def test_upsert_numeric_qty(self):
        item = server.upsert_item("Milk", qty=2)
        self.assertEqual(item["qty"], 2)
        inv = server.load_inventory()
        self.assertIn("milk", inv)

    def test_upsert_text_qty(self):
        item = server.upsert_item("Herbs", qty="a bunch")
        self.assertEqual(item["qty"], "a bunch")

    def test_upsert_expiry_parsing(self):
        expiry_date = "2025-01-01"
        item = server.upsert_item("Yogurt", qty=1, expiry=expiry_date)
        self.assertEqual(item["expiry"], expiry_date)

    def test_upsert_fuzzy_merge(self):
        server.save_inventory_file({"spinach": {"name": "Spinach", "qty": 1}})
        client = server.app.test_client()
        payload = {"items": [{"name": "spinach leaves", "qty": 2}]}
        resp = client.post(
            "/add_items",
            json=payload,
            headers={"Authorization": f"Bearer {server.AUTH_TOKEN}"},
        )
        self.assertEqual(resp.status_code, 200)
        inv = server.load_inventory()
        self.assertEqual(inv["spinach"]["qty"], 3)

    def test_suggestion_prefers_expiring_items(self):
        today = date.today()
        soon_expiry = str(today + timedelta(days=1))

        inventory = {
            "milk": {"name": "Milk", "qty": 1, "expiry": soon_expiry, "last_used": str(today)},
            "rice": {"name": "Rice", "qty": 1},
        }
        recipes = [
            {"name": "Soon Milk Recipe", "ingredients": ["Milk"]},
            {"name": "Rice Bowl", "ingredients": ["Rice"]},
        ]
        server.save_inventory_file(inventory)
        with open(self.recipes_path, "w", encoding="utf-8") as f:
            json.dump(recipes, f)

        client = server.app.test_client()
        resp = client.get("/suggest")
        data = resp.get_json()
        self.assertEqual(resp.status_code, 200)
        self.assertGreaterEqual(len(data["suggestions"]), 2)
        self.assertEqual(data["suggestions"][0]["recipe"], "Soon Milk Recipe")


if __name__ == "__main__":
    unittest.main()
