  """
╔══════════════════════════════════════════════╗
║          PA STORE — Python Web App           ║
║       CEO: Ayan Shill | pastore.dev          ║
╚══════════════════════════════════════════════╝
"""

from flask import Flask, render_template_string, jsonify, request
import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "pastore-ayan-shill-2025"

COMPANY = {
    "name": "PA STORE",
    "ceo": "Ayan Shill",
    "founded": 2025,
    "tagline": "Python-Powered Solutions for Modern Developers",
    "website": "pastore.dev",
    "email": "contact@pastore.dev",
}

PRODUCTS = [
    {
        "id": 1,
        "name": "PA CoreLib",
        "description": "Core Python utility library with 100+ helper functions.",
        "long_description": "PA CoreLib is the foundation of all PA STORE products. It includes 100+ battle-tested Python utility functions for string manipulation, file handling, date processing, and more. Perfect for beginners and professionals alike.",
        "price": 0,
        "currency": "BDT",
        "category": "Library",
        "tags": ["python", "utilities", "free"],
        "features": ["100+ helper functions", "Zero dependencies", "Python 3.8+", "MIT License", "Full documentation"],
    },
    {
        "id": 2,
        "name": "PA DataKit",
        "description": "Data processing & analytics toolkit. Pandas, NumPy extensions.",
        "long_description": "PA DataKit supercharges your data workflow with powerful Pandas and NumPy extensions. Clean, transform, and analyze data 10x faster with built-in visualization helpers.",
        "price": 999,
        "currency": "BDT",
        "category": "Data",
        "tags": ["pandas", "numpy", "analytics"],
        "features": ["Pandas extensions", "NumPy utilities", "Auto visualization", "CSV/Excel support", "Email reports"],
    },
    {
        "id": 3,
        "name": "PA AutoBot",
        "description": "Automation framework for scheduling, scraping, and workflows.",
        "long_description": "PA AutoBot is a powerful automation framework that handles web scraping, task scheduling, and complex workflows. Built on Selenium and Celery for enterprise-grade reliability.",
        "price": 1499,
        "currency": "BDT",
        "category": "Automation",
        "tags": ["selenium", "celery", "automation"],
        "features": ["Web scraping", "Task scheduler", "Workflow builder", "Selenium integration", "Slack notifications"],
    },
    {
        "id": 4,
        "name": "PA FastAPI Kit",
        "description": "Production-ready FastAPI templates with auth and deployment.",
        "long_description": "PA FastAPI Kit gives you production-ready FastAPI project templates with JWT authentication, database integration, Docker support, and one-click cloud deployment.",
        "price": 799,
        "currency": "BDT",
        "category": "Web",
        "tags": ["fastapi", "rest", "api"],
        "features": ["JWT Auth", "PostgreSQL ready", "Docker included", "Auto API docs", "Deploy scripts"],
    },
    {
        "id": 5,
        "name": "PA MLPack",
        "description": "Machine learning starter packs with scikit-learn integrations.",
        "long_description": "PA MLPack provides ready-to-use machine learning pipelines with scikit-learn and TensorFlow integrations. Includes model training, evaluation, and deployment templates.",
        "price": 1999,
        "currency": "BDT",
        "category": "ML/AI",
        "tags": ["ml", "scikit-learn", "tensorflow"],
        "features": ["ML pipelines", "scikit-learn", "TensorFlow", "Model deployment", "Jupyter notebooks"],
    },
]

# ─── HTML Templates ───────────────────────────────

BASE_STYLE = """
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background:#0a0a12; color:#fff; font-family:'Segoe UI',sans-serif; }
  nav { display:flex; justify-content:space-between; align-items:center;
        padding:1rem 2rem; border-bottom:1px solid rgba(0,229,255,0.2); }
  .logo { font-size:22px; font-weight:700; color:#00e5ff; letter-spacing:3px; text-decoration:none; }
  .logo span { color:#ffd700; }
  footer { text-align:center; padding:2rem; color:rgba(255,255,255,0.25);
           border-top:1px solid rgba(0,229,255,0.1); font-size:13px; }
  footer span { color:#00e5ff; }
  .btn { display:inline-block; padding:.6rem 1.4rem; border-radius:8px;
         font-size:13px; font-weight:600; cursor:pointer; text-decoration:none;
         transition:all .2s; border:none; }
  .btn-primary { background:#00e5ff; color:#0a0a12; }
  .btn-primary:hover { background:#00bcd4; transform:translateY(-2px); }
  .btn-outline { background:transparent; color:#00e5ff; border:1px solid #00e5ff; }
  .btn-outline:hover { background:rgba(0,229,255,0.1); transform:translateY(-2px); }
  .tag { display:inline-block; background:rgba(0,229,255,0.1); color:#00e5ff;
         font-size:10px; padding:2px 8px; border-radius:10px; margin:2px; }
</style>
"""

