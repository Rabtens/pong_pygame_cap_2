import unittest
from unittest.mock import patch
from io import StringIO
import pygame
import sys
import random
import math
from pong import ball_animation, player_animation, opponent_ai, ball_restart

class TestPongGame(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initializing Pygame before running tests
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()

    def setUp(self):
        # Creating a StringIO object to capture stdout
        self.mock_stdout = StringIO()

        # Redirecting stdout to the StringIO object
        sys.stdout = self.mock_stdout

    def tearDown(self):
        # Resetting redirection of stdout
        sys.stdout = sys.__stdout__

    def test_ball_animation(self):
        # Mocking the Pygame functions
        with patch('pygame.mixer.Sound.play') as mock_play:
            ball_animation()
            mock_play.assert_called_once_with(pong_sound)

    def test_player_animation(self):
        global player_speed, player
        player_speed = 5
        player.y = 50

        player_animation()

        self.assertEqual(player.y, 55)  # Checking if player's y-coordinate is updated

    def test_opponent_ai(self):
        global opponent, ball
        opponent.top = 50
        ball.y = 60

        opponent_ai()

        self.assertEqual(opponent.top, 57)  # Checking if opponent's top position is updated

    def test_ball_restart(self):
        global ball_speed_x, ball_speed_y, score_time, ball
        ball_speed_x = 3
        ball_speed_y = 4
        score_time = pygame.time.get_ticks()
        ball.center = (100, 200)

        # Mocking Pygame functions
        with patch('pygame.time.get_ticks', return_value=score_time + 1500):
            ball_restart()

        self.assertEqual(ball_speed_x, 0)  # Check if ball_speed_x is reset
        self.assertEqual(ball_speed_y, 0)  # Check if ball_speed_y is reset
        self.assertEqual(ball.center, (screen_width/2, screen_height/2))  # Check if ball is centered

    def test_check_for_win_player_wins(self):
        global player_score, opponent_score, screen, screen_width, screen_height, game_font, orange
        player_score = 5
        opponent_score = 3

        # Mocking Pygame functions
        with patch('pygame.mixer.Sound.play') as mock_play:
            with patch('pygame.display.flip') as mock_flip:
                with patch('pygame.time.delay') as mock_delay:
                    check_for_win()

        mock_play.assert_called_once_with(congrats_sound)
        mock_flip.assert_called_once()
        mock_delay.assert_called_once_with(2000)
        self.assertEqual(sys.stdout.getvalue().strip(), 'Player Wins!')

    def test_check_for_win_opponent_wins(self):
        global player_score, opponent_score, screen, screen_width, screen_height, game_font, orange
        player_score = 3
        opponent_score = 5

        # Mocking Pygame functions
        with patch('pygame.mixer.Sound.play') as mock_play:
            with patch('pygame.display.flip') as mock_flip:
                with patch('pygame.time.delay') as mock_delay:
                    check_for_win()

        mock_play.assert_called_once_with(congrats_sound)
        mock_flip.assert_called_once()
        mock_delay.assert_called_once_with(2000)
        self.assertEqual(sys.stdout.getvalue().strip(), 'Opponent Wins!')

if __name__ == '__main__':
    unittest.main()
