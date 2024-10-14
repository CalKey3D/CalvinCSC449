import unittest
from SOS import SOSGame

class MockGUI:
    def show_message(self, message):
        pass  # Mock implementation; you can log or assert if needed.

class TestBoardSizeSelection(unittest.TestCase):
    def test_board_size_selection(self):
        game = SOSGame(5, 'simple')
        self.assertEqual(len(game.board), 5)
        self.assertEqual(len(game.board[0]), 5)

class TestGameModeSelection(unittest.TestCase):
    def test_game_mode_selection_simple(self):
        game = SOSGame(3, 'simple')
        self.assertEqual(game.game_mode, 'simple')

    def test_game_mode_selection_general(self):
        game = SOSGame(3, 'general')
        self.assertEqual(game.game_mode, 'general')

    def test_game_end_in_simple_mode(self):
        game = SOSGame(3, 'simple')
        gui = MockGUI()
        game.make_move(0, 0, 'S', gui)
        game.make_move(0, 1, 'O', gui)
        game.make_move(0, 2, 'S', gui)
        self.assertTrue(game.game_over)

    def test_game_end_in_general_mode(self):
        game = SOSGame(3, 'general')
        gui = MockGUI()
        moves = [(0, 0, 'S'), (0, 1, 'O'), (0, 2, 'S'), (1, 0, 'S'), (1, 1, 'O')]
        for pos in moves:
            game.make_move(pos[0], pos[1], pos[2], gui)  # Pass mock GUI
        self.assertFalse(game.game_over)  # Game shouldn't be over until the board is filled

class TestSimpleGameMoves(unittest.TestCase):
    def test_player_move_in_simple_game(self):
        game = SOSGame(3, 'simple')
        gui = MockGUI()
        self.assertTrue(game.make_move(0, 0, 'S', gui))  # Pass mock GUI
        self.assertEqual(game.board[0][0], 'S')

    def test_invalid_move_in_simple_game(self):
        game = SOSGame(3, 'simple')
        gui = MockGUI()
        game.make_move(0, 0, 'S', gui)  # Pass mock GUI
        with self.assertRaises(ValueError) as context:
            game.make_move(0, 0, 'O', gui)  # Cannot place a symbol in an occupied spot
        self.assertEqual(str(context.exception), "Invalid move: Position (0, 0) is already occupied.")

class TestGeneralGameMoves(unittest.TestCase):
    def test_player_move_in_general_game(self):
        game = SOSGame(3, 'general')
        gui = MockGUI()
        self.assertTrue(game.make_move(1, 1, 'S', gui))  # Pass mock GUI
        self.assertEqual(game.board[1][1], 'S')

    def test_sos_recognition_in_general_game(self):
        game = SOSGame(3, 'general')
        gui = MockGUI()
        game.make_move(0, 0, 'S', gui)  # Pass mock GUI
        game.make_move(0, 1, 'O', gui)  # Pass mock GUI
        self.assertTrue(game.make_move(0, 2, 'S', gui))  # Should recognize SOS and allow another move

    def test_invalid_move_in_general_game(self):
        game = SOSGame(3, 'general')
        gui = MockGUI()
        game.make_move(1, 1, 'S', gui)  # Pass mock GUI
        with self.assertRaises(ValueError) as context:
            game.make_move(1, 1, 'O', gui)  # Cannot place a symbol in an occupied spot
        self.assertEqual(str(context.exception), "Invalid move: Position (1, 1) is already occupied.")

    def test_game_over_move(self):
        game = SOSGame(3, 'general')
        gui = MockGUI()
        game.make_move(0, 0, 'S', gui)  # Pass mock GUI
        game.make_move(0, 1, 'O', gui)  # Pass mock GUI
        game.make_move(0, 2, 'S', gui)  # This should end the game

        # Set the game over state explicitly to ensure that the game is recognized as over
        game.game_over = True

        # Attempting to make a move after game over
        with self.assertRaises(Exception) as context:
            game.make_move(1, 1, 'S', gui)  # Attempting to make a move after game over

        self.assertEqual(str(context.exception), "Game is over; no more moves allowed.")


if __name__ == '__main__':
    unittest.main()

