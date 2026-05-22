import tkinter as tk
import random
import time

class ProcessChallengeGameGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Process Challenge Game")

        # Game parameters
        self.board_size = 5
        self.initial_max_colors = 5  
        self.colors = ["white", "red", "green", "blue", "yellow", "orange", "cyan", "purple"]  # Color names for visualization
        self.player1_time = 0
        self.player2_time = 0

        # Create player boards
        self.player1_board = [[0] * self.board_size for _ in range(self.board_size)]
        self.player2_board = [[0] * self.board_size for _ in range(self.board_size)]

        # Create GUI elements
        self.player1_label = tk.Label(self.master, text="Player 1 Matrix")
        self.player1_label.grid(row=0, column=0) 
        self.player1_canvas = tk.Canvas(self.master, width=200, height=200, bg="white")
        self.player1_canvas.grid(row=1, column=0, padx=10, pady=10)

        self.player2_label = tk.Label(self.master, text="Player 2 Matrix")
        self.player2_label.grid(row=0, column=1)
        self.player2_canvas = tk.Canvas(self.master, width=200, height=200, bg="white")
        self.player2_canvas.grid(row=1, column=1, padx=10, pady=10)

        # Strategy options for dropdown menus
        self.strategy_options = [
            "Greedy Algorithm", "Backtracking", "CSP (Constraint satisfaction problem)",
            "Memoization Algorithm", "Default Algorithm (glouton)"
        ]

        # Initialize StringVars to track selected strategies
        self.player1_method_var = tk.StringVar(self.master)
        self.player1_method_var.set(self.strategy_options[0])  # Default method for Player 1
        self.player2_method_var = tk.StringVar(self.master)
        self.player2_method_var.set(self.strategy_options[0])  # Default method for Player 2

        # Create dropdown menus for selecting strategies
        self.player1_method_menu = tk.OptionMenu(self.master, self.player1_method_var, *self.strategy_options)
        self.player1_method_menu.grid(row=2, column=0, pady=10)

        self.player2_method_menu = tk.OptionMenu(self.master, self.player2_method_var, *self.strategy_options)
        self.player2_method_menu.grid(row=2, column=1, pady=10)

        # Create "Start" button to begin the game
        self.start_button = tk.Button(self.master, text="Start", command=self.start_game)
        self.start_button.grid(row=3, columnspan=2, pady=10)

        # Create label to display game result
        self.result_label = tk.Label(self.master, text="")
        self.result_label.grid(row=4, columnspan=2, pady=10)

    def draw_board(self, canvas, board):
        canvas.delete("all")
        cell_size = 40
        for r in range(self.board_size):
            for c in range(self.board_size):
                x0, y0 = c * cell_size, r * cell_size
                x1, y1 = x0 + cell_size, y0 + cell_size
                color_index = board[r][c]
                canvas.create_rectangle(x0, y0, x1, y1, fill=self.colors[color_index])

    def start_game(self):
        # Get selected methods for both players
        player1_method = self.player1_method_var.get()
        player2_method = self.player2_method_var.get()
        #coloring
        start_time = time.perf_counter()
        self.color_board(self.player1_board, player1_method)
        end_time = time.perf_counter()
        self.player1_time = (end_time - start_time) * 1000  # Convert to milliseconds

        start_time = time.perf_counter()
        self.color_board(self.player2_board, player2_method)
        end_time = time.perf_counter()
        self.player2_time = (end_time - start_time) * 1000  # Convert to milliseconds

        # Display the colored matrices
        self.draw_board(self.player1_canvas, self.player1_board)
        self.draw_board(self.player2_canvas, self.player2_board)

        # Determine the winner based on completion times
        if self.player1_time < self.player2_time:
            winner = "Player 1 wins!"
        elif self.player2_time < self.player1_time:
            winner = "Player 2 wins!"
        else:
            winner = "It's a tie!"

        # Display the execution times for both players
        self.execution_time_p1 = tk.Label(self.master, text="Player 1 time: ")
        self.player1_time_label = tk.Label(self.master, text=str(self.player1_time))
        self.execution_time_p1.grid(row=5, column=0)
        self.player1_time_label.grid(row=6, column=0)

        self.execution_time_p2 = tk.Label(self.master, text="Player 2 time: ")
        self.player2_time_label = tk.Label(self.master, text=str(self.player2_time))
        self.execution_time_p2.grid(row=5, column=1)
        self.player2_time_label.grid(row=6, column=1)

        # Display the winner
        self.result_label.config(text=winner)

    def color_board(self, board, method):
        # Simulate coloring the board with the selected method
        coloring_function = getattr(self, method.lower().replace(" ", "_") + "_algorithm", self.default_algorithm)
        if coloring_function:
            max_colors = self.initial_max_colors
            for r in range(self.board_size):
                for c in range(self.board_size):
                    valid_colors = [color for color in range(max_colors) if self.is_valid_color(board, r, c, color)]
                    if not valid_colors:
                        # If no valid colors, expand the color palette and retry
                        max_colors += 1
                        self.colors.append(f"color_{max_colors}")  # Add new color
                        valid_colors = [color for color in range(max_colors) if self.is_valid_color(board, r, c, color)]
                    board[r][c] = random.choice(valid_colors)

    def is_valid_color(self, board, row, col, color):
        # Check if assigning the given color to the cell at (row, col) is valid
        for i in range(self.board_size):
            if board[row][i] == color or board[i][col] == color:
                return False
        return True

    def default_algorithm(self, board):
        # Default algorithm (glouton)
        max_colors = self.initial_max_colors
        for r in range(self.board_size):
            for c in range(self.board_size):
                valid_colors = [color for color in range(max_colors) if self.is_valid_color(board, r, c, color)]
                if not valid_colors:
                    # If no valid colors, expand the color palette and retry
                    max_colors += 1
                    self.colors.append(f"color_{max_colors}")  # Add new color
                    valid_colors = [color for color in range(max_colors) if self.is_valid_color(board, r, c, color)]
                board[r][c] = random.choice(valid_colors)

    def backtracking_algorithm(self, board):
        self.backtrack(board, 0, 0)

    def backtrack(self, board, row, col):
        if row == self.board_size:
            return True

        for color in range(len(self.colors)):
            if self.is_valid_color(board, row, col, color):
                board[row][col] = color

                if col < self.board_size - 1:
                    next_col = col + 1
                    next_row = row
                else:
                    next_col = 0
                    next_row = row + 1

                if self.backtrack(board, next_row, next_col):
                    return True

                board[row][col] = 0

        return False

    def csp_algorithm(self, board):
        self.csp(board, 0, 0)

    def csp(self, board, row, col):
        if row == self.board_size:
            return True

        domain = list(range(len(self.colors)))

        for color in domain:
            if self.is_valid_color(board, row, col, color):
                board[row][col] = color

                if col < self.board_size - 1:
                    next_col = col + 1
                    next_row = row
                else:
                    next_col = 0
                    next_row = row + 1

                if self.csp(board, next_row, next_col):
                    return True

                board[row][col] = 0

        return False

    def memoization_algorithm(self, board):
        self.memo = {}  # Memoization dictionary
        return self.memoization(board, 0, 0)

    def memoization(self, board, row, col):
        if row == self.board_size:
            return True

        if (row, col) in self.memo:
            return self.memo[(row, col)]

        for color in range(len(self.colors)):
            if self.is_valid_color(board, row, col, color):
                board[row][col] = color

                if col < self.board_size - 1:
                    next_col = col + 1
                    next_row = row
                else:
                    next_col = 0
                    next_row = row + 1

                if self.memoization(board, next_row, next_col):
                    self.memo[(row, col)] = True
                    return True

                board[row][col] = 0

        self.memo[(row, col)] = False
        return False

    def greedy_algorithm(self, board):
        for r in range(self.board_size):
            for c in range(self.board_size):
                valid_colors = [color for color in range(len(self.colors)) if self.is_valid_color(board, r, c, color)]
                if not valid_colors:
                    # If no valid colors, expand the color palette and retry
                    max_colors = len(self.colors)
                    self.colors.append(f"color_{max_colors}")  # Add new color
                    valid_colors = [color for color in range(max_colors) if self.is_valid_color(board, r, c, color)]
                board[r][c] = min(valid_colors)
                

def main():
    root = tk.Tk()
    app = ProcessChallengeGameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
