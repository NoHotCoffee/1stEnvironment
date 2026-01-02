from flask import Flask, request, jsonify, render_template_string
import json, os, datetime
from dateutil import parser as dateparser
from rapidfuzz import process, fuzz
from config import AUTH_TOKEN, PORT, HOST, UNUSED_DAYS, TOP_SUGGESTIONS

app = Flask(__name__, static_folder='static')

INVENTORY_FILE = "inventory.json"
RECIPES_FILE = "recipes.json"
BARCODE_FILE = "barcode_map.json"

def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def normalize(s):
    return s.strip().lower()

def fuzzy_match_choice(query, choices, score_cutoff=70):
    if not choices:
        return None, 0
    match = process.extractOne(query, choices, scorer=fuzz.token_sort_ratio)
    if match and match[1] >= score_cutoff:
        return match[0], match[1]
    return None, 0

def load_inventory():
    return load_json(INVENTORY_FILE, {})

def save_inventory_file(inv):
    save_json(INVENTORY_FILE, inv)

def upsert_item(name, qty=1, source='phone', expiry=None, category=None):
    inv = load_inventory()
    key = normalize(name)
    entry = inv.get(key, {"name": name, "qty": 0, "added": None, "last_used": None, "expiry": None, "category": category})
    try:
        q = int(qty)
        entry['qty'] = (entry.get('qty') or 0) + q
    except:
        entry['qty'] = qty or entry.get('qty', 1)
    entry['added'] = entry.get('added') or str(datetime.date.today())
    entry['last_used'] = str(datetime.date.today())
    if expiry:
        try:
            entry['expiry'] = str(dateparser.parse(expiry).date())
        except:
            entry['expiry'] = expiry
    if category:
        entry['category'] = category
    entry.setdefault('sources', []).append(source)
    inv[key] = entry
    save_inventory_file(inv)
    return entry

def check_auth(req):
    auth = req.headers.get('Authorization','')
    return auth == f"Bearer {AUTH_TOKEN}"

@app.route('/add_items', methods=['POST'])
def add_items():
    if not check_auth(request):
        return jsonify({'error':'unauthorized'}), 401
    data = request.get_json() or {}
    items = data.get('items', [])
    added = []
    for it in items:
        name = it.get('name') or it.get('title')
        qty = it.get('qty', 1)
        expiry = it.get('expiry')
        category = it.get('category')
        if not name:
            continue
        inv = load_inventory()
        existing_keys = list(inv.keys())
        match, score = fuzzy_match_choice(normalize(name), existing_keys, score_cutoff=80)
        if match:
            entry = upsert_item(match, qty=qty, source=data.get('source','phone'), expiry=expiry, category=category)
        else:
            entry = upsert_item(name, qty=qty, source=data.get('source','phone'), expiry=expiry, category=category)
        added.append(entry)
    return jsonify({'status':'ok','added':len(added)})

@app.route('/add_barcode', methods=['POST'])
def add_barcode():
    if not check_auth(request):
        return jsonify({'error':'unauthorized'}), 401
    data = request.get_json() or {}
    barcode = data.get('barcode')
    qty = data.get('qty',1)
    if not barcode:
        return jsonify({'error':'no barcode'}), 400
    barcode_map = load_json(BARCODE_FILE, {})
    name = barcode_map.get(barcode)
    if not name:
        name = f'unknown_{barcode}'
    entry = upsert_item(name, qty=qty, source='barcode')
    return jsonify({'status':'ok','item':entry})

@app.route('/suggest', methods=['GET'])
def suggest():
    inv = load_inventory()
    recipes = load_json(RECIPES_FILE, [])
    today = datetime.date.today()
    inv_keys = set(inv.keys())
    suggestions = []
    for r in recipes:
        needed = [normalize(x) for x in r.get('ingredients', [])]
        matched = []
        for ing in needed:
            if ing in inv_keys:
                matched.append(ing)
            else:
                match, score = fuzzy_match_choice(ing, list(inv_keys), score_cutoff=75)
                if match:
                    matched.append(match)
        score = len(matched)/max(1,len(needed))
        expiry_pressure = 0
        for m in matched:
            e = inv.get(m,{}).get('expiry')
            if e:
                try:
                    d = dateparser.parse(e).date()
                    if (d - today).days <= 3:
                        expiry_pressure += 1
                except:
                    pass
        if score == 1.0:
            suggestions.append({'recipe': r['name'], 'type':'full', 'expiry_score': expiry_pressure})
        elif score >= 0.6:
            suggestions.append({'recipe': r['name'], 'type':'partial', 'match_score': round(score,2), 'expiry_score': expiry_pressure})
    suggestions.sort(key=lambda x: (0 if x['type']=='full' else 1, -x.get('expiry_score',0), -x.get('match_score',0)))
    return jsonify({'suggestions': suggestions[:TOP_SUGGESTIONS], 'inventory_count': len(inv)})

@app.route('/inventory', methods=['GET'])
def inventory():
    return jsonify(load_inventory())

@app.route('/summary', methods=['GET'])
def summary():
    inv = load_inventory()
    today = datetime.date.today()
    unused = []
    expiring_soon = []
    for k,v in inv.items():
        last_used = v.get('last_used')
        if last_used:
            try:
                d = dateparser.parse(last_used).date()
                if (today - d).days >= UNUSED_DAYS:
                    unused.append({'name':v.get('name'),'days_since':(today-d).days})
            except:
                pass
        expiry = v.get('expiry')
        if expiry:
            try:
                ed = dateparser.parse(expiry).date()
                days_left = (ed - today).days
                if days_left <= 7:
                    expiring_soon.append({'name':v.get('name'),'days_left': days_left})
            except:
                pass
    return jsonify({'unused': unused, 'expiring_soon': expiring_soon})

INDEX_HTML = '''
<!doctype html>
<html>
<head><meta charset="utf-8"><title>Kitchen Brain</title></head>
<body>
  <h1>Kitchen Brain</h1>
  <p>Local inventory count: <span id="count">...</span></p>
  <button onclick="loadInv()">Refresh Inventory</button>
  <button onclick="getSuggest()">What can I cook?</button>
  <pre id="out"></pre>

  <h3>Add item</h3>
  <input id="name" placeholder="item name"><input id="qty" placeholder="qty" style="width:60px"><input id="expiry" placeholder="YYYY-MM-DD"><button onclick="addItem()">Add</button>

<script>
async function loadInv(){
  const r=await fetch('/inventory'); const j=await r.json(); document.getElementById('out').textContent=JSON.stringify(j,null,2); document.getElementById('count').textContent=Object.keys(j).length}
async function addItem(){
  const name=document.getElementById('name').value; const qty=document.getElementById('qty').value||1; const expiry=document.getElementById('expiry').value||null;
  const payload={items:[{name:name,qty:qty,expiry:expiry}]};
  const r=await fetch('/add_items',{method:'POST',headers:{'Content-Type':'application/json','Authorization':'Bearer '+ 'REPLACE_IN_JS_TOKEN'},body:JSON.stringify(payload)});
  const j=await r.json(); alert(JSON.stringify(j)); loadInv();}
async function getSuggest(){const r=await fetch('/suggest'); const j=await r.json(); document.getElementById('out').textContent=JSON.stringify(j,null,2)}
loadInv();
</script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

if __name__ == '__main__':
    # ensure files exist
    for p,d in [(INVENTORY_FILE,{}),(RECIPES_FILE,[]),(BARCODE_FILE,{})]:
        if not os.path.exists(p):
            save_json(p,d)
    print(f"Starting Kitchen Brain on {HOST}:{PORT}")
    app.run(host=HOST, port=PORT)
