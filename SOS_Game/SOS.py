import tkinter as tk
from tkinter import messagebox
from abc import ABC, abstractmethod

class CPU:
    def check_sos(self, row, col, symbol, board):

        if symbol == 'S':
            return self.check_sequence_s(row, col, board)
        if symbol == 'O':
            return self.check_sequence_o(row, col, board)

    def check_sequence_o(self, row, col, board):

        pairs = [[(-1, 0), (1, 0)], [(-1, 1), (1, -1)], [(0, -1), (0, 1)], [(-1, -1), (1, 1)]]
        for pair in pairs:
            try:
                if row + pair[0][0] < 0 or col + pair[0][1] < 0:
                    continue
                if board[row + pair[0][0]][col + pair[0][1]] != 'S':
                    continue
                if row + pair[1][0] < 0 or col + pair[1][1] < 0:
                    continue
                if board[row + pair[1][0]][col + pair[1][1]] == 'S':
                    return True

            except IndexError:
                continue

        return False

    def check_sequence_s(self, row, col, board):

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
                if board[row + pair[0][0]][col + pair[0][1]] != 'O':
                    continue
                if row + pair[1][0] < 0 or col + pair[1][1] < 0:
                    continue
                if board[row + pair[1][0]][col + pair[1][1]] == 'S':
                    return True

            except IndexError:
                continue

        return False

    def calculate_move(self, board):

        board_size = range(len(board))

        # checks for possible sequences throughout the board
        for row in board_size:
            # print("ROW:", row)
            for col in board_size:
                # print("COL:", col)
                if board[row][col] == ' ':
                    if self.check_sos(row, col, 'S', board):
                        return row, col, 'S'
                    elif self.check_sos(row, col, 'O', board):
                        return row, col, 'O'
        # print("Sequence not found, moving to logic 2...")

        # finds the first 'S' and tries to place an 'O' to the right of it
        for row in board_size:
            for col in board_size:
                if board[row][col] == 'S':
                    try:
                        if board[row][col + 1] == ' ':
                            return row, col + 1, 'O'
                    except IndexError:
                        continue
        # print("Moving to logic 3...")


        # places an 'S' in the first available spot
        for row in board_size:
            for col in board_size:
                if board[row][col] == ' ':
                    return row, col, 'S'
        print("No possible move, something could be wrong...")

        raise Exception

