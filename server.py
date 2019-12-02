from flask import Flask, request, jsonify
import requests
from capture import convert_image

app = Flask(__name__)

@app.route('/decode_image', methods=['POST'])
def decode_image():
    if 'file' not in request.files:
        err = "No image found in request"
        print(err)
        return jsonify({ "error": err })

    file = request.files['file']

    board_arr = convert_image(file)

    return jsonify({ "board": board_arr })

if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True)
