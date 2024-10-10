from tkinter import *
from tkinter import ttk
import random


class GameOfLife:
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
        
        self.speed = 500
        self.speed_scale = Scale(frame, from_=1000, to=50, orient=HORIZONTAL, label="   speed the game", font=("Arial", 12, "bold"), length=200, bg="#F0F0F0")
        self.speed_scale.set(self.speed)
        self.speed_scale.pack(pady=10)

        self.color_list = ['black', 'red', 'green', 'blue', 'yellow', 'purple', 'orange', 'pink']
        self.alive_color = 'black'
        self.dead_color = 'white'

        self.alive_color_combobox = ttk.Combobox(frame, values=self.color_list, state='readonly', width=12)
        self.alive_color_combobox.set(self.alive_color)
        self.alive_color_combobox.pack(side='left', padx=5)

        self.dead_color_combobox = ttk.Combobox(frame, values=self.color_list, state='readonly', width=12)
        self.dead_color_combobox.set(self.dead_color)
        self.dead_color_combobox.pack(side='left', padx=5)

        color_button = Button(frame, text='Set Colors', command=self.set_colors, font=("Arial", 14), bg="#FFC107", fg="white", relief=FLAT)
        color_button.pack(side='left', padx=5)

        button_frame = Frame(frame, bg='white')
        button_frame.pack(side='bottom', pady=10)

        self.start_button = Button(button_frame, text='Start', command=self.start_game, font=("Arial", 14), bg="#4CAF50", fg="white", relief=FLAT)
        self.start_button.grid(row=0, column=0, padx=5)

        self.stop_button = Button(button_frame, text='Stop', command=self.stop_game, font=("Arial", 14), bg="#F44336", fg="white", relief=FLAT)
        self.stop_button.grid(row=0, column=1, padx=5)

        self.reset_button = Button(button_frame, text='Reset', command=self.reset_game, font=("Arial", 14), bg="#FF9800", fg="white", relief=FLAT)
        self.reset_button.grid(row=0, column=2, padx=5)

        self.randomize_button = Button(button_frame, text='Randomize', command=self.randomize_grid, font=("Arial", 14), bg="#2196F3", fg="white", relief=FLAT)
        self.randomize_button.grid(row=0, column=3, padx=5)

        from dragons import Dragons
        self.lobby_button = Button(button_frame, text='Lobby', command=lambda: Dragons.lobby.tkraise(), font=("Arial", 14), bg="#FF5722", fg="white", relief=FLAT)
        self.lobby_button.grid(row=0, column=4, padx=5)

        self.canvas.bind("<Button-1>", self.toggle_cell)

        self.draw_grid()

    def set_colors(self):
        """
        Set the colors for alive and dead cells based on the combobox selections.
        """
        self.alive_color = self.alive_color_combobox.get()
        self.dead_color = self.dead_color_combobox.get()
        self.draw_grid()

    def toggle_cell(self, event):
        """
        Toggle the state of a cell between alive and dead when clicked.
        """
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] = 1 - self.grid[row][col]
            self.draw_grid()

    def randomize_grid(self):
        """
        Randomize the grid with alive and dead cells.
        """
        for r in range(self.rows):
            for c in range(self.cols):
                self.grid[r][c] = random.choice([0, 1])
        self.draw_grid()

    def start_game(self):
        """
        Start the Game of Life simulation.
        """
        self.is_running = True
        self.update_grid()

    def stop_game(self):
        """
        Stop the Game of Life simulation.
        """
        self.is_running = False

    def reset_game(self):
        """
        Reset the grid to all dead cells.
        """
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.draw_grid()

    def draw_grid(self):
        """
        Draw the grid on the canvas.
        """
        self.canvas.delete("all")
        for r in range(self.rows):
            for c in range(self.cols):
                color = self.alive_color if self.grid[r][c] == 1 else self.dead_color
                self.canvas.create_rectangle(c * self.cell_size, r * self.cell_size, (c + 1) * self.cell_size, (r + 1) * self.cell_size, fill=color, outline="#ccc")

    def update_grid(self, rows=None, cols=None):
        """
        Update the grid based on the rules of the Game of Life.
        """
        if rows is not None and cols is not None:
            self.rows, self.cols = rows, cols
            self.grid = [[random.choice([0, 1]) for _ in range(cols)] for _ in range(rows)]
            self.canvas.config(width=cols * self.cell_size, height=rows * self.cell_size)

        if self.is_running:
            self.temp_grid = [[self.calculate_next_state(r, c) for c in range(self.cols)] for r in range(self.rows)]
            self.grid = [row[:] for row in self.temp_grid]
            self.draw_grid()
            self.frame.after(self.speed_scale.get(), self.update_grid)

    def calculate_next_state(self, row, col):
        """
        Calculate the next state of a cell based on its neighbors.
        """
        neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        live_neighbors = 0
        for neighbor in neighbors:
            n_row, n_col = row + neighbor[0], col + neighbor[1]
            if 0 <= n_row < self.rows and 0 <= n_col < self.cols:
                live_neighbors += self.grid[n_row][n_col]

        if self.grid[row][col] == 1:
            return 1 if live_neighbors in (2, 3) else 0
        else:
            return 1 if live_neighbors == 3 else 0
