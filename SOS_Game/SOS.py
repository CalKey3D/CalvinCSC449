import tkinter as tk
from tkinter import messagebox, filedialog
from abc import ABC, abstractmethod
import requests

API_KEY = "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"  # Replace with your actual OpenAI API key

#LLM Driven CPU
class CPU:
    def calculate_move(self, board, max_retries=3):
        # Convert board to a string so that the LLM can process it properly
        board_str = ""
        for row in board:
            row_str = " ".join(cell if cell != ' ' else '_' for cell in row)
            board_str += row_str + "\n"

        prompt = f"""
        You are playing an SOS game. The board is given below. Underscores ('_') represent empty cells; 'S' and 'O' represent occupied cells.

        Goal: Make a move that leads to forming "SOS" if possible in horizontal, vertical, or diagonal directions. 
        - You must pick an empty cell (denoted by '_').
        - The board uses zero-based indexing.
        - Respond with "row,column,letter" (where letter is 'S' or 'O').
        - Do not pick a cell that is already occupied (not '_').

        Current board:
        {board_str}

        It's your turn. Only provide the move (no other explanation).
        """

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "model": "gpt-4o",  # Can swap to "gpt-3.5-turbo" if this is too expensive, but seems reasonable
            "messages": [{"role": "user", "content": prompt.strip()}],
            "max_tokens": 300,
            "temperature": 0.4,
        }

        for attempt in range(max_retries):
            try:
                # Send the request
                response = requests.post(url, headers=headers, json=data)

                if response.status_code == 200:
                    json_response = response.json()
                    move = json_response['choices'][0]['message']['content'].strip()
                    row_str, col_str, letter = move.split(",")
                    row = int(row_str.strip())
                    col = int(col_str.strip())
                    letter = letter.strip().upper()

                    # Validate the output
                    if letter not in ['S', 'O']:
                        raise ValueError("LLM returned an invalid symbol. Must be 'S' or 'O'.")

                    # Verify not an occupied cell
                    if board[row][col] != ' ':
                        raise ValueError("LLM chose an occupied cell.")

                    return row, col, letter

                else:
                    # For any API errors
                    print(f"Error {response.status_code}: {response.text}")
                    raise Exception("Failed to get a valid response from LLM.")

            except Exception as e:
                # Log the error and retry up to the max_retries count
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    # If all retries fail, just places into the first empty cell
                    print("All retries failed. Placed S into first empty cell.")
                    for r in range(len(board)):
                        for c in range(len(board[r])):
                            if board[r][c] == ' ':
                                return r, c, 'S'
                    raise Exception("No possible move.")

class SOSGame(ABC):
    def __init__(self, board_size, CPU):
        self.board_size = board_size
        self.CPU = CPU
        self.board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = 'blue'
        self.last_player = None  # Added to track the last player
        self.sos_count = {'blue': 0, 'red': 0}
        self.CPU_Player = {'blue': False, 'red': False}
        self.game_over = False
        self.game_over_counter = 0
        self.game_over_max = board_size ** 2
        self.current_turn_sequences = []

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

        pairs = [[(-1, 0), (1, 0)],
                 [(-1, 1), (1, -1)],
                 [(0, -1), (0, 1)],
                 [(-1, -1), (1, 1)]]
        for pair in pairs:
            try:
                if row + pair[0][0] < 0 or col + pair[0][1] < 0:
                    continue
                if self.board[row + pair[0][0]][col + pair[0][1]] != 'S':
                    continue
                if row + pair[1][0] < 0 or col + pair[1][1] < 0:
                    continue
                if self.board[row + pair[1][0]][col + pair[1][1]] == 'S':
                    self.sos_count[self.current_player] += 1
                    sos_sequence = [
                        (row + pair[1][0], col + pair[1][1]),
                        (row, col),
                        (row + pair[0][0], col + pair[0][1])
                    ]
                    self.current_turn_sequences.append(sos_sequence)

            except IndexError:
                continue

    def check_sequence_s(self, row, col):

        pairs = [[(-1, 0), (-2, 0)],      # up
                 [(-1, 1), (-2, 2)],      # up right
                 [(0, 1), (0, 2)],        # right
                 [(1, 1), (2, 2)],        # down right
                 [(1, 0), (2, 0)],        # down
                 [(1, -1), (2, -2)],      # down left
                 [(0, -1), (0, -2)],      # left
                 [(-1, -1), (-2, -2)]]    # up left

        for pair in pairs:
            try:
                if row + pair[0][0] < 0 or col + pair[0][1] < 0:
                    continue
                if self.board[row + pair[0][0]][col + pair[0][1]] != 'O':
                    continue
                if row + pair[1][0] < 0 or col + pair[1][1] < 0:
                    continue
                if self.board[row + pair[1][0]][col + pair[1][1]] == 'S':
                    self.sos_count[self.current_player] += 1
                    sos_sequence = [
                        (row, col),
                        (row + pair[0][0], col + pair[0][1]),
                        (row + pair[1][0], col + pair[1][1])
                    ]
                    self.current_turn_sequences.append(sos_sequence)

            except IndexError:
                continue

    def get_board(self):
        return self.board

    def reset_game(self):
        self.board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = 'blue'
        self.last_player = None
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

        # Record the move if recording is enabled
        if hasattr(gui, 'record_file') and gui.record_file is not None and not gui.record_file.closed:
            gui.record_file.write(f"{self.current_player},{row},{col},{symbol}\n")

        # Record the player who made the move
        self.last_player = self.current_player

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

        # Record the move if recording is enabled
        if hasattr(gui, 'record_file') and gui.record_file is not None and not gui.record_file.closed:
            gui.record_file.write(f"{self.current_player},{row},{col},{symbol}\n")

        # Record the player who made the move
        self.last_player = self.current_player

        self.change_turn()  # Always change turn in general game

        if self.game_over_counter >= self.game_over_max:
            self.game_over = True
            return

class SOSGUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.symbol_choice_blue = tk.StringVar(value='S')
        self.symbol_choice_red = tk.StringVar(value='S')

        self.record_game = tk.BooleanVar(value=False)
        self.record_file = None
        self.loaded_game = False

        if self.game is not None:
            self.setup_game()

    def setup_game(self):
        if not hasattr(self, 'canvas'):
            self.canvas = tk.Canvas(self.root)
            self.canvas.grid(row=0, column=0, columnspan=self.game.board_size)
        self.create_board()
        self.create_controls()

        if self.record_game.get() and not self.loaded_game:
            self.start_recording()

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

        # Add Record Game checkbox
        self.record_game = tk.BooleanVar(value=False)
        tk.Checkbutton(dialog, text="Record Game", variable=self.record_game).pack()

        # Add Load Game button
        tk.Button(dialog, text="Load Game", command=lambda: [dialog.destroy(), self.load_game()]).pack()

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
        self.canvas.delete("all")  # Clear any existing elements
        for row in range(self.game.board_size):
            for col in range(self.game.board_size):
                x1, y1 = col * cell_size, row * cell_size
                x2, y2 = x1 + cell_size, y1 + cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", tags="grid")

        self.canvas.create_rectangle(2, 2, board_size, board_size, outline="black", width=1, tags="outer_border")
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
        if not hasattr(self, 'symbol_frame'):
            self.symbol_frame = tk.Frame(self.root)
            self.symbol_frame.grid(row=self.game.board_size, column=0, columnspan=self.game.board_size)
            tk.Label(self.symbol_frame, text="Blue: ").pack(side=tk.LEFT)
            tk.Radiobutton(self.symbol_frame, text='S', variable=self.symbol_choice_blue, value='S').pack(side=tk.LEFT)
            tk.Radiobutton(self.symbol_frame, text='O', variable=self.symbol_choice_blue, value='O').pack(side=tk.LEFT)
            tk.Checkbutton(self.symbol_frame, text='CPU', command=self.toggle_cpu_blue).pack(side=tk.LEFT)
            tk.Label(self.symbol_frame, text="Red: ").pack(side=tk.LEFT)
            tk.Radiobutton(self.symbol_frame, text='S', variable=self.symbol_choice_red, value='S').pack(side=tk.LEFT)
            tk.Radiobutton(self.symbol_frame, text='O', variable=self.symbol_choice_red, value='O').pack(side=tk.LEFT)
            tk.Checkbutton(self.symbol_frame, text='CPU', command=self.toggle_cpu_red).pack(side=tk.LEFT)

            replay_button = tk.Button(self.symbol_frame, text="Replay", command=self.reset_board)
            replay_button.pack(side=tk.LEFT)

            self.turn_label = tk.Label(self.symbol_frame, text="Blue's Turn", fg="blue")
            self.turn_label.pack(side=tk.LEFT)

    def on_canvas_click(self, event):
        cell_size = 50
        row, col = event.y // cell_size, event.x // cell_size

        if self.game.game_over:
            return

        if self.game.current_player == 'blue':
            symbol = self.symbol_choice_blue.get()
        else:
            symbol = self.symbol_choice_red.get()

        try:
            self.game.make_move(row, col, symbol, self)
            self.update_after_move()
        except Exception as e:
            pass

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
            if hasattr(self, 'record_file') and self.record_file and not self.record_file.closed:
                self.record_file.close()
        else:
            self.update_turn_label()

            if self.game.current_player == 'blue':
                if self.game.CPU_Player['blue']:
                    row, col, symbol = self.game.CPU.calculate_move(self.game.board)
                    self.game.make_move(row, col, symbol, self)
                    self.update_after_move()
            else:
                if self.game.CPU_Player['red']:
                    row, col, symbol = self.game.CPU.calculate_move(self.game.board)
                    self.game.make_move(row, col, symbol, self)
                    self.update_after_move()

    def draw_sos_lines(self):
        if self.game.last_player == 'blue':
            color = 'blue'
        elif self.game.last_player == 'red':
            color = 'red'
        else:
            color = 'black'

        cell_size = 50

        for sequence in self.game.current_turn_sequences:
            (r1, c1), (r2, c2), (r3, c3) = sequence

            x1, y1 = c1 * cell_size + 25, r1 * cell_size + 25
            x2, y2 = c2 * cell_size + 25, r2 * cell_size + 25
            x3, y3 = c3 * cell_size + 25, r3 * cell_size + 25

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
        if hasattr(self, 'record_file') and self.record_file and not self.record_file.closed:
            self.record_file.close()

        self.game.reset_game()
        self.canvas.delete("sos_line")
        self.update_board()
        self.turn_label.config(text="Blue's Turn", fg="blue")

        if self.record_game.get():
            self.start_recording()

    def show_message(self, message):
        messagebox.showerror("Error", message)

    def start_recording(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if save_path:
            self.record_file = open(save_path, 'w')
            self.record_file.write(f"BoardSize:{self.selected_board_size}\n")
            self.record_file.write(f"GameMode:{self.selected_game_mode}\n")
            self.record_file.write(f"CPUPlayers:Blue={self.game.CPU_Player['blue']},Red={self.game.CPU_Player['red']}\n")
            self.record_file.write("Moves:\n")
        else:
            self.record_game.set(False)

    def load_game(self):
        load_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if load_path:
            with open(load_path, 'r') as file:
                lines = file.readlines()
            self.parse_loaded_game(lines)
            self.loaded_game = True
        else:
            self.show_startup_dialog()

    def parse_loaded_game(self, lines):
        cpu_players = {'blue': False, 'red': False}
        moves = []
        for index, line in enumerate(lines):
            if line.startswith('BoardSize'):
                self.selected_board_size = int(line.split(':')[1])
            elif line.startswith('GameMode'):
                self.selected_game_mode = line.split(':')[1].strip()
            elif line.startswith('CPUPlayers'):
                cpu_players_line = line.split(':')[1]
                cpu_players = dict(item.split('=') for item in cpu_players_line.strip().split(','))
                cpu_players = {k.lower(): v == 'True' for k, v in cpu_players.items()}
            elif line.strip() == 'Moves:':
                moves = lines[index + 1:]
                break

        CPU_instance = CPU()
        if self.selected_game_mode == 'simple':
            self.game = SOSSimpleGame(self.selected_board_size, CPU_instance)
        elif self.selected_game_mode == 'general':
            self.game = SOSGeneralGame(self.selected_board_size, CPU_instance)

        self.game.CPU_Player['blue'] = cpu_players['blue']
        self.game.CPU_Player['red'] = cpu_players['red']

        self.symbol_choice_blue.set('S')
        self.symbol_choice_red.set('S')

        if not hasattr(self, 'canvas'):
            self.setup_game()
        else:
            self.create_board()
            self.create_controls()

        for move_line in moves:
            if move_line.strip() == '':
                continue
            player, row, col, symbol = move_line.strip().split(',')
            row, col = int(row), int(col)
            self.game.current_player = player
            if player == 'blue':
                self.symbol_choice_blue.set(symbol)
            else:
                self.symbol_choice_red.set(symbol)
            try:
                self.game.make_move(row, col, symbol, self)
                self.update_board()
                self.update_turn_label()
                self.draw_sos_lines()

            except Exception as e:
                print(f"Error during loading move {move_line}: {e}")

    def setup_game_instance(self, cpu_players):
        CPU_instance = CPU()
        if self.selected_game_mode == 'simple':
            self.game = SOSSimpleGame(self.selected_board_size, CPU_instance)
        else:
            self.game = SOSGeneralGame(self.selected_board_size, CPU_instance)

        self.game.CPU_Player['blue'] = cpu_players['blue']
        self.game.CPU_Player['red'] = cpu_players['red']

        self.setup_game()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("SOS Game")

    gui = SOSGUI(root, None)
    gui.show_startup_dialog()

    if not gui.loaded_game:
        CPU_instance = CPU()
        if gui.selected_game_mode == 'simple':
            game = SOSSimpleGame(gui.selected_board_size, CPU_instance)
        elif gui.selected_game_mode == 'general':
            game = SOSGeneralGame(gui.selected_board_size, CPU_instance)

        gui.game = game
        gui.setup_game()

    root.mainloop()
