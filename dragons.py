from tkinter import *
import random

class Dragons:
    def __init__(self):
        self.root = Tk()
        self.config_root()
        self.lobby = Frame(self.root, bg="white")
        self.settings = Frame(self.root, bg="white")
        self.game = Frame(self.root, bg="white")
        self.frames_config()
        self.run()
        self.app_loop()

    def config_root(self):
        self.root.title("The Game of Life")
        self.root.geometry("800x600")
        self.root.configure(bg="white")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def frames_config(self):
        self.lobby.grid(row=0, column=0, sticky="nsew")
        self.game.grid(row=0, column=0, sticky="nsew")
        self.settings.grid(row=0, column=0, sticky="nsew")

    def app_loop(self):
        self.root.mainloop()

    def lobby_page(self):
        self.lobby.grid_rowconfigure(0, weight=1)
        self.lobby.grid_rowconfigure(1, weight=1)
        self.lobby.grid_rowconfigure(2, weight=1)
        self.lobby.grid_rowconfigure(3, weight=1)
        self.lobby.grid_rowconfigure(4, weight=1)
        self.lobby.grid_columnconfigure(0, weight=1)

        title = Label(self.lobby, text="The Game of Life", font=("Helvetica", 24, "bold"), bg="white")
        title.grid(row=1, column=0, pady=20, padx=20, sticky="n")

        start_button = Button(self.lobby, text="Start Game", font=("Helvetica", 16), command=lambda: self.switch_frames(self.game))
        start_button.grid(row=2, column=0, pady=10, padx=20)

        setting_button = Button(self.lobby, text="Settings", font=("Helvetica", 16), command=lambda: self.switch_frames(self.settings))
        setting_button.grid(row=3, column=0, pady=10, padx=20)

    def setting_page(self):
        self.settings.grid_rowconfigure(0, weight=1)
        self.settings.grid_rowconfigure(1, weight=1)
        self.settings.grid_rowconfigure(2, weight=1)
        self.settings.grid_rowconfigure(3, weight=1)
        self.settings.grid_rowconfigure(4, weight=1)
        self.settings.grid_columnconfigure(0, weight=1)

        title = Label(self.settings, text="Settings", font=("Helvetica", 24, "bold"), bg="white")
        title.grid(row=1, column=0, pady=20, padx=20, sticky="n")
        return_button = Button(self.settings, text="Lobby", font=("Helvetica", 16), command=lambda: self.switch_frames(self.lobby))
        return_button.grid(row=2, column=0, pady=10, padx=20)

        self.rows_entry = Entry(self.settings, width=5)
        self.rows_entry.insert(0, "20")
        self.rows_entry.grid(row=3, column=0, pady=5)

        self.cols_entry = Entry(self.settings, width=5)
        self.cols_entry.insert(0, "20")
        self.cols_entry.grid(row=4, column=0, pady=5)

        apply_button = Button(self.settings, text="Apply", command=self.apply_settings)
        apply_button.grid(row=5, column=0, pady=10)

    def apply_settings(self):
        try:
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())
            self.game_page(rows, cols)
        except ValueError:
            pass

    def game_page(self, rows=20, cols=20):
        self.game_of_life = GameOfLife(self.game, rows, cols)
        self.switch_frames(self.game)

    def switch_frames(self, frame):
        frame.tkraise()

    def run(self):
        self.lobby_page()
        self.setting_page()
        self.game_page()
        self.switch_frames(self.lobby)


class GameOfLife:
    def __init__(self, frame, rows=20, cols=20, cell_size=20, alive_color='black', dead_color='white'):
        self.frame = frame
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.alive_color = alive_color
        self.dead_color = dead_color
        self.is_running = False

        self.canvas = Canvas(frame, width=cols * cell_size, height=rows * cell_size, bg='white')
        self.canvas.pack()

        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.temp_grid = [[0 for _ in range(cols)] for _ in range(rows)]

        self.draw_grid()

        self.canvas.bind('<Button-1>', self.toggle_cell)

        self.start_button = Button(frame, text='Start', command=self.start_game)
        self.start_button.pack(side='left')

        self.stop_button = Button(frame, text='Stop', command=self.stop_game)
        self.stop_button.pack(side='left')

        self.reset_button = Button(frame, text='Reset', command=self.reset_game)
        self.reset_button.pack(side='left')

        self.randomize_button = Button(frame, text='Randomize', command=self.randomize_grid)
        self.randomize_button.pack(side='left')

        self.alive_color_entry = Entry(frame)
        self.alive_color_entry.insert(0, 'black')
        self.alive_color_entry.pack(side='left')

        self.dead_color_entry = Entry(frame)
        self.dead_color_entry.insert(0, 'white')
        self.dead_color_entry.pack(side='left')

        color_button = Button(frame, text='Set Colors', command=self.set_colors)
        color_button.pack(side='left')

    def set_colors(self):
        """Set the colors for alive and dead cells based on user input."""
        self.alive_color = self.alive_color_entry.get()
        self.dead_color = self.dead_color_entry.get()
        self.draw_grid()

    def draw_grid(self):
        """Draw the grid on the canvas based on the current state."""
        self.canvas.delete('all')
        for row in range(self.rows):
            for col in range(self.cols):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = self.alive_color if self.grid[row][col] == 1 else self.dead_color
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='gray')

    def toggle_cell(self, event):
        """Toggle the cell state between alive (1) and dead (0) when clicked."""
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if 0 <= col < self.cols and 0 <= row < self.rows:
            self.grid[row][col] = 1 if self.grid[row][col] == 0 else 0
        self.draw_grid()

    def start_game(self):
        """Start the game loop."""
        if not self.is_running:
            self.is_running = True
            self.run_game()

    def stop_game(self):
        """Stop the game loop."""
        self.is_running = False

    def reset_game(self):
        """Reset the grid to all dead cells."""
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.draw_grid()

    def randomize_grid(self):
        """Randomize the grid with alive and dead cells."""
        self.grid = [[random.choice([0, 1]) for _ in range(self.cols)] for _ in range(self.rows)]
        self.draw_grid()

    def run_game(self):
        """Run the game's logic, updating the grid for each step."""
        if self.is_running:
            self.update_grid()
            self.draw_grid()
            self.frame.after(200, self.run_game)

    def update_grid(self):
        """Apply the rules of Conway's Game of Life to update the grid."""
        for row in range(self.rows):
            for col in range(self.cols):
                alive_neighbors = self.count_alive_neighbors(row, col)

                if self.grid[row][col] == 1:
                    if alive_neighbors < 2 or alive_neighbors > 3:
                        self.temp_grid[row][col] = 0
                    else:
                        self.temp_grid[row][col] = 1
                else:
                    if alive_neighbors == 3:
                        self.temp_grid[row][col] = 1
                    else:
                        self.temp_grid[row][col] = 0

        self.grid, self.temp_grid = self.temp_grid, self.grid

    def count_alive_neighbors(self, row, col):
        """Count the number of alive neighbors for a given cell."""
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        count = 0
        for d in directions:
            r, c = row + d[0], col + d[1]
            if 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] == 1:
                count += 1
        return count

if __name__ == "__main__":
    x = Dragons()
