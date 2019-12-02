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

'''
brain_url = "http://127.0.0.1:3001"

# performs a player turn and a bot turn
@app.route('/round', methods=['POST'])
def game_round():
    if 'file' not in request.files:
        err = "No image found in request"
        print(err)
        return jsonify({ "error": err })

    file = request.files['file']

    # TODO: process image, get current board state
    boardArr = process_image(file)

    try:
        res = requests.post(brain_url, json={ "board": boardArr })
        # TODO: if data['result'] exists (ie. game is done), should send back as well
        data = res.json();
        return jsonify({ "board": data["board"] })
    except:
        err = "Error with HTTP req to brain"
        print(err)
        return jsonify({ "error": err })
'''
