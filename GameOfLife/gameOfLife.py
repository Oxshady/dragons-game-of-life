from tkinter import *
from tkinter import ttk
import random
import json
class GameOfLife:
    """
    The Game of Life class that implements the Game of Life simulation.
    """
    def __init__(self, frame, rows=20, cols=20, cell_size=20):
        """
        Initialize the Game of Life with a given frame, number of rows, columns, and cell size.
        """
        self.frame = frame
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.is_running = False

        self.canvas = Canvas(frame, width=cols * cell_size, height=rows * cell_size, bg='white', highlightbackground="#ccc")
        self.canvas.pack(pady=20)

        self.grid = [[random.choice([0, 1]) for _ in range(cols)] for _ in range(rows)]
        self.temp_grid = [[0 for _ in range(cols)] for _ in range(rows)]

        self.canvas.bind("<Button-1>", self.toggle_cell)

        self.slider_frame = Frame(frame, bg="#F0F0F0")
        self.slider_frame.pack(pady=10)

        self.speed_scale = Scale(self.slider_frame, from_=500, to=10, orient=HORIZONTAL, label="Speed (ms)", font=("Arial", 12, "bold"), length=200, bg="#F0F0F0")
        self.speed_scale.set(250)
        self.speed_scale.pack(side='left', padx=5)

        self.zoom_scale = Scale(self.slider_frame, from_=10, to=50, orient=HORIZONTAL, label="Zoom", font=("Arial", 12, "bold"), length=200, command=self.zoom_grid)
        self.zoom_scale.set(self.cell_size)
        self.zoom_scale.pack(side='left', padx=5)

        self.color_frame = Frame(frame, bg="#F0F0F0")
        self.color_frame.pack(pady=10)

        self.color_list = ['black', 'red', 'green', 'blue', 'yellow', 'purple', 'orange', 'pink']
        self.alive_color = 'black'
        self.dead_color = 'white'

        self.alive_color_combobox = ttk.Combobox(self.color_frame, values=self.color_list, state='readonly', width=12)
        self.alive_color_combobox.set(self.alive_color)
        self.alive_color_combobox.bind("<<ComboboxSelected>>", self.update_alive_color)
        self.alive_color_combobox.grid(row=0, column=0, padx=5)

        self.dead_color_combobox = ttk.Combobox(self.color_frame, values=self.color_list, state='readonly', width=12)
        self.dead_color_combobox.set(self.dead_color)
        self.dead_color_combobox.bind("<<ComboboxSelected>>", self.update_dead_color)
        self.dead_color_combobox.grid(row=0, column=1, padx=5)

        self.start_button = Button(self.color_frame, text="Start", command=self.start_game, bg="#4CAF50", fg="white", relief=FLAT)
        self.start_button.grid(row=0, column=2, padx=5)

        self.stop_button = Button(self.color_frame, text="Stop", command=self.stop_game, bg="#F44336", fg="white", relief=FLAT)
        self.stop_button.grid(row=0, column=3, padx=5)

        self.clear_button = Button(self.color_frame, text="Clear", command=self.clear_grid, bg="#FF9800", fg="white", relief=FLAT)
        self.clear_button.grid(row=0, column=4, padx=5)

        self.randomize_button = Button(self.color_frame, text="Randomize", command=self.randomize_grid, bg="#58CBFC", fg="white", relief=FLAT)
        self.randomize_button.grid(row=0, column=5, padx=5)
        from dragons import Dragons
        self.lobby_button = Button(self.color_frame, text="lobby", command=Dragons.lobby.tkraise, bg="#58FCC2", fg="white", relief=FLAT)
        self.lobby_button.grid(row=0, column=6, padx=5)
        save_button = Button(self.color_frame, text="Save Pattern", command=self.save_pattern, font=("Arial", 12, "bold"), bg="#673AB7", fg="white", relief=FLAT)
        save_button.grid(row=1, column=2, padx=5, pady=5)

        load_button = Button(self.color_frame, text="Load Pattern", command=self.load_pattern, font=("Arial", 12, "bold"), bg="#FFEB3B", fg="black", relief=FLAT)
        load_button.grid(row=1, column=3, padx=5, pady=5)

        self.draw_grid()
        self.update_canvas()

    def toggle_cell(self, event):
        """
        Toggle the state of a cell between alive and dead when clicked.
        """
        x, y = event.x, event.y
        row = y // self.cell_size
        col = x // self.cell_size
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] = 1 if self.grid[row][col] == 0 else 0
            self.update_canvas()

    def draw_grid(self):
        """
        Draw the grid on the canvas with the current state of each cell.
        """
        for i in range(self.rows):
            for j in range(self.cols):
                color = self.alive_color if self.grid[i][j] == 1 else self.dead_color
                self.canvas.create_rectangle(j * self.cell_size, i * self.cell_size,
                                              (j + 1) * self.cell_size, (i + 1) * self.cell_size,
                                              fill=color, outline="#ccc")

    def update_canvas(self):
        """
        Update the canvas by redrawing the grid.
        """
        self.canvas.delete("all")
        self.draw_grid()

    def update_grid(self, rows, cols):
        """
        Update the grid dimensions and reset the grid with random values.
        """
        self.rows = rows
        self.cols = cols
        self.cell_size = self.zoom_scale.get()
        self.grid = [[random.choice([0, 1]) for _ in range(cols)] for _ in range(rows)]
        self.temp_grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.canvas.config(width=self.cols * self.cell_size, height=self.rows * self.cell_size)
        self.update_canvas()

    def zoom_grid(self, value):
        """
        Zoom the grid by adjusting the cell size.
        """
        self.cell_size = int(value)
        self.canvas.config(width=self.cols * self.cell_size, height=self.rows * self.cell_size)
        self.update_canvas()

    def update_alive_color(self, event):
        """
        Update the color used for alive cells.
        """
        self.alive_color = self.alive_color_combobox.get()
        self.update_canvas()

    def update_dead_color(self, event):
        """
        Update the color used for dead cells.
        """
        self.dead_color = self.dead_color_combobox.get()
        self.update_canvas()

    def start_game(self):
        """
        Start the Game of Life simulation.
        """
        self.is_running = True
        self.run_game()

    def run_game(self):
        """
        Run the Game of Life simulation by updating cells and redrawing the grid.
        """
        if self.is_running:
            self.update_cells()
            self.update_canvas()
            self.frame.after(self.speed_scale.get(), self.run_game)

    def stop_game(self):
        """
        Stop the Game of Life simulation.
        """
        self.is_running = False

    def clear_grid(self):
        """
        Clear the grid by setting all cells to dead.
        """
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.update_canvas()

    def randomize_grid(self):
        """
        Randomize the grid by setting each cell to a random state.
        """
        self.grid = [[random.choice([0, 1]) for _ in range(self.cols)] for _ in range(self.rows)]
        self.update_canvas()

    def update_cells(self):
        """
        Update the state of each cell based on the Game of Life rules.
        """
        for i in range(self.rows):
            for j in range(self.cols):
                live_neighbors = self.count_live_neighbors(i, j)
                if self.grid[i][j] == 1:
                    self.temp_grid[i][j] = 1 if live_neighbors in (2, 3) else 0
                else:
                    self.temp_grid[i][j] = 1 if live_neighbors == 3 else 0
        self.grid, self.temp_grid = self.temp_grid, self.grid

    def count_live_neighbors(self, row, col):
        """
        Count the number of live neighbors for a given cell.
        """
        count = 0
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if (i == row and j == col) or i < 0 or i >= self.rows or j < 0 or j >= self.cols:
                    continue
                count += self.grid[i][j]
        return count
    def save_pattern(self):
        """Save the current grid pattern to a file."""
        with open("saved_pattern.json", "w") as file:
            json.dump(self.grid, file)
    def load_pattern(self):
        """Load a saved grid pattern from a file."""
        try:
            with open("saved_pattern.json", "r") as file:
                self.grid = json.load(file)
            self.draw_grid()
        except FileNotFoundError:
            print("No saved pattern found.")
