import unittest
from SOS import SOSSimpleGame, SOSGeneralGame

class MockGUI:
    def show_message(self, message):
        pass  # Mock implementation; you can log or assert if needed.

class TestBoardSizeSelection(unittest.TestCase):
    def test_board_size_selection(self):
        game = SOSSimpleGame(5)
        self.assertEqual(len(game.board), 5)
        self.assertEqual(len(game.board[0]), 5)

class TestSimpleGameMode(unittest.TestCase):
    def test_game_end_in_simple_mode(self):
        game = SOSSimpleGame(3)
        gui = MockGUI()
        game.make_move(0, 0, 'S', gui)
        game.make_move(0, 1, 'O', gui)
        game.make_move(0, 2, 'S', gui)
        self.assertTrue(game.game_over)

    def test_sos_in_simple_game_ends_game(self):
        game = SOSSimpleGame(3)
        gui = MockGUI()
        game.make_move(1, 0, 'S', gui)
        game.make_move(1, 1, 'O', gui)
        game.make_move(1, 2, 'S', gui)
        self.assertTrue(game.game_over)
        self.assertEqual(game.sos_count[game.current_player], 1)

class TestGeneralGameMode(unittest.TestCase):
    def test_game_end_in_general_mode(self):
        game = SOSGeneralGame(3)
        gui = MockGUI()
        moves = [(0, 0, 'S'), (0, 1, 'O'), (0, 2, 'S'), (1, 0, 'S'), (1, 1, 'O')]
        for pos in moves:
            game.make_move(pos[0], pos[1], pos[2], gui)
        self.assertFalse(game.game_over)

    def test_full_board_in_general_game(self):
        game = SOSGeneralGame(3)
        gui = MockGUI()
        moves = [
            (0, 0, 'S'), (0, 1, 'O'), (0, 2, 'S'),
            (1, 0, 'O'), (1, 1, 'S'), (1, 2, 'O'),
            (2, 0, 'S'), (2, 1, 'O'), (2, 2, 'S')
        ]
        for row, col, symbol in moves:
            game.make_move(row, col, symbol, gui)
        self.assertTrue(game.game_over)

class TestSimpleGameMoves(unittest.TestCase):
    def test_player_move_in_simple_game(self):
        game = SOSSimpleGame(3)
        gui = MockGUI()
        game.make_move(0, 0, 'S', gui)
        self.assertEqual(game.board[0][0], 'S')

    def test_invalid_move_in_simple_game(self):
        game = SOSSimpleGame(3)
        gui = MockGUI()
        game.make_move(0, 0, 'S', gui)
        with self.assertRaises(ValueError) as context:
            game.make_move(0, 0, 'O', gui)
        self.assertEqual(str(context.exception), "Invalid move: Position (0, 0) is already occupied.")

class TestGeneralGameMoves(unittest.TestCase):
    def test_player_move_in_general_game(self):
        game = SOSGeneralGame(3)
        gui = MockGUI()
        game.make_move(1, 1, 'S', gui)
        self.assertEqual(game.board[1][1], 'S')

    def test_sos_recognition_in_general_game(self):
        game = SOSGeneralGame(3)
        gui = MockGUI()
        game.current_player = 'blue'
        game.make_move(0, 0, 'S', gui)
        game.make_move(0, 1, 'O', gui)
        game.make_move(0, 2, 'S', gui)
        self.assertEqual(game.sos_count['blue'], 1)

    def test_invalid_move_in_general_game(self):
        game = SOSGeneralGame(3)
        gui = MockGUI()
        game.make_move(1, 1, 'S', gui)
        with self.assertRaises(ValueError) as context:
            game.make_move(1, 1, 'O', gui)
        self.assertEqual(str(context.exception), "Invalid move: Position (1, 1) is already occupied.")

    def test_game_over_move(self):
        game = SOSGeneralGame(3)
        gui = MockGUI()
        game.make_move(0, 0, 'S', gui)
        game.make_move(0, 1, 'O', gui)
        game.make_move(0, 2, 'S', gui)

        game.game_over = True

        with self.assertRaises(Exception) as context:
            game.make_move(1, 1, 'S', gui)
        self.assertEqual(str(context.exception), "Game is over; no more moves allowed.")

#Written by ChatGPT
class TestGameModeSelection(unittest.TestCase):
    def test_game_mode_selection_simple(self):
        game = SOSSimpleGame(3)
        self.assertIsInstance(game, SOSSimpleGame)
        self.assertNotIsInstance(game, SOSGeneralGame)

    def test_game_mode_selection_general(self):
        game = SOSGeneralGame(3)
        self.assertIsInstance(game, SOSGeneralGame)
        self.assertNotIsInstance(game, SOSSimpleGame)

# Written by ChatGPT
class TestWinnerCheckInFullGeneralGame(unittest.TestCase):
    def test_winner_by_sequence_count(self):
        game = SOSGeneralGame(3)
        gui = MockGUI()
        moves = [
            (0, 0, 'S'), (0, 1, 'O'), (0, 2, 'S'),  # blue forms SOS
            (1, 0, 'S'), (1, 1, 'O'), (1, 2, 'S'),  # red forms SOS
            (2, 0, 'O'), (2, 1, 'S'), (2, 2, 'O')   # blue forms SOS
        ]
        game.current_player = 'blue'
        for row, col, symbol in moves[:3]:
            game.make_move(row, col, symbol, gui)
        game.change_turn()
        for row, col, symbol in moves[3:6]:
            game.make_move(row, col, symbol, gui)
        game.change_turn()
        for row, col, symbol in moves[6:]:
            game.make_move(row, col, symbol, gui)

        self.assertTrue(game.game_over)
        self.assertGreater(game.sos_count['blue'], game.sos_count['red'])

if __name__ == '__main__':
    unittest.main()
