from flask import Flask, request, jsonify
import requests
from capture import convert_image
import numpy as np

app = Flask(__name__)

'''
prev_board = np.array([
    ['f', 'g', '', '', '', '', '', '', '', '', '', '', '', 'u', 'r'],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', 's', 'i', 'd', '', '', '', '', '', '', 't', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', 'h', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', 'o', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', 'l', 't', 'h', '', '', '', '', '', '', 'c', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', 'o', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', 'z', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', 's', '', '', '', ''],
    ['', '', 'p', 'k', 'e', 'a', '', '', '', '', 'c', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['n', 'm', 'y', '', '', '', '', '', '', '', '', '', 'e', 'w', 'a']
])
'''
prev_board = None

@app.route('/decode_image', methods=['POST'])
def decode_image():
    global prev_board

    if 'file' not in request.files:
        err = "No image found in request"
        print(err)
        return jsonify({ "error": err })

    file = request.files['file']

    board_arr = convert_image(file, prev_board)
    prev_board = np.copy(board_arr)

    return jsonify({ "board": board_arr.tolist() })

if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True)
