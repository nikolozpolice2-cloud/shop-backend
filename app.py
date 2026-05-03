from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json

app = Flask(__name__)
CORS(app)

# ---------------- DATABASE ----------------
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

# ---------------- MARK AS SHIPPED ----------------
@app.route("/ship/<int:order_id>")
def ship(order_id):
    conn = sqlite3.connect("orders.db")
    c = conn.cursor()

    c.execute("UPDATE orders SET status='shipped' WHERE id=?", (order_id,))

    conn.commit()
    conn.close()

    return "OK"

# ---------------- VIEW ORDERS ----------------
@app.route("/orders")
def orders():

    conn = sqlite3.connect("orders.db")
    c = conn.cursor()
    c.execute("SELECT * FROM orders")
    rows = c.fetchall()
    conn.close()

    html = "<h1>Orders</h1>"

    for row in rows:
        order_id = row[0]
        data = json.loads(row[1])
        status = row[2]

        customer = data.get("customer", {})
        items = data.get("items", [])

        html += "<div style='border:1px solid #000; padding:10px; margin:10px;'>"

        html += f"<p><b>ID:</b> {order_id}</p>"
        html += f"<p><b>Status:</b> {status}</p>"

        # customer info
        html += f"<p><b>Name:</b> {customer.get('name','')}</p>"
        html += f"<p><b>Phone:</b> {customer.get('phone','')}</p>"
        html += f"<p><b>Address:</b> {customer.get('address','')}</p>"
        html += f"<p><b>Country:</b> {customer.get('country','')}</p>"
        html += f"<p><b>ZIP:</b> {customer.get('zip','')}</p>"

        # items
        html += "<hr><b>Items:</b><br>"
        for item in items:
            html += f"{item.get('name')} | Size: {item.get('size')} | ${item.get('price')}<br>"

        if status != "shipped":
            html += f"<br><a href='/ship/{order_id}'>Mark as shipped</a>"

        html += "</div>"

    return html
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
.order { border:1px solid #ddd; padding:15px; margin-bottom:10px; }
</style>

</head>
<body>

<div class="box">
<h1>Orders Admin Panel</h1>
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
