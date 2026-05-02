from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/order", methods=["POST"])
def order():
    data = request.json
    print("ORDER RECEIVED:", data)
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)