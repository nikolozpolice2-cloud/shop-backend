from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

orders = []  # აქ ინახება ყველა შეკვეთა

@app.route("/")
def home():
    return "API WORKING"

@app.route("/order", methods=["POST"])
def order():
    data = request.json
    orders.append(data)   # ⬅️ ინახავს order-ს

    print("NEW ORDER:", data)
    return jsonify({"status": "ok"})

@app.route("/orders")
def orders_page():
    html = "<h1>Orders</h1>"

    for o in orders:
        html += "<div style='border:1px solid black; padding:10px; margin:10px;'>"
        
        if "items" in o:
            for item in o["items"]:
                name = item.get("name", "No name")
                size = item.get("size", "No size")
                
                html += f"<p><b>{name}</b> - Size: {size}</p>"
        
        html += "</div>"

    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
