from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json

app = Flask(__name__)
CORS(app)

# 📦 create DB
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


# 🏠 home
@app.route("/")
def home():
    return "API WORKING"


# 🛒 new order
@app.route("/order", methods=["POST"])
def order():
    data = request.json

    conn = sqlite3.connect("orders.db")
    c = conn.cursor()

    c.execute("INSERT INTO orders (data, status) VALUES (?, ?)", 
              (json.dumps(data), "pending"))

    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})


# 📦 ship order
@app.route("/ship/<int:id>")
def ship_order(id):
    conn = sqlite3.connect("orders.db")
    c = conn.cursor()

    c.execute("UPDATE orders SET status='shipped' WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return "OK"


# 📋 admin panel
@app.route("/orders")
def orders_page():
    conn = sqlite3.connect("orders.db")
    c = conn.cursor()

    c.execute("SELECT * FROM orders")
    rows = c.fetchall()

    html = "<h1>Orders</h1>"

    for row in rows:
        id = row[0]
        data = json.loads(row[1])
        status = row[2]

        html += "<div style='border:1px solid black; padding:10px; margin:10px;'>"
        html += f"<p><b>ID:</b> {id}</p>"
        html += f"<p><b>Status:</b> {status}</p>"

        html += f"<p><b>Name:</b> {data.get('name','')}</p>"
        html += f"<p><b>Phone:</b> {data.get('phone','')}</p>"
        html += f"<p><b>Address:</b> {data.get('address','')}</p>"
        html += f"<p><b>Country:</b> {data.get('country','')}</p>"
        html += f"<p><b>ZIP:</b> {data.get('zip','')}</p>"

        if "items" in data:
            for item in data["items"]:
                html += f"<p>{item.get('name')} - Size: {item.get('size')}</p>"

        if status != "shipped":
            html += f"<a href='/ship/{id}'>Mark as shipped</a>"

        html += "</div>"

    conn.close()
    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
