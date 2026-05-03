@app.route("/orders")
def orders_page():

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

        html += "<div style='border:1px solid black; padding:10px; margin:10px;'>"

        html += f"<p><b>ID:</b> {order_id}</p>"
        html += f"<p><b>Status:</b> {status}</p>"

        # 👤 CUSTOMER INFO
        html += f"<p><b>Name:</b> {customer.get('name','')}</p>"
        html += f"<p><b>Phone:</b> {customer.get('phone','')}</p>"
        html += f"<p><b>Address:</b> {customer.get('address','')}</p>"
        html += f"<p><b>Country:</b> {customer.get('country','')}</p>"
        html += f"<p><b>ZIP:</b> {customer.get('zip','')}</p>"

        # 🛒 ITEMS
        html += "<hr><b>Items:</b><br>"
        for item in items:
            name = item.get("name", "")
            size = item.get("size", "")
            price = item.get("price", "")

            html += f"<p>{name} | Size: {size} | ${price}</p>"

        # 📦 ship button
        if status != "shipped":
            html += f"<a href='/ship/{order_id}'>Mark as shipped</a>"

        html += "</div>"

    return html
