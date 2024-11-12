import unittest
from SOS import SOSSimpleGame, SOSGeneralGame, CPU

class MockGUI:
    def show_message(self, message):
        pass  # Mock implementation; you can log or assert if needed.

class TestBoardSizeSelection(unittest.TestCase):
    def test_board_size_selection(self):
        CPU_instance = CPU()
        game = SOSSimpleGame(5, CPU_instance)
        self.assertEqual(len(game.board), 5)
        self.assertEqual(len(game.board[0]), 5)

class TestSimpleGameMode(unittest.TestCase):
    def test_game_end_in_simple_mode(self):
        CPU_instance = CPU()
        game = SOSSimpleGame(3, CPU_instance)
        gui = MockGUI()
        game.make_move(0, 0, 'S', gui)  # blue
        game.make_move(0, 1, 'O', gui)  # red
        game.make_move(0, 2, 'S', gui)  # blue
        self.assertTrue(game.game_over)

    def test_sos_in_simple_game_ends_game(self):
        CPU_instance = CPU()
        game = SOSSimpleGame(3, CPU_instance)
        gui = MockGUI()
        game.make_move(1, 0, 'S', gui)  # blue
        game.make_move(1, 1, 'O', gui)  # red
        game.make_move(1, 2, 'S', gui)  # blue
        self.assertTrue(game.game_over)
        previous_player = 'red' if game.current_player == 'blue' else 'blue'
        self.assertEqual(game.sos_count[previous_player], 1)

class TestGeneralGameMode(unittest.TestCase):
    def test_game_end_in_general_mode(self):
        CPU_instance = CPU()
        game = SOSGeneralGame(3, CPU_instance)
        gui = MockGUI()
        moves = [(0, 0, 'S'), (0, 1, 'O'), (0, 2, 'S'), (1, 0, 'S'), (1, 1, 'O')]
        for row, col, symbol in moves:
            game.make_move(row, col, symbol, gui)
        self.assertFalse(game.game_over)

    def test_full_board_in_general_game(self):
        CPU_instance = CPU()
        game = SOSGeneralGame(3, CPU_instance)
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
        CPU_instance = CPU()
        game = SOSSimpleGame(3, CPU_instance)
        gui = MockGUI()
        game.make_move(0, 0, 'S', gui)
        self.assertEqual(game.board[0][0], 'S')

    def test_invalid_move_in_simple_game(self):
        CPU_instance = CPU()
        game = SOSSimpleGame(3, CPU_instance)
        gui = MockGUI()
        game.make_move(0, 0, 'S', gui)
        with self.assertRaises(ValueError) as context:
            game.make_move(0, 0, 'O', gui)
        self.assertEqual(str(context.exception), "Invalid move: Position (0, 0) is already occupied.")

class TestGeneralGameMoves(unittest.TestCase):
    def test_player_move_in_general_game(self):
        CPU_instance = CPU()
        game = SOSGeneralGame(3, CPU_instance)
        gui = MockGUI()
        game.make_move(1, 1, 'S', gui)
        self.assertEqual(game.board[1][1], 'S')

    def test_sos_recognition_in_general_game(self):
        CPU_instance = CPU()
        game = SOSGeneralGame(3, CPU_instance)
        gui = MockGUI()
        game.current_player = 'blue'
        game.make_move(0, 0, 'S', gui)  # blue
        game.make_move(0, 1, 'O', gui)  # red
        game.make_move(0, 2, 'S', gui)  # blue
        previous_player = 'red' if game.current_player == 'blue' else 'blue'
        self.assertEqual(game.sos_count[previous_player], 1)

    def test_invalid_move_in_general_game(self):
        CPU_instance = CPU()
        game = SOSGeneralGame(3, CPU_instance)
        gui = MockGUI()
        game.make_move(1, 1, 'S', gui)
        with self.assertRaises(ValueError) as context:
            game.make_move(1, 1, 'O', gui)
        self.assertEqual(str(context.exception), "Invalid move: Position (1, 1) is already occupied.")

    def test_game_over_move(self):
        CPU_instance = CPU()
        game = SOSGeneralGame(3, CPU_instance)
        gui = MockGUI()
        game.make_move(0, 0, 'S', gui)
        game.make_move(0, 1, 'O', gui)
        game.make_move(0, 2, 'S', gui)
        game.game_over = True
        with self.assertRaises(Exception) as context:
            game.make_move(1, 1, 'S', gui)
        self.assertEqual(str(context.exception), "Game is over; no more moves allowed.")