HOME_TEMPLATE = BASE_STYLE + """
<style>
  h1 { text-align:center; font-size:48px; padding:3rem 1rem 1rem;
       background:linear-gradient(135deg,#00e5ff,#7b2dff);
       -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
  .subtitle { text-align:center; color:rgba(255,255,255,0.5); margin-bottom:3rem; }
  .grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr));
          gap:1.5rem; padding:0 2rem 3rem; }
  .card { background:#12121e; border:1px solid rgba(0,229,255,0.15); border-radius:12px;
          padding:1.5rem; transition:border-color .2s,transform .2s;
          display:flex; flex-direction:column; }
  .card:hover { border-color:#00e5ff; transform:translateY(-4px); }
  .card h3 { color:#00e5ff; margin-bottom:.5rem; }
  .card p { color:rgba(255,255,255,0.5); font-size:13px; line-height:1.6; margin-bottom:1rem; flex:1; }
  .price { font-size:18px; font-weight:700; color:#ffd700; margin-bottom:1rem; }
  .card-footer { display:flex; justify-content:space-between; align-items:center; margin-top:auto; }
</style>

<nav>
  <a href="/" class="logo">PA<span>STORE</span></a>
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
    <div class="card-footer">
      <div class="price">{% if p.price == 0 %}Free{% else %}৳{{ p.price }}/mo{% endif %}</div>
      <a href="/product/{{ p.id }}" class="btn btn-outline">View Details →</a>
    </div>
  </div>
  {% endfor %}
</div>

<footer>
  © {{ year }} <span>{{ company.name }}</span> · Founded by <span>{{ company.ceo }}</span>
</footer>
"""

DETAIL_TEMPLATE = BASE_STYLE + """
<style>
  .container { max-width:800px; margin:3rem auto; padding:0 2rem; }
  .back { color:rgba(255,255,255,0.4); font-size:13px; text-decoration:none; display:inline-block; margin-bottom:2rem; }
  .back:hover { color:#00e5ff; }
  .product-header { margin-bottom:2rem; }
  .product-header h1 { font-size:36px; color:#00e5ff; margin-bottom:.5rem; }
  .product-header p { color:rgba(255,255,255,0.6); line-height:1.8; font-size:15px; }
  .price-box { background:#12121e; border:1px solid rgba(0,229,255,0.2); border-radius:12px;
               padding:2rem; margin:2rem 0; }
  .big-price { font-size:36px; font-weight:700; color:#ffd700; margin-bottom:1rem; }
  .features { background:#12121e; border:1px solid rgba(0,229,255,0.1); border-radius:12px; padding:2rem; margin:1rem 0; }
  .features h3 { color:#00e5ff; margin-bottom:1rem; }
  .features ul { list-style:none; }
  .features ul li { padding:.4rem 0; color:rgba(255,255,255,0.7); font-size:14px; }
  .features ul li::before { content:"✅ "; }
  .buy-btn { background:linear-gradient(135deg,#00e5ff,#7b2dff); color:#fff;
             padding:1rem 2rem; border-radius:10px; font-size:16px; font-weight:700;
             cursor:pointer; border:none; width:100%; text-align:center;
             display:block; text-decoration:none; transition:opacity .2s; margin-top:1rem; }
  .buy-btn:hover { opacity:.85; }
  .free-btn { background:linear-gradient(135deg,#00e5ff,#00bcd4); color:#0a0a12; }
  .modal-overlay { display:none; position:fixed; top:0;left:0;right:0;bottom:0;
                   background:rgba(0,0,0,0.7); z-index:100; justify-content:center; align-items:center; }
  .modal-overlay.active { display:flex; }
  .modal { background:#12121e; border:1px solid rgba(0,229,255,0.3); border-radius:16px;
           padding:2.5rem; max-width:420px; width:90%; text-align:center; }
  .modal h2 { color:#00e5ff; margin-bottom:1rem; }
  .modal p { color:rgba(255,255,255,0.6); font-size:14px; margin-bottom:1.5rem; line-height:1.6; }
  .modal input { width:100%; background:#0a0a12; border:1px solid rgba(0,229,255,0.3);
                 color:#fff; padding:.8rem 1rem; border-radius:8px; font-size:14px;
                 margin-bottom:1rem; outline:none; }
  .modal input:focus { border-color:#00e5ff; }
  .close-btn { background:transparent; border:none; color:rgba(255,255,255,0.4);
               cursor:pointer; font-size:20px; position:absolute; top:1rem; right:1rem; }
  .success-msg { display:none; color:#00e5ff; font-size:14px; margin-top:1rem; }
</style>

<nav>
  <a href="/" class="logo">PA<span>STORE</span></a>
  <div style="font-size:12px;color:rgba(255,255,255,0.4);">CEO: <strong style="color:#ffd700;">{{ company.ceo }}</strong></div>
</nav>

<div class="container">
  <a href="/" class="back">← Back to Store</a>

  <div class="product-header">
    <div style="margin-bottom:.5rem;">
      {% for tag in product.tags %}
      <span class="tag">{{ tag }}</span>
      {% endfor %}
    </div>
    <h1>{{ product.name }}</h1>
    <p>{{ product.long_description }}</p>
  </div>

  <div class="features">
    <h3>✨ What's Included</h3>
    <ul>
      {% for f in product.features %}
      <li>{{ f }}</li>
      {% endfor %}
    </ul>
  </div>

  <div class="price-box">
    <div class="big-price">
      {% if product.price == 0 %}Free Forever{% else %}৳{{ product.price }}/month{% endif %}
    </div>
    {% if product.price == 0 %}
    <a href="#" class="buy-btn free-btn" onclick="openModal()">🚀 Download Free</a>
    {% else %}
    <a href="#" class="buy-btn" onclick="openModal()">🛒 Buy Now — ৳{{ product.price }}/mo</a>
    {% endif %}
  </div>
</div>

<!-- Modal -->
<div class="modal-overlay" id="modal">
  <div class="modal" style="position:relative;">
    <button class="close-btn" onclick="closeModal()">✕</button>
    {% if product.price == 0 %}
    <h2>🚀 Get {{ product.name }}</h2>
    <p>Enter your email and we'll send you the download link instantly!</p>
    {% else %}
    <h2>🛒 Buy {{ product.name }}</h2>
    <p>Enter your email to complete the purchase. We'll send you access details within 24 hours.</p>
    {% endif %}
    <input type="email" id="emailInput" placeholder="your@email.com" />
    <button class="btn btn-primary" style="width:100%;padding:.8rem;" onclick="submitOrder()">
      {% if product.price == 0 %}Get Free Access{% else %}Confirm Purchase{% endif %}
    </button>
    <div class="success-msg" id="successMsg">
      ✅ Done! Check your email soon. Thank you!
    </div>
  </div>
</div>

<script>
function openModal() { document.getElementById('modal').classList.add('active'); }
function closeModal() { document.getElementById('modal').classList.remove('active'); }
function submitOrder() {
  const email = document.getElementById('emailInput').value;
  if (!email || !email.includes('@')) { alert('Please enter a valid email!'); return; }
  document.getElementById('successMsg').style.display = 'block';
  setTimeout(() => closeModal(), 2500);
}
</script>

<footer>
  © {{ year }} <span>{{ company.name }}</span> · Founded by <span>{{ company.ceo }}</span>
</footer>
"""


