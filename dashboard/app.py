from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

BACKEND_API = "http://backend:5000/api/latest"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    try:
        r = requests.get(BACKEND_API, timeout=3)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
