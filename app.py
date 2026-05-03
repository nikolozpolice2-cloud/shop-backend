from flask import Flask, request, jsonify
from flask_cors import CORS
from guara import application, it

from transactions import CreateOrder, OrderDoesNotExist, TransactionException 

app = Flask(__name__)
CORS(app)

orders = []  # აქ ინახება ყველა შეკვეთა

brain = application.Application()

@app.route("/")
def home():
    return "API WORKING"

@app.route("/order", methods=["POST"])
def order():
    data = request.json
    try:
        (
            brain.given(OrderDoesNotExist, orders=orders, order=data)
            .when(CreateOrder, orders=orders, order=data)
            .then(it.IsTrue)
        )

        print("NEW ORDER:", data)
        return jsonify({"status": "ok"})
    except TransactionException as e:
        return jsonify({"status": "fail", "error": str(e)})
         

@app.route("/orders", methods=["GET"])
def get_orders():
    return jsonify(orders)  # ⬅️ აქ ნახავ ყველას

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