# ─── Routes ─────────────────────────────────────

@app.route("/")
def home():
    return render_template_string(
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>PA STORE</title></head><body>" + HOME_TEMPLATE + "</body></html>",
        company=COMPANY, products=PRODUCTS, year=datetime.date.today().year,
    )


@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        return "<h1 style='color:white;text-align:center;margin-top:5rem;'>Product not found</h1>", 404
    return render_template_string(
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>" + product["name"] + " — PA STORE</title></head><body>" + DETAIL_TEMPLATE + "</body></html>",
        company=COMPANY, product=product, year=datetime.date.today().year,
    )


@app.route("/api/company")
def api_company():
    return jsonify({"success": True, "data": COMPANY})


@app.route("/api/products")
def api_products():
    category = request.args.get("category")
    if category:
        filtered = [p for p in PRODUCTS if p["category"].lower() == category.lower()]
        return jsonify({"success": True, "count": len(filtered), "data": filtered})
    return jsonify({"success": True, "count": len(PRODUCTS), "data": PRODUCTS})


@app.route("/api/products/<int:product_id>")
def api_product_detail(product_id):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        return jsonify({"success": False, "message": "Product not found"}), 404
    return jsonify({"success": True, "data": product})


@app.route("/api/search")
def api_search():
    query = request.args.get("q", "").lower()
    if not query:
        return jsonify({"success": False, "message": "Please provide ?q=search_term"}), 400
    results = [p for p in PRODUCTS if query in p["name"].lower() or query in p["description"].lower()]
    return jsonify({"success": True, "query": query, "count": len(results), "data": results})


if __name__ == "__main__":
    print("=" * 50)
    print("  🐍 PA STORE — Python Web App")
    print(f"  CEO: {COMPANY['ceo']}")
    print(f"  Founded: {COMPANY['founded']}")
    print("=" * 50)
    app.run(debug=True, host="0.0.0.0", port=5000)
    
