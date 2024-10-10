from tkinter import *
from tkinter import ttk
import random

class Dragons:
    def __init__(self):
        self.root = Tk()
        self.config_root()
        self.lobby = Frame(self.root, bg="#F0F0F0")
        self.settings = Frame(self.root, bg="#F0F0F0")
        self.game = Frame(self.root, bg="#F0F0F0")
        self.frames_config()
        self.run()
        self.app_loop()

    def config_root(self):
        self.root.title("The Game of Life")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#F0F0F0")

    def frames_config(self):
        for frame in (self.lobby, self.settings, self.game):
            frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def app_loop(self):
        self.root.mainloop()

    def lobby_page(self):
        title = Label(self.lobby, text="The Game of Life", font=("Arial", 30, "bold"), bg="#F0F0F0", fg="#333")
        title.pack(pady=(30, 10))

        start_button = Button(self.lobby, text="Start Game", font=("Arial", 16), command=lambda: self.switch_frames(self.game), bg="#4CAF50", fg="white", relief=FLAT)
        start_button.pack(pady=10, padx=20, fill=X)

        setting_button = Button(self.lobby, text="Settings", font=("Arial", 16), command=lambda: self.switch_frames(self.settings), bg="#2196F3", fg="white", relief=FLAT)
        setting_button.pack(pady=10, padx=20, fill=X)

    def setting_page(self):
        title = Label(self.settings, text="Settings", font=("Arial", 30, "bold"), bg="#F0F0F0", fg="#333")
        title.pack(pady=(30, 10))

        return_button = Button(self.settings, text="Lobby", font=("Arial", 16), command=lambda: self.switch_frames(self.lobby), bg="#FF5722", fg="white", relief=FLAT)
        return_button.pack(pady=10, padx=20, fill=X)

        entry_frame = Frame(self.settings, bg="#F0F0F0")
        entry_frame.pack(pady=20)

        self.rows_entry = Entry(entry_frame, width=5, font=("Arial", 14), justify='center')
        self.rows_entry.insert(0, "20")
        self.rows_entry.grid(row=0, column=0, padx=5)

        self.cols_entry = Entry(entry_frame, width=5, font=("Arial", 14), justify='center')
        self.cols_entry.insert(0, "20")
        self.cols_entry.grid(row=0, column=1, padx=5)

        apply_button = Button(self.settings, text="Apply", font=("Arial", 14), command=self.apply_settings, bg="#4CAF50", fg="white", relief=FLAT)
        apply_button.pack(pady=10)

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

        self.draw_grid()

        self.canvas.bind('<Button-1>', self.toggle_cell)

    def set_colors(self):
        """Set the colors for alive and dead cells based on user selection."""
        self.alive_color = self.alive_color_combobox.get()
        self.dead_color = self.dead_color_combobox.get()
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
