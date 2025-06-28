from flask import Flask, request, render_template
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



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
