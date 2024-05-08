from flask import Flask, render_template, session, request, jsonify, url_for
from boggle import Boggle
from flask_debugtoolbar import DebugToolbarExtension
from unittest import TestCase


app = Flask(__name__)

app.config['SECRET_KEY'] = "BurbujaBruja"

debug = DebugToolbarExtension(app)

boggle_game = Boggle()


@app.route('/')
def start_page():
    """route to start boggle game"""
    board = boggle_game.make_board()
    session['board'] = board
    return render_template('index.html', board=board)

@app.route('/submit_guess', methods=['POST'])
def submit_guess():
    # get the guess from the request data
    guess = request.json['guess']
    # check if guess is a valid word
    result = boggle_game.check_valid_word(session['board'], guess)
    # return the result as JSON
    res = {'result': result}
    return jsonify(res)