from flask import Flask, jsonify
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_version() -> str:
    path = os.path.join(BASE_DIR, "version.txt")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip() or "dev"
    except FileNotFoundError:
        return "dev"


app = Flask(__name__)


@app.route('/')
def home():
    return "Czesc! Aplikacja dziala. Zaliczenie DevOps."


@app.route('/products')
def products():
    data = [
        {"id": 1, "name": "Laptop"},
        {"id": 2, "name": "Myszka"}
    ]
    return jsonify(data)


@app.route('/version')
def version():
    return jsonify({"version": get_version()})


@app.route('/health')
def health():
    return "OK", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
