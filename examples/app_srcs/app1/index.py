from flask import Flask, jsonify
import random
import requests
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/api/get_average_power")
def GetAvgPower():
    return jsonify({
        'message': 'success',
        'value': random.randrange(100,150)
    })


@app.route("/api/get_hello")
def GetHello():
    return requests.get('http://172.25.0.1:5001/').content


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
