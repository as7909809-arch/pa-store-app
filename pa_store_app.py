"""
╔══════════════════════════════════════════════╗
║          PA STORE — Python Web App           ║
║       CEO: Ayan Shill | pastore.dev          ║
╚══════════════════════════════════════════════╝

Run karte: python pa_store_app.py
Then browser e jao: http://localhost:5000
"""

from flask import Flask, render_template_string, jsonify, request
import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "pastore-ayan-shill-2025"

# ─── Company Info ───────────────────────────────
COMPANY = {
    "name": "PA STORE",
    "ceo": "Ayan Shill",
    "founded": 2025,
    "tagline": "Python-Powered Solutions for Modern Developers",
    "website": "pastore.dev",
    "email": "contact@pastore.dev",
}

# ─── Products ───────────────────────────────────
PRODUCTS = [
    {
        "id": 1,
        "name": "PA CoreLib",
        "description": "Core Python utility library with 100+ helper functions.",
        "price": 0,
        "currency": "BDT",
        "category": "Library",
        "tags": ["python", "utilities", "free"],
    },
    {
        "id": 2,
        "name": "PA DataKit",
        "description": "Data processing & analytics toolkit. Pandas, NumPy extensions.",
        "price": 999,
        "currency": "BDT",
        "category": "Data",
        "tags": ["pandas", "numpy", "analytics"],
    },
    {
        "id": 3,
        "name": "PA AutoBot",
        "description": "Automation framework for scheduling, scraping, and workflows.",
        "price": 1499,
        "currency": "BDT",
        "category": "Automation",
        "tags": ["selenium", "celery", "automation"],
    },
    {
        "id": 4,
        "name": "PA FastAPI Kit",
        "description": "Production-ready FastAPI templates with auth and deployment.",
        "price": 799,
        "currency": "BDT",
        "category": "Web",
        "tags": ["fastapi", "rest", "api"],
    },
    {
        "id": 5,
        "name": "PA MLPack",
        "description": "Machine learning starter packs with scikit-learn integrations.",
        "price": 1999,
        "currency": "BDT",
        "category": "ML/AI",
        "tags": ["ml", "scikit-learn", "tensorflow"],
    },
]