class SOSGame(ABC):
    def __init__(self, board_size, CPU):
        self.board_size = board_size
        self.CPU = CPU
        self.board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = 'blue'
        self.sos_count = {'blue': 0, 'red': 0}
        self.CPU_Player = {'blue': False, 'red': False}
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
                    # print("sequence found") debug line
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
                    # print("sequence found") debug line
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
        self.symbol_choice_blue = tk.StringVar(value='S')
        self.symbol_choice_red = tk.StringVar(value='S')

        # Delay canvas until after getting game instance
        if self.game is not None:
            self.setup_game()

    def setup_game(self):
        self.canvas = tk.Canvas(self.root, width=50 * self.game.board_size, height=50 * self.game.board_size)
        self.canvas.grid(row=0, column=0, columnspan=self.game.board_size)
        self.create_board()
        self.create_controls()

    def show_startup_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Game Setup")

        tk.Label(dialog, text="Enter board size (greater than 2):").pack()
        board_size_entry = tk.Entry(dialog)
        board_size_entry.pack()

        # Game mode selection
        game_mode = tk.StringVar(value="simple")
        tk.Label(dialog, text="Select Game Mode:").pack()
        tk.Radiobutton(dialog, text="Simple", variable=game_mode, value="simple").pack()
        tk.Radiobutton(dialog, text="General", variable=game_mode, value="general").pack()

        def confirm():
            try:
                board_size = int(board_size_entry.get())
                if board_size <= 2:
                    raise ValueError("Board size must be greater than 2.")
                self.selected_board_size = board_size
                self.selected_game_mode = game_mode.get()
                dialog.destroy()  # Close the dialog
            except ValueError as e:
                tk.messagebox.showerror("Invalid Input", str(e))

        # Confirm button
        tk.Button(dialog, text="Confirm", command=confirm).pack()

        # Wait for the window to close before continuing
        self.root.wait_window(dialog)

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

    def toggle_cpu_blue(self):
        self.game.CPU_Player['blue'] = not self.game.CPU_Player['blue']
        if self.game.CPU_Player['blue'] == True and self.game.current_player == 'blue':
            row, col, symbol = self.game.CPU.calculate_move(self.game.board)
            self.game.make_move(row, col, symbol, self)
            self.update_after_move()

    def toggle_cpu_red(self):
        self.game.CPU_Player['red'] = not self.game.CPU_Player['red']
        if self.game.CPU_Player['red'] == True and self.game.current_player == 'red':
            row, col, symbol = self.game.CPU.calculate_move(self.game.board)
            self.game.make_move(row, col, symbol, self)
            self.update_after_move()

    def create_controls(self):
        # Add radio buttons for symbol selection and human/cpu selection
        symbol_frame = tk.Frame(self.root)
        symbol_frame.grid(row=self.game.board_size, column=0, columnspan=self.game.board_size)
        tk.Label(symbol_frame, text="Blue: ").pack(side=tk.LEFT)
        tk.Radiobutton(symbol_frame, text='S', variable=self.symbol_choice_blue, value='S').pack(side=tk.LEFT)
        tk.Radiobutton(symbol_frame, text='O', variable=self.symbol_choice_blue, value='O').pack(side=tk.LEFT)
        tk.Checkbutton(symbol_frame, text='CPU', command=self.toggle_cpu_blue).pack(side=tk.LEFT)
        tk.Label(symbol_frame, text="Red: ").pack(side=tk.LEFT)
        tk.Radiobutton(symbol_frame, text='S', variable=self.symbol_choice_red, value='S').pack(side=tk.LEFT)
        tk.Radiobutton(symbol_frame, text='O', variable=self.symbol_choice_red, value='O').pack(side=tk.LEFT)
        tk.Checkbutton(symbol_frame, text='CPU', command=self.toggle_cpu_red).pack(side=tk.LEFT)

        # Add Replay button
        replay_button = tk.Button(symbol_frame, text="Replay", command=self.reset_board)
        replay_button.pack(side=tk.LEFT)

        # Add Turn label
        self.turn_label = tk.Label(symbol_frame, text="Blue's Turn", fg="blue")
        self.turn_label.pack(side=tk.LEFT)

    def on_canvas_click(self, event):
        cell_size = 50
        row, col = event.y // cell_size, event.x // cell_size


        if self.game.current_player == 'blue':
            symbol = self.symbol_choice_blue.get()
        else:
            symbol = self.symbol_choice_red.get()

        # Check if the move is valid, then update board and draw the symbol
        self.game.make_move(row, col, symbol, self)
        self.update_after_move()

    def update_after_move(self):
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

            if self.game.current_player == 'blue':
                symbol = self.symbol_choice_blue.get()
                if self.game.CPU_Player['blue'] == True:
                    row, col, symbol = self.game.CPU.calculate_move(self.game.board)
                    self.game.make_move(row, col, symbol, self)
                    self.update_after_move()


            else:
                symbol = self.symbol_choice_red.get()
                if self.game.CPU_Player['red'] == True:
                    row, col, symbol = self.game.CPU.calculate_move(self.game.board)
                    self.game.make_move(row, col, symbol, self)
                    self.update_after_move()

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
    root = tk.Tk()
    root.title("SOS Game")

    # Initialize the GUI without a game instance
    gui = SOSGUI(root, None)

    # Run the popup to get board size and game mode
    gui.show_startup_dialog()

    # Create the game
    CPU_instance = CPU()
    if gui.selected_game_mode == 'simple':
        game = SOSSimpleGame(gui.selected_board_size, CPU_instance)
    elif gui.selected_game_mode == 'general':
        game = SOSGeneralGame(gui.selected_board_size, CPU_instance)

    # Assign the created game to the GUI and complete setup
    gui.game = game
    gui.setup_game()
    root.mainloop()

