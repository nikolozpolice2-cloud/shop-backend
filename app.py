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

@app.route("/orders", methods=["GET"])
def get_orders():
    return jsonify(orders)  # ⬅️ აქ ნახავ ყველას

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
