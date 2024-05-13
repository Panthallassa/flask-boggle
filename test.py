from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Set up testing environment"""
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.boggle_game = Boggle()

    def test_start_page(self):
        """Test start_page route"""
        with self.client as client:
            response = client.get('/')
            # check if response is successful
            self.assertEqual(response.status_code, 200)
            # check if expected HTML is present
            self.assertIn(b"<h1>Let's Play Boggle</h1>", response.data)
            with client.session_transaction() as sess:
                # check if board key is present in session
                self.assertIn('board', sess)
                # check if stored board matches the one showing
                self.assertEqual(sess['board'], self.boggle_game.make_board())
                # check if higheset_score key is present in session
                self.assertIn('highest_score', sess)
                # ensure that the highest score varibale is correctly initialized to 0 in the session
                self.assertEqual(sess['highest_score'], 0)
                # checks that num_games_played is in session
                self.assertIn('num_games_played', sess)
                # check that the num_games_played is initialized as 0 iin the session
                self.assertEqual(sess['num_games_played'], 0)

    def test_submit_guess(self):
        """Test submit_guess route"""
        # set up session with a sample board
        with self.client.session_transaction() as sess:
            sess['board'] = [['C', 'A', 'T'], ['D', 'E', 'F'], ['G', 'H', 'I']]
            # Send a POST request with a guess
            response = self.client.post('/submit_guess', json={'guess': 'CAT'})
            # check is response is successful
            self.assertEqual(response.status_code, 200)
            # Check if the response contains expected JSON data
            data = json.loads(response.data)
            self.assertIn('result', data)
            self.assertIn('score', data)

            # check if score is correctly calculated and result 'ok'
            self.assertEqual(data['result'], 'ok')
            self.assertEqual(data['score'], 3)

        def test_game_over_post(self):
            """Test game_over route with POST request"""
            with self.client.session_transaction() as sess:
                sess['highest_score'] = 0
                sess['num_games_played'] = 0

                # Send a POST request to update the highest score
                response = self.client.post('/game-over', json={'score': 10})
                # check if the response is successful
                self.assertEqual(response.status_code, 200)

                # Check in the session variables are updated correctly 
                with self.client.session_transaction() as sess:
                    self.assertEqual(sess['highest_score'], 10)
                    self.assertEqual(sess['num_games_played'], 1)

                # Check if the response contains the expected JSON data
                data = json.loads(response.data)
                self.assertIn('message', data)
                self.assertEqual(data['message'], 'Score received successfully.')

        def test_game_over_get(self):
            """Test game_over route with GET request"""
            with self.client.session_transaction() as sess:
                sess['highest_score'] = 10
                sess['num_games_played'] = 1

                # Send a GET request to render the game over template
                response = self.client.get('/game-over')

                # Check if the response is successful
                self.assertEqual(response.status_code, 200)

                # Check if the response contains the expected HTML content
                self.assertIn(b'<h1>Game Over!</h1>', response.data)
                self.assertIn(b'Highest Score: 10', response.data)
                self.assertIn(b'Number of Times Played: 1', response.data)
