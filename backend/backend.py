from flask import Flask, jsonify, send_file
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    # Путь к frontend.html в папке frontend относительно корня проекта
    project_root = os.path.dirname(os.path.dirname(__file__))
    frontend_path = os.path.join(project_root, 'frontend', 'frontend.html')
    return send_file(frontend_path)


@app.route('/api/message', methods=['GET'])
def get_message():
    return jsonify({
        'message': 'Когда будем работать пацаны?'
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)