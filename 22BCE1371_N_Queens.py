import tkinter as tk
from tkinter import messagebox

class NQueens:
    def __init__(self, n):
        self.n = n
        self.board = [[0 for _ in range(n)] for _ in range(n)]

    def is_safe(self, row, col):
        for i in range(row):
            if self.board[i][col] == 1:
                return False
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if j < 0:
                break
            if self.board[i][j] == 1:
                return False
        for i, j in zip(range(row, -1, -1), range(col, self.n)):
            if j >= self.n:
                break
            if self.board[i][j] == 1:
                return False
        return True

    def heuristic_value(self):
        count = 0
        for row in range(self.n):
            for col in range(self.n):
                if self.board[row][col] == 1:
                    for i in range(self.n):
                        for j in range(self.n):
                            if (i != row and j != col and
                                abs(row - i) != abs(col - j) and
                                self.board[i][j] == 1):
                                count += 1
        return count // 2

    def place_queens(self, row):
        if row >= self.n:
            return True
        for col in range(self.n):
            if self.is_safe(row, col):
                self.board[row][col] = 1
                if self.place_queens(row + 1):
                    return True
                self.board[row][col] = 0
        return False

    def reset_board(self):
        self.board = [[0 for _ in range(self.n)] for _ in range(self.n)]

    def is_goal_state(self):
        for row in range(self.n):
            if sum(self.board[row]) != 1:
                return False
            for col in range(self.n):
                count = sum(self.board[row][col] for row in range(self.n))
                if count != 1:
                    return False
                for row in range(self.n):
                    for col in range(self.n):
                        if self.board[row][col] == 1:
                            for i, j in zip(range(row - 1, -1, -1), range(col - 1, -1, -1)):
                                if self.board[i][j] == 1:
                                    return False
                                for i, j in zip(range(row - 1, -1, -1), range(col + 1, self.n)):
                                    if self.board[i][j] == 1:
                                        return False
        return True

class NQueensGUI:
    def __init__(self, master):
        self.master = master
        self.n = 4
        self.n_queens = NQueens(self.n)

        self.size_frame = tk.Frame(master)
        self.size_frame.pack(pady=5)
        self.size_label = tk.Label(self.size_frame, text="Enter board size (n):")
        self.size_label.pack(side=tk.LEFT)
        self.size_entry = tk.Entry(self.size_frame, width=5)
        self.size_entry.insert(0, str(self.n))
        self.size_entry.pack(side=tk.LEFT)

        self.input_frame = tk.Frame(master)
        self.input_frame.pack(pady=5)
        self.input_label = tk.Label(self.input_frame, text="Enter initial queen positions (comma separated):")
        self.input_label.pack(side=tk.LEFT)
        self.input_entry = tk.Entry(self.input_frame)
        self.input_entry.pack(side=tk.LEFT)

        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=5)

        self.submit_button = tk.Button(self.button_frame, text="Display Queens", command=self.display_initial_state)
        self.submit_button.pack(side=tk.LEFT, padx=5)

        self.solve_button = tk.Button(self.button_frame, text="Solve N-Queens", command=self.solve_n_queens)
        self.solve_button.pack(side=tk.LEFT, padx=5)

        self.canvas = tk.Canvas(master, width=400, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self.resize_canvas)
        self.draw_board()

        self.size_entry.bind("<Return>", self.update_board_size)

    def update_board_size(self, event):
        try:
            new_n = int(self.size_entry.get())
            if new_n < 4:
                raise ValueError("N must be at least 4")
            self.n = new_n
            self.n_queens = NQueens(self.n)
            self.input_entry.delete(0, tk.END)
            self.draw_board()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def display_initial_state(self):
        input_str = self.input_entry.get()
        positions = input_str.split(',')

        if len(positions) != self.n:
            messagebox.showerror("Error", f"Please enter {self.n} positions.")
            return

        self.n_queens.reset_board()
        try:
            for row in range(self.n):
                col = int(positions[row].strip())
                if 0 <= col < self.n:
                    self.n_queens.board[row][col] = 1
                else:
                    raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Enter valid column indices.")
            return

        heuristic = self.n_queens.heuristic_value()
        print("\nHeuristic value for the given state:", heuristic)

        if self.n_queens.is_goal_state():
            print("The initial state is a goal state!")

        self.draw_board()

    def solve_n_queens(self):
        self.n_queens.reset_board()
        self.n_queens.place_queens(0)
        self.draw_board()
        heuristic = self.n_queens.heuristic_value()
        print("Heuristic value for the solution state:", heuristic)

    def resize_canvas(self, event):
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        cell_size = min(self.canvas.winfo_width(), self.canvas.winfo_height()) // self.n
        for i in range(self.n):
            for j in range(self.n):
                color = "white" if (i + j) % 2 == 0 else "black"
                self.canvas.create_rectangle(j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size, fill=color)
                if self.n_queens.board[i][j] == 1:
                    self.canvas.create_oval(j * cell_size + 10, i * cell_size + 10, (j + 1) * cell_size - 10, (i + 1) * cell_size - 10, fill="red")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("N-Queens Problem")
    root.geometry("680x800")
    root.resizable(True, True)
    app = NQueensGUI(root)
    root.mainloop()
