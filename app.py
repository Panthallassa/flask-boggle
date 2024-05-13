from flask import Flask, render_template, session, request, jsonify, redirect
from boggle import Boggle
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SECRET_KEY'] = "BurbujaBruja"
debug = DebugToolbarExtension(app)
boggle_game = Boggle()

total_score = 0
num_games_played = 0
highest_score = 0

@app.route('/')
def start_page():
    """Route to start boggle game"""
    global total_score
    # session.clear()

    board = boggle_game.make_board()
    session['board'] = board
    print(session['board'])
    # reset total score
    total_score = 0

    session['highest_score'] = highest_score
    session['num_games_played'] = num_games_played

    # highest_score = session.get('highest_score', 0)
    # num_games_played = session.get('num_games_played', 0)

    return render_template('index.html', board=board, score=total_score, highest_score=highest_score, num_games_played=num_games_played)

@app.route('/submit_guess', methods=['POST'])
def submit_guess():
    """route that submits the user's guess"""
    global total_score
    # get the guess from the request data
    guess = request.json['guess']
    if 'board' not in session:
        return jsonify({'error': 'No board found in session'}), 400
        # check if guess is a valid word
    result = boggle_game.check_valid_word(session['board'], guess)
    if result == 'ok':
        # calculate score
        score = calculate_score(guess)
        total_score += score
    # return the result as JSON
    res = {'result': result, 'score': total_score}
    return jsonify(res)

def calculate_score(guess):
    """Calculate score based on the values from the guess"""
    score = len(guess)
    return score

@app.route('/game-over', methods=['POST', 'GET'])
def game_over():
    """Route to handle game over"""
    global num_games_played, highest_score

    if request.method == 'POST':
        data = request.json
        score = data.get('score')
        score = int(score)

        if score > highest_score:
             highest_score = score
    
        num_games_played += 1

        session['highest_score'] = highest_score
        session['num_games_played'] = num_games_played

        return jsonify({'message': 'Score received successfully.'}), 200
    else:
        return render_template('game_over.html', highest_score=highest_score, num_games_played=num_games_played)