from tkinter import *
from tkinter import ttk
import random

class GameOfLife:
    def __init__(self, frame, rows=20, cols=20, cell_size=20):
        self.frame = frame
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.is_running = False

        self.canvas = Canvas(frame, width=cols * cell_size, height=rows * cell_size, bg='white', highlightbackground="#ccc")
        self.canvas.pack(pady=20)

        self.grid = [[random.choice([0, 1]) for _ in range(cols)] for _ in range(rows)]
        self.temp_grid = [[0 for _ in range(cols)] for _ in range(rows)]
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
        self.start_button.pack(side='left', padx=5)

        self.stop_button = Button(button_frame, text='Stop', command=self.stop_game, font=("Arial", 14), bg="#F44336", fg="white", relief=FLAT)
        self.stop_button.pack(side='left', padx=5)

        self.reset_button = Button(button_frame, text='Reset', command=self.reset_game, font=("Arial", 14), bg="#FF9800", fg="white", relief=FLAT)
        self.reset_button.pack(side='left', padx=5)

        self.randomize_button = Button(button_frame, text='Randomize', command=self.randomize_grid, font=("Arial", 14), bg="#2196F3", fg="white", relief=FLAT)
        self.randomize_button.pack(side='left', padx=5)
        from dragons import Dragons
        self.lobby_button = Button(button_frame, text='Lobby', command=lambda: Dragons.lobby.tkraise(), font=("Arial", 14), bg="#FF5722", fg="white", relief=FLAT)
        self.lobby_button.pack(side='left', padx=5)

        self.canvas.bind("<Button-1>", self.toggle_cell)

        self.draw_grid()

    def set_colors(self):
        self.alive_color = self.alive_color_combobox.get()
        self.dead_color = self.dead_color_combobox.get()
        self.draw_grid()

    def toggle_cell(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] = 1 - self.grid[row][col]
            self.draw_grid()

    def randomize_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col] = random.choice([0, 1])
        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        for row in range(self.rows):
            for col in range(self.cols):
                color = self.alive_color if self.grid[row][col] == 1 else self.dead_color
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#ccc")

    def update(self):
        if not self.is_running:
            return
        for row in range(self.rows):
            for col in range(self.cols):
                live_neighbors = self.get_live_neighbors(row, col)
                if self.grid[row][col] == 1:
                    if live_neighbors < 2 or live_neighbors > 3:
                        self.temp_grid[row][col] = 0
                    else:
                        self.temp_grid[row][col] = 1
                else:
                    if live_neighbors == 3:
                        self.temp_grid[row][col] = 1
                    else:
                        self.temp_grid[row][col] = 0

        self.grid, self.temp_grid = self.temp_grid, self.grid
        self.draw_grid()
        self.frame.after(100, self.update)

    def get_live_neighbors(self, row, col):
        live_neighbors = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                r = (row + i) % self.rows
                c = (col + j) % self.cols
                live_neighbors += self.grid[r][c]
        return live_neighbors

    def start_game(self):
        self.is_running = True
        self.update()

    def stop_game(self):
        self.is_running = False

    def reset_game(self):
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.temp_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.draw_grid()

    def update_grid(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.temp_grid = [[0 for _ in range(cols)] for _ in range(rows)]

        self.canvas.config(width=cols * self.cell_size, height=rows * self.cell_size)

        self.draw_grid()
