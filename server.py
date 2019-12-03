from flask import Flask, request, jsonify
import requests
from capture import convert_image
import numpy as np
import gameplay.run as brain

app = Flask(__name__)

prev_board = None

@app.route('/decode_image', methods=['POST'])
def decode_image():
    global prev_board

    if 'file' not in request.files:
        err = "No image found in request"
        print(err)
        return jsonify({ "error": err })

    file = request.files['file']
    rack = request.form['rack']

    board_arr = convert_image(file, prev_board)
    prev_board = np.copy(board_arr)

    moves = brain.main(board_arr, rack)

    return jsonify({ "moves": moves })

if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True)
