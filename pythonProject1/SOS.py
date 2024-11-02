import tkinter as tk
from tkinter import messagebox
from abc import ABC, abstractmethod

class SOSGame(ABC):
    def __init__(self, board_size):
        self.board_size = board_size
        self.board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = 'blue'
        self.player_choice = {'blue': 'S', 'red': 'S'}
        self.sos_count = {'blue': 0, 'red': 0}
        self.game_over = False
        self.game_over_counter = 0
        self.game_over_max = board_size ** 2
        self.current_turn_sequences = []  # Is reset by GUI

    @abstractmethod
    def make_move(self, row, col, symbol, gui):
        pass

    def check_sos(self, row, col, symbol):

        if symbol == 'S':
            return self.check_sequence_s(row, col)
        if symbol == 'O':
            return self.check_sequence_o(row, col)

    def change_turn(self):
        if self.current_player == 'blue':
            self.current_player = 'red'
        elif self.current_player == 'red':
            self.current_player = 'blue'
        else:
            print("Error: player color is broken")

    def check_sequence_o(self, row, col):

        pairs = [[(-1, 0), (1, 0)], [(-1, 1), (1, -1)], [(0, -1), (0, 1)], [(-1, -1), (1, 1)]]
        for pair in pairs:
            try:
                if row + pair[0][0] < 0 or col + pair[0][1] < 0:
                    continue
                if self.board[row + pair[0][0]][col + pair[0][1]] != 'S':
                    continue
                if row + pair[1][0] < 0 or col + pair[1][1] < 0:
                    continue
                if self.board[row + pair[1][0]][col + pair[1][1]] == 'S':
                    print("sequence found")
                    self.sos_count[self.current_player] += 1
                    sos_sequence = [(row + pair[1][0], col + pair[1][1]), (row, col), (row + pair[0][0], col + pair[0][1])]
                    self.current_turn_sequences.append(sos_sequence)

            except IndexError:
                continue

    def check_sequence_s(self, row, col):

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
                    print("sequence found")
                    self.sos_count[self.current_player] += 1
                    sos_sequence = [(row, col), (row + pair[0][0], col + pair[0][1]), (row + pair[1][0], col + pair[1][1])]
                    self.current_turn_sequences.append(sos_sequence)

            except IndexError:
                continue

    def get_board(self):
        return self.board

    def reset_game(self):
        self.board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = 'blue'
        self.sos_count = {'blue': 0, 'red': 0}
        self.game_over = False
        self.game_over_counter = 0

class SOSSimpleGame(SOSGame):
    def make_move(self, row, col, symbol, gui):
        if self.game_over:
            raise Exception("Game is over; no more moves allowed.")

        if self.board[row][col] != ' ':
            gui.show_message("Invalid move! Cell is already occupied or the game is over.")
            raise ValueError(f"Invalid move: Position ({row}, {col}) is already occupied.")

        self.board[row][col] = symbol
        self.game_over_counter += 1

        self.check_sos(row, col, symbol)

        self.change_turn()

        if self.game_over_counter >= self.game_over_max:
            self.game_over = True
            return

        if self.sos_count['red'] > 0 or self.sos_count['blue'] > 0:
            self.game_over = True
            return

class SOSGeneralGame(SOSGame):
    def make_move(self, row, col, symbol, gui):
        if self.game_over:
            raise Exception("Game is over; no more moves allowed.")

        if self.board[row][col] != ' ':
            gui.show_message("Invalid move! Cell is already occupied or the game is over.")
            raise ValueError(f"Invalid move: Position ({row}, {col}) is already occupied.")

        self.board[row][col] = symbol
        self.game_over_counter += 1

        self.check_sos(row, col, symbol)

        self.change_turn()

        if self.game_over_counter >= self.game_over_max:
            self.game_over = True
            return

class SOSGUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.symbol_choice = tk.StringVar(value='S')
        self.canvas = tk.Canvas(self.root, width=50 * game.board_size, height=50 * game.board_size)
        self.canvas.grid(row=0, column=0, columnspan=game.board_size)
        self.create_board()
        self.create_controls()

    def create_board(self):
        cell_size = 50
        board_size = self.game.board_size * cell_size
        self.canvas.config(width=board_size, height=board_size)
        for row in range(self.game.board_size):
            for col in range(self.game.board_size):
                x1, y1 = col * cell_size, row * cell_size
                x2, y2 = x1 + cell_size, y1 + cell_size
                # Draw each cell as a rectangle on the canvas to create grid lines
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", tags="grid")

        # Draw the outer border for the entire grid
        self.canvas.create_rectangle(2, 2, board_size, board_size, outline="black", width=1, tags="outer_border")

        # Bind mouse clicks to the canvas
        self.canvas.bind("<Button-1>", self.on_canvas_click)

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

    def on_canvas_click(self, event):
        cell_size = 50
        row, col = event.y // cell_size, event.x // cell_size
        symbol = self.symbol_choice.get()

        # Check if the move is valid, then update board and draw the symbol
        self.game.make_move(row, col, symbol, self)
        self.draw_sos_lines()
        self.update_board()
        if self.game.game_over:
            if self.game.sos_count['blue'] > self.game.sos_count['red']:
                winner = 'Blue'
            elif self.game.sos_count['blue'] < self.game.sos_count['red']:
                winner = 'Red'
            else:
                winner = 'No one'

            messagebox.showinfo("Game Over", f"{winner} wins!")
        else:
            self.update_turn_label()

    def draw_sos_lines(self):
        if self.game.current_player == 'blue':
            color = 'red'
        elif self.game.current_player == 'red':
            color = 'blue'
        cell_size = 50

        for sequence in self.game.current_turn_sequences:
            # Unpack the sequence into individual cell coordinates
            (r1, c1), (r2, c2), (r3, c3) = sequence

            # Calculate the center coordinates of each cell
            x1, y1 = c1 * cell_size + 25, r1 * cell_size + 25
            x2, y2 = c2 * cell_size + 25, r2 * cell_size + 25
            x3, y3 = c3 * cell_size + 25, r3 * cell_size + 25

            # Draw lines between the cells in the SOS sequence
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2, tags="sos_line")
            self.canvas.create_line(x2, y2, x3, y3, fill=color, width=2, tags="sos_line")

        self.game.current_turn_sequences = []

    def update_board(self):
        cell_size = 50
        self.canvas.delete("symbol")
        for row in range(self.game.board_size):
            for col in range(self.game.board_size):
                symbol = self.game.board[row][col]
                if symbol != ' ':
                    x, y = col * cell_size + cell_size // 2, row * cell_size + cell_size // 2
                    color = "black"
                    self.canvas.create_text(x, y, text=symbol, fill=color, font=('Arial', 24), tags="symbol")

    def update_turn_label(self):
        if self.game.current_player == 'blue':
            self.turn_label.config(text="Blue's Turn", fg="blue")
        else:
            self.turn_label.config(text="Red's Turn", fg="red")

    def reset_board(self):
        self.game.reset_game()
        self.canvas.delete("sos_line")
        self.update_board()
        self.turn_label.config(text="Blue's Turn", fg="blue")

    def show_message(self, message):

        messagebox.showerror("Error", message)

if __name__ == '__main__':
    # Run the game GUI
    root = tk.Tk()
    root.title("SOS Game")
    board_size = int(input("Enter board size (greater than 2): "))
    game_mode = input("Enter game mode (simple/general): ").strip().lower()

    # Set the game
    if game_mode == 'simple':
        game = SOSSimpleGame(board_size)
    elif game_mode == 'general':
        game = SOSGeneralGame(board_size)
    else:
        print("Invalid game mode. Please choose 'simple' or 'general'.")
        exit()

    gui = SOSGUI(root, game)
    root.mainloop()

    # Run tests
    import unittest
    unittest.main(module='test_SOSGame', exit=False)

