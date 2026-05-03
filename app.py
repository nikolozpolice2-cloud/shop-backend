from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json

app = Flask(__name__)
app.secret_key = "super_secret_key_123"
CORS(app)

# ---------------- DB ----------------
def init_db():
    conn = sqlite3.connect("orders.db")
    c = conn.cursor()

    # ORDERS
    c.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            status TEXT
        )
    """)

    # PRODUCTS
    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            size TEXT,
            price REAL,
            address TEXT,
            image TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------- HOME ----------------
@app.route("/")
def home():
    return "API WORKING"

# ---------------- CREATE ORDER ----------------
@app.route("/order", methods=["POST"])
def order():
    try:
        data = request.json

        conn = sqlite3.connect("orders.db")
        c = conn.cursor()

        c.execute(
            "INSERT INTO orders (data, status) VALUES (?, ?)",
            (json.dumps(data), "pending")
        )

        conn.commit()
        conn.close()

        return jsonify({"status": "ok"})

    except Exception as e:
        return jsonify({"error": str(e)})

# ---------------- ORDERS API ----------------
@app.route("/orders")
def orders():
    conn = sqlite3.connect("orders.db")
    c = conn.cursor()
    c.execute("SELECT id, data, status FROM orders")
    rows = c.fetchall()
    conn.close()

    result = []

    for r in rows:
        result.append({
            "id": r[0],
            "data": r[1],
            "status": r[2]
        })

    return jsonify(result)

# ---------------- SHIP ORDER ----------------
@app.route("/ship/<int:order_id>")
def ship(order_id):
    conn = sqlite3.connect("orders.db")
    c = conn.cursor()

    c.execute("UPDATE orders SET status='shipped' WHERE id=?", (order_id,))

    conn.commit()
    conn.close()

    return "OK"

# ---------------- PRODUCTS ADD ----------------
@app.route("/add-product", methods=["POST"])
def add_product():
    data = request.json

    conn = sqlite3.connect("orders.db")
    c = conn.cursor()

    c.execute("""
        INSERT INTO products (name, size, price, address, image)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data["name"],
        data["size"],
        data["price"],
        data["address"],
        data.get("image", "")
    ))

    conn.commit()
    conn.close()

    return jsonify({"status": "product added"})

# ---------------- PRODUCTS GET ----------------
@app.route("/products")
def products():
    conn = sqlite3.connect("orders.db")
    c = conn.cursor()

    c.execute("SELECT * FROM products")
    rows = c.fetchall()

    conn.close()

    result = []

    for r in rows:
        result.append({
            "id": r[0],
            "name": r[1],
            "size": r[2],
            "price": r[3],
            "address": r[4],
            "image": r[5]
        })

    return jsonify(result)

# ---------------- ADMIN PAGE ----------------
@app.route("/admin")
def admin():
    return """
<!DOCTYPE html>
<html>
<head>
<title>Admin Panel</title>

<style>
body { font-family: Arial; background:#f4f4f4; padding:20px; }
.box { max-width:900px; margin:auto; background:white; padding:20px; border-radius:10px; }
.order, .product { border:1px solid #ddd; padding:15px; margin-bottom:10px; }
input { width:100%; padding:8px; margin:5px 0; }
button { padding:8px 12px; margin-top:5px; }
</style>
</head>

<body>

<div class="box">

<h1>Admin Panel</h1>
<button onclick="location.reload()">Refresh</button>

<hr>

<h2>Orders</h2>
<div id="orders"></div>

<hr>

<h2>Add Product</h2>

<input id="pname" placeholder="Name">
<input id="psize" placeholder="Size">
<input id="pprice" placeholder="Price">
<input id="paddress" placeholder="Address">
<input id="pimage" placeholder="Image URL">

<button onclick="addProduct()">Add Product</button>

<div id="products"></div>

</div>

<script>

// ---------------- ORDERS ----------------
fetch('/orders')
.then(res => res.json())
.then(data => {

  let html = "";

  data.forEach(o => {

    let c = JSON.parse(o.data);

    html += `
      <div class="order">
        <h3>Order #${o.id}</h3>
        <p><b>Name:</b> ${c.customer.name}</p>
        <p><b>Phone:</b> ${c.customer.phone}</p>
        <p><b>Address:</b> ${c.customer.address}</p>
        <p><b>Country:</b> ${c.customer.country}</p>
        <p><b>Status:</b> ${o.status}</p>

        <a href='/ship/${o.id}'>Mark as shipped</a>
      </div>
    `;
  });

  document.getElementById("orders").innerHTML = html;

});

// ---------------- ADD PRODUCT ----------------
function addProduct() {

  fetch("/add-product", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({
      name: document.getElementById("pname").value,
      size: document.getElementById("psize").value,
      price: document.getElementById("pprice").value,
      address: document.getElementById("paddress").value,
      image: document.getElementById("pimage").value
    })
  })
  .then(res => res.json())
  .then(data => {
    alert("Product added!");
  });

}

</script>

</body>
</html>
"""

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
