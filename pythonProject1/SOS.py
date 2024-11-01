import tkinter as tk
from tkinter import messagebox

class SOSGame:
    def __init__(self, board_size, game_mode):
        self.board_size = board_size
        self.game_mode = game_mode
        self.board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = 'blue'
        self.player_choice = {'blue': 'S', 'red': 'S'}  # Default choice for each player
        self.sos_count = {'blue': 0, 'red': 0}
        self.game_over = False
        self.game_over_counter = 0
        self.game_over_max = board_size ** 2

    def make_move(self, row, col, symbol, gui):
        if self.game_over:
            raise Exception("Game is over; no more moves allowed.")

        if self.board[row][col] != ' ':
            gui.show_message("Invalid move! Cell is already occupied or the game is over.")
            raise ValueError(f"Invalid move: Position ({row}, {col}) is already occupied.")

        self.board[row][col] = symbol

        # increment counter that is used to detect full board
        # game over if counter hits the max
        self.game_over_counter += 1
        if self.game_over_counter >= self.game_over_max:
            self.game_over = True

        sos_count = self.check_sos(row, col, symbol)
        if sos_count > 0:
            self.sos_count[self.current_player] += sos_count

            if self.game_mode == 'simple':
                self.game_over = True
        self.current_player = 'red' if self.current_player == 'blue' else 'blue'
        return True

    def check_sos(self, row, col, symbol):

        if symbol == 'S':
            return self.check_sequence_s(row, col)
        if symbol == 'O':
            return self.check_sequence_o(row, col)

    def check_sequence_o(self, row, col):

        sequences_found = 0
        pairs = [[(-1, 0), (1, 0)],  # Vertical
                 [(-1, 1), (1, -1)], # y=x
                 [(0, -1), (0, 1)],  # horizontal
                 [(-1, -1), (1, 1)]]  # y=-x

        for pair in pairs:
            s = 0
            for tup in pair:
                try:
                    if row + tup[0] < 0 or col + tup[1] < 0:
                        continue
                    if self.board[row + tup[0]][col + tup[1]] == 'S':
                        s += 1
                except IndexError:
                    print("index error")
                    break
            if s == 2:
                sequences_found += 1
                print("sequence found")
        return sequences_found

    def check_sequence_s(self, row, col):

        sequences_found = 0
        pairs = [[(-1, 0), (-2, 0)],  # up
                 [(-1, 1), (-2, 2)],  # up right
                 [(0, 1), (0, 2)],  # right
                 [(1, 1), (2, 2)],  # down right
                 [(1, 0), (2, 0)],  # down
                 [(1, -1), (2, -2)],  # down left
                 [(0, -1), (0, -2)],  # left
                 [(-1, -1), (-2, -2)]]  # up left

        for pair in pairs:
            try:
                if row + pair[0][0] < 0 or col + pair[0][1] < 0:
                    continue
                if self.board[row + pair[0][0]][col + pair[0][1]] != 'O':
                    continue
                if row + pair[1][0] < 0 or col + pair[1][1] < 0:
                    continue
                if self.board[row + pair[1][0]][col + pair[1][1]] == 'S':
                    sequences_found += 1
                    print("sequence found")
            except IndexError:
                print("index error")
                continue
        return sequences_found

    def get_board(self):
        return self.board

    def reset_game(self):
        self.board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = 'blue'
        self.sos_count = {'blue': 0, 'red': 0}
        self.game_over = False
        self.game_over_counter = 0

class SOSGUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.buttons = {}
        self.symbol_choice = tk.StringVar(value='S')  # Default to 'S'
        self.create_board()
        self.create_controls()

    def create_board(self):
        for row in range(self.game.board_size):
            for col in range(self.game.board_size):
                button = tk.Button(self.root, text=' ', width=5, height=2,
                                   command=lambda r=row, c=col: self.on_button_click(r, c))
                button.grid(row=row, column=col)
                self.buttons[(row, col)] = button

    def create_controls(self):
        # Add radio buttons for symbol selection
        symbol_frame = tk.Frame(self.root)
        symbol_frame.grid(row=self.game.board_size, column=0, columnspan=self.game.board_size)
        tk.Label(symbol_frame, text="Choose symbol: ").pack(side=tk.LEFT)
        tk.Radiobutton(symbol_frame, text='S', variable=self.symbol_choice, value='S').pack(side=tk.LEFT)
        tk.Radiobutton(symbol_frame, text='O', variable=self.symbol_choice, value='O').pack(side=tk.LEFT)

        # Add Replay button
        replay_button = tk.Button(symbol_frame, text="Replay", command=self.reset_board)
        replay_button.pack(side=tk.LEFT)

        # Add Turn label
        self.turn_label = tk.Label(symbol_frame, text="Blue's Turn", fg="blue")
        self.turn_label.pack(side=tk.LEFT)

    def on_button_click(self, row, col):
        symbol = self.symbol_choice.get()
        if self.game.make_move(row, col, symbol, self):  # Pass self as the GUI instance
            self.update_board()
            if self.game.game_over:
                winner = 'Red' if self.game.current_player == 'blue' else 'Blue'
                messagebox.showinfo("Game Over", f"{winner} wins!")
            else:
                self.update_turn_label()

    def update_board(self):
        for row in range(self.game.board_size):
            for col in range(self.game.board_size):
                self.buttons[(row, col)].config(text=self.game.board[row][col])

    def update_turn_label(self):
        if self.game.current_player == 'blue':
            self.turn_label.config(text="Blue's Turn", fg="blue")
        else:
            self.turn_label.config(text="Red's Turn", fg="red")

    def reset_board(self):
        self.game.reset_game()
        self.update_board()
        self.turn_label.config(text="Blue's Turn", fg="blue")  # Reset turn to Blue

    def show_message(self, message):
        # Show an error message using a message box
        messagebox.showerror("Error", message)

if __name__ == '__main__':
    # Run the game GUI
    root = tk.Tk()
    root.title("SOS Game")
    board_size = int(input("Enter board size (greater than 2): "))
    game_mode = input("Enter game mode (simple/general): ")
    game = SOSGame(board_size, game_mode)
    gui = SOSGUI(root, game)
    root.mainloop()

    # Run tests
    import unittest
    unittest.main(module='test_SOSGame', exit=False)
