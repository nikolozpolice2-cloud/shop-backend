from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json

app = Flask(__name__)
CORS(app)

ADMIN_PASSWORD = "1234"

# ---------------- DB ----------------
def init_db():
    conn = sqlite3.connect("orders.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------------- HOME ----------------
@app.route("/")
def home():
    return "API WORKING"

# ---------------- ORDER ----------------
@app.route("/admin")
def admin():
    return "ADMIN WORKS"
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

# ---------------- SHIP ----------------
@app.route("/ship/<int:order_id>")
def ship(order_id):
    conn = sqlite3.connect("orders.db")
    c = conn.cursor()

    c.execute("UPDATE orders SET status='shipped' WHERE id=?", (order_id,))

    conn.commit()
    conn.close()

    return "OK"

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

# ---------------- ADMIN ----------------
@app.route("/admin")
def admin():
    password = request.args.get("pass")

    if password != ADMIN_PASSWORD:
        return "Access denied"

    return """
<!DOCTYPE html>
<html>
<head>
<title>Admin Panel</title>

<style>
body { font-family: Arial; background:#f4f4f4; padding:20px; }
.box { max-width:900px; margin:auto; background:white; padding:20px; border-radius:10px; }
.order { border:1px solid #ddd; padding:15px; margin-bottom:10px; }
button { padding:8px 12px; margin-top:5px; }
</style>
</head>

<body>

<div class="box">
<h1>Admin Panel</h1>
<button onclick="location.reload()">Refresh</button>
<div id="orders"></div>
</div>

<script>

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

</script>

</body>
</html>
"""

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
