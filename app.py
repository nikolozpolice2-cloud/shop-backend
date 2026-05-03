from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

orders = []

@app.route("/")
def home():
    return "API WORKING"


# 🛒 order receive
@app.route("/order", methods=["POST"])
def order():
    data = request.json
    
    data["status"] = "pending"   # status default
    
    orders.append(data)

    print("NEW ORDER:", data)

    return jsonify({"status": "ok"})


# 📦 mark as shipped
@app.route("/ship/<int:index>")
def ship_order(index):
    if index < len(orders):
        orders[index]["status"] = "shipped"
    return "OK"


# 📋 admin panel
@app.route("/orders")
def orders_page():
    html = "<h1>Orders</h1>"

    for i, o in enumerate(orders):
        html += "<div style='border:1px solid black; padding:10px; margin:10px;'>"
        
        status = o.get("status", "pending")
        html += f"<p>Status: <b>{status}</b></p>"

        if "items" in o:
            for item in o["items"]:
                name = item.get("name", "No name")
                size = item.get("size", "No size")
                
                html += f"<p>{name} - Size: {size}</p>"

        # ✅ button
        if status != "shipped":
            html += f"<br><a href='/ship/{i}'>Mark as shipped</a>"

        html += "</div>"

    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