# ─── HTML Template ───────────────────────────────
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PA STORE — Python Solutions</title>
  <style>
    * { margin:0; padding:0; box-sizing:border-box; }
    body { background:#0a0a12; color:#fff; font-family:'Segoe UI',sans-serif; }
    nav { display:flex; justify-content:space-between; align-items:center;
          padding:1rem 2rem; border-bottom:1px solid rgba(0,229,255,0.2); }
    .logo { font-size:22px; font-weight:700; color:#00e5ff; letter-spacing:3px; }
    .logo span { color:#ffd700; }
    h1 { text-align:center; font-size:48px; padding:3rem 1rem 1rem;
         background: linear-gradient(135deg,#00e5ff,#7b2dff);
         -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
    .subtitle { text-align:center; color:rgba(255,255,255,0.5); margin-bottom:3rem; }
    .grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
            gap:1.5rem; padding:0 2rem 3rem; }
    .card { background:#12121e; border:1px solid rgba(0,229,255,0.15); border-radius:12px;
            padding:1.5rem; transition:border-color .2s,transform .2s; }
    .card:hover { border-color:#00e5ff; transform:translateY(-4px); }
    .card h3 { color:#00e5ff; margin-bottom:.5rem; }
    .card p { color:rgba(255,255,255,0.5); font-size:13px; line-height:1.6; margin-bottom:1rem; }
    .price { font-size:18px; font-weight:700; color:#ffd700; }
    .tag { display:inline-block; background:rgba(0,229,255,0.1); color:#00e5ff;
           font-size:10px; padding:2px 8px; border-radius:10px; margin:2px; }
    footer { text-align:center; padding:2rem; color:rgba(255,255,255,0.25);
             border-top:1px solid rgba(0,229,255,0.1); font-size:13px; }
    footer span { color:#00e5ff; }
  </style>
</head>
<body>
  <nav>
    <div class="logo">PA<span>STORE</span></div>
    <div style="font-size:12px;color:rgba(255,255,255,0.4);">CEO: <strong style="color:#ffd700;">{{ company.ceo }}</strong></div>
  </nav>

  <h1>{{ company.name }}</h1>
  <p class="subtitle">{{ company.tagline }}</p>

  <div class="grid">
    {% for p in products %}
    <div class="card">
      <h3>{{ p.name }}</h3>
      <p>{{ p.description }}</p>
      <div style="margin-bottom:.8rem;">
        {% for tag in p.tags %}
        <span class="tag">{{ tag }}</span>
        {% endfor %}
      </div>
      <div class="price">{% if p.price == 0 %}Free{% else %}৳{{ p.price }}/mo{% endif %}</div>
    </div>
    {% endfor %}
  </div>

  <footer>
    © {{ year }} <span>{{ company.name }}</span> · Founded by <span>{{ company.ceo }}</span>
  </footer>
</body>
</html>
"""


# ─── Routes ─────────────────────────────────────

@app.route("/")
def home():
    """Homepage — shows all products."""
    return render_template_string(
        HTML_TEMPLATE,
        company=COMPANY,
        products=PRODUCTS,
        year=datetime.date.today().year,
    )


@app.route("/api/company")
def api_company():
    """API: Company information."""
    return jsonify({"success": True, "data": COMPANY})


@app.route("/api/products")
def api_products():
    """API: All products. Filter by ?category=Data"""
    category = request.args.get("category")
    if category:
        filtered = [p for p in PRODUCTS if p["category"].lower() == category.lower()]
        return jsonify({"success": True, "count": len(filtered), "data": filtered})
    return jsonify({"success": True, "count": len(PRODUCTS), "data": PRODUCTS})


@app.route("/api/products/<int:product_id>")
def api_product_detail(product_id):
    """API: Single product by ID."""
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        return jsonify({"success": False, "message": "Product not found"}), 404
    return jsonify({"success": True, "data": product})


@app.route("/api/search")
def api_search():
    """API: Search products by name. ?q=bot"""
    query = request.args.get("q", "").lower()
    if not query:
        return jsonify({"success": False, "message": "Please provide ?q=search_term"}), 400
    results = [p for p in PRODUCTS if query in p["name"].lower() or query in p["description"].lower()]
    return jsonify({"success": True, "query": query, "count": len(results), "data": results})


# ─── PA Store SDK (Simple) ───────────────────────

class PAStoreClient:
    """
    PA Store Python SDK — by Ayan Shill.

    Usage:
        client = PAStoreClient()
        products = client.get_all_products()
        data_products = client.get_by_category("Data")
    """

    def __init__(self, api_key: str = "demo"):
        self.api_key = api_key
        self.company = COMPANY
        print(f"✅ PA Store SDK initialized | CEO: {COMPANY['ceo']}")

    def get_all_products(self) -> list:
        """Return all products."""
        return PRODUCTS

    def get_by_category(self, category: str) -> list:
        """Filter products by category."""
        return [p for p in PRODUCTS if p["category"].lower() == category.lower()]

    def get_product(self, product_id: int) -> dict | None:
        """Get a single product by ID."""
        return next((p for p in PRODUCTS if p["id"] == product_id), None)

    def search(self, query: str) -> list:
        """Search products by name or description."""
        q = query.lower()
        return [p for p in PRODUCTS if q in p["name"].lower() or q in p["description"].lower()]

    def company_info(self) -> dict:
        """Return company information."""
        return self.company


# ─── Main ────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 50)
    print("  🐍 PA STORE — Python Web App")
    print(f"  CEO: {COMPANY['ceo']}")
    print(f"  Founded: {COMPANY['founded']}")
    print("=" * 50)
    print("\n📡 API Endpoints:")
    print("  GET /                      → Homepage")
    print("  GET /api/company           → Company info")
    print("  GET /api/products          → All products")
    print("  GET /api/products/1        → Product by ID")
    print("  GET /api/products?category=Data → Filter")
    print("  GET /api/search?q=bot      → Search")
    print("\n🚀 Server running at http://localhost:5000\n")

    app.run(debug=True, host="0.0.0.0", port=5000)