class TestGameModeSelection(unittest.TestCase):
    def test_game_mode_selection_simple(self):
        CPU_instance = CPU()
        game = SOSSimpleGame(3, CPU_instance)
        self.assertIsInstance(game, SOSSimpleGame)
        self.assertNotIsInstance(game, SOSGeneralGame)

    def test_game_mode_selection_general(self):
        CPU_instance = CPU()
        game = SOSGeneralGame(3, CPU_instance)
        self.assertIsInstance(game, SOSGeneralGame)
        self.assertNotIsInstance(game, SOSSimpleGame)

class TestWinnerCheckInFullGeneralGame(unittest.TestCase):
    def test_winner_by_sequence_count(self):
        CPU_instance = CPU()
        game = SOSGeneralGame(3, CPU_instance)
        gui = MockGUI()
        moves = [
            (0, 0, 'S'),  # Blue
            (0, 1, 'O'),  # Red
            (0, 2, 'S'),  # Blue
            (1, 0, 'O'),  # Red
            (1, 1, 'S'),  # Blue
            (1, 2, 'O'),  # Red
            (2, 0, 'S'),  # Blue
            (2, 1, 'O'),  # Red
            (2, 2, 'S')   # Blue
        ]
        game.current_player = 'blue'
        for row, col, symbol in moves:
            game.make_move(row, col, symbol, gui)
        self.assertTrue(game.game_over)
        self.assertGreater(game.sos_count['blue'], game.sos_count['red'])

class TestComputerOpponent(unittest.TestCase):
    #AC 8.1
    def test_select_computer_opponent(self):

        CPU_instance = CPU()
        game = SOSSimpleGame(3, CPU_instance)
        gui = MockGUI()

        # Simulate selecting the computer as the red player
        game.CPU_Player['red'] = True
        self.assertTrue(game.CPU_Player['red'])
        self.assertFalse(game.CPU_Player['blue'])

    #AC 8.2
    def test_computer_makes_valid_move(self):

        CPU_instance = CPU()
        game = SOSSimpleGame(3, CPU_instance)
        gui = MockGUI()

        # Set red player as computer and current player
        game.CPU_Player['red'] = True
        game.current_player = 'red'

        # Capture the initial empty cells
        empty_cells_before = [(r, c) for r in range(3) for c in range(3) if game.board[r][c] == ' ']

        # Simulate the computer's turn
        row, col, symbol = game.CPU.calculate_move(game.board)
        game.make_move(row, col, symbol, gui)

        # Verify the move
        self.assertEqual(game.board[row][col], symbol)
        self.assertIn((row, col), empty_cells_before)

    # AC 9.1
    def test_computer_vs_computer_mode(self):

        CPU_instance = CPU()
        game = SOSGeneralGame(3, CPU_instance)
        gui = MockGUI()

        # Set both players as computers
        game.CPU_Player['blue'] = True
        game.CPU_Player['red'] = True

        self.assertTrue(game.CPU_Player['blue'])
        self.assertTrue(game.CPU_Player['red'])

    # AC 9.2
    def test_automatic_gameplay(self):

        CPU_instance = CPU()
        game = SOSGeneralGame(3, CPU_instance)
        gui = MockGUI()

        # Set both players as computers
        game.CPU_Player['blue'] = True
        game.CPU_Player['red'] = True

        # Simulate automatic gameplay until the game is over
        while not game.game_over:
            current_player = game.current_player
            row, col, symbol = game.CPU.calculate_move(game.board)
            game.make_move(row, col, symbol, gui)
            self.assertEqual(game.board[row][col], symbol)

        # Verify that the game ended
        self.assertTrue(game.game_over)

        # Checks that the board is full or that other game over conditions are met
        empty_cells = [(r, c) for r in range(game.board_size) for c in range(game.board_size) if game.board[r][c] == ' ']
        self.assertEqual(len(empty_cells), 0)

if __name__ == '__main__':
    unittest.main()

