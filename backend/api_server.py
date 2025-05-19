from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow requests from frontend on a different port

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    value = data.get('userInput')
    print(f"Received input: {value}")
    return jsonify({'message': f"You submitted: {value}"})

if __name__ == '__main__':
    app.run(port=5001)
