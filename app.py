from flask import Flask, jsonify

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)