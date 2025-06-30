from flask import Flask, jsonify, render_template,request
from db.mongo import collection
# from bot.notify import send_alert
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def dashboard():
    data = list(collection.find().sort("time", -1).limit(20))
    return render_template("dashboard.html", data=data)

@app.route("/update", methods=["POST"])
def update():
    temp = float(request.form["temp"])
    humidity = float(request.form["humidity"])
    soil = int(request.form["soil"])

    doc = {
        "temp": temp,
        "humidity": humidity,
        "soil": soil,
        "time": datetime.now()
    }
    collection.insert_one(doc)

    if soil < 300:
        send_alert("🌱 ความชื้นในดินต่ำมาก! ดินแห้ง")
    return "OK"

@app.route("/api/latest")
def api_latest():
    latest = collection.find_one(sort=[("time", -1)])
    if not latest:
        return jsonify({"temp": 0, "humidity": 0, "soil": 0})
    
    return jsonify({
        "temp": latest.get("temp", 0),
        "humidity": latest.get("humidity", 0),
        "soil": latest.get("soil", 0),
        "time": latest.get("time")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
