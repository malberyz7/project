from flask import Flask, jsonify, send_file
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Главная страница — отдаём frontend.html
@app.route("/")
def home():
    frontend_path = os.path.join(os.path.dirname(__file__), 'frontend.html')
    return send_file(frontend_path)


# API endpoint
@app.route('/api/message', methods=['GET'])
def get_message():
    return jsonify({
        'message': 'Когда будем работать пацаны?'
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)