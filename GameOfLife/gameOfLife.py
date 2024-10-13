import customtkinter as ctk
from tkinter import Canvas, colorchooser
import random
import json
import pygame

def play_sound_in_thread(sound_file):
    sound = pygame.mixer.Sound(sound_file)
    sound.play()

class GameOfLife:
    def __init__(self, frame, app, rows=20, cols=20, cell_size=20):
        self.frame = frame
        self.app = app  # Reference to the Dragons instance
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.is_running = False
        pygame.mixer.init()
        pygame.mixer.music.set_volume(1.0)

        self.canvas = Canvas(frame, width=cols * cell_size, height=rows * cell_size, bg='white', highlightbackground="#ccc")
        self.canvas.pack(pady=20)

        self.grid = [[random.choice([0, 1]) for _ in range(cols)] for _ in range(rows)]
        self.temp_grid = [[0 for _ in range(cols)] for _ in range(rows)]

        self.canvas.bind("<Button-1>", self.toggle_cell)

        self.slider_frame = ctk.CTkFrame(frame)
        self.slider_frame.pack(pady=10)

        self.speed_scale = ctk.CTkSlider(self.slider_frame, from_=10, to=500, number_of_steps=49, command=self.update_speed)
        self.speed_scale.set(250)
        self.speed_scale.pack(side='left', padx=5)
        self.speed_label = ctk.CTkLabel(self.slider_frame, text="Speed: 250ms")
        self.speed_label.pack(side='left', padx=5)

        self.zoom_scale = ctk.CTkSlider(self.slider_frame, from_=10, to=37, number_of_steps=27, command=self.zoom_grid)
        self.zoom_scale.set(self.cell_size)
        self.zoom_scale.pack(side='left', padx=5)
        self.zoom_label = ctk.CTkLabel(self.slider_frame, text=f"Zoom: {self.cell_size}")
        self.zoom_label.pack(side='left', padx=5)

        self.color_frame = ctk.CTkFrame(frame)
        self.color_frame.pack(pady=10)

        self.alive_color = 'black'
        self.dead_color = 'white'

        self.alive_color_button = ctk.CTkButton(self.color_frame, text="Alive Color", command=self.choose_alive_color)
        self.alive_color_button.grid(row=0, column=0, padx=5)

        self.dead_color_button = ctk.CTkButton(self.color_frame, text="Dead Color", command=self.choose_dead_color)
        self.dead_color_button.grid(row=0, column=1, padx=5)

        self.boundary_condition = 'Finite'
        self.boundary_conditions = ['Finite', 'Reflective', 'Toroidal', 'Infinite']
        self.boundary_combobox = ctk.CTkOptionMenu(self.color_frame, values=self.boundary_conditions, command=self.update_boundary_condition)
        self.boundary_combobox.set("Select Boundary")
        self.boundary_combobox.grid(row=1, column=0, padx=5)

        self.toggle_button = ctk.CTkButton(self.color_frame, text="Start", command=self.toggle_game)
        self.toggle_button.grid(row=0, column=2, padx=5)

        self.clear_button = ctk.CTkButton(self.color_frame, text="Clear", command=lambda: [self.clear_grid(), play_sound_in_thread("sound_effects/reset.wav")])
        self.clear_button.grid(row=0, column=3, padx=5)

        self.randomize_button = ctk.CTkButton(self.color_frame, text="Randomize", command=lambda: [self.randomize_grid(), play_sound_in_thread("sound_effects/click2.wav")])
        self.randomize_button.grid(row=0, column=4, padx=5)

        self.lobby_button = ctk.CTkButton(self.color_frame, text="Lobby", command=self.return_to_lobby)
        self.lobby_button.grid(row=0, column=5, padx=5)

        save_button = ctk.CTkButton(self.color_frame, text="Save Pattern", command=lambda: [self.save_pattern(), play_sound_in_thread("sound_effects/click2.wav")])
        save_button.grid(row=1, column=2, padx=5, pady=5)

        load_button = ctk.CTkButton(self.color_frame, text="Load Pattern", command=lambda: [self.load_pattern(), play_sound_in_thread("sound_effects/click2.wav")])
        load_button.grid(row=1, column=3, padx=5, pady=5)

        self.draw_grid()
        self.update_canvas()
        print(type(self.frame))


    def return_to_lobby(self):
        if hasattr(self.app, 'switch_frames') and hasattr(self.app, 'lobby'):
            self.app.switch_frames(self.app.lobby)
            play_sound_in_thread("sound_effects/navigate.wav")
        else:
            print("Error: Unable to return to lobby. Required attributes not found.")

    def toggle_cell(self, event):
        x, y = event.x, event.y
        row = y // self.cell_size
        col = x // self.cell_size
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] = 1 if self.grid[row][col] == 0 else 0
            play_sound_in_thread("sound_effects/click_cell.wav")
            self.update_canvas()

    def draw_grid(self):
        for i in range(self.rows):
            for j in range(self.cols):
                color = self.alive_color if self.grid[i][j] == 1 else self.dead_color
                self.canvas.create_rectangle(j * self.cell_size, i * self.cell_size,
                                              (j + 1) * self.cell_size, (i + 1) * self.cell_size,
                                              fill=color, outline="#ccc")

    def update_canvas(self):
        self.canvas.delete("all")
        self.draw_grid()

    def update_boundary_condition(self, choice):
        self.boundary_condition = choice

    def update_grid(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cell_size = int(self.zoom_scale.get())
        self.grid = [[random.choice([0, 1]) for _ in range(cols)] for _ in range(rows)]
        self.temp_grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.canvas.config(width=self.cols * self.cell_size, height=self.rows * self.cell_size)
        self.update_canvas()

    def zoom_grid(self, value):
        self.cell_size = int(float(value))
        self.canvas.config(width=self.cols * self.cell_size, height=self.rows * self.cell_size)
        self.update_canvas()
        self.zoom_label.configure(text=f"Zoom: {self.cell_size}")

    def update_speed(self, value):
        speed = int(float(value))
        self.speed_label.configure(text=f"Speed: {speed}ms")

    def choose_alive_color(self):
        color = colorchooser.askcolor(title="Choose color for alive cells")[1]
        if color:
            self.alive_color = color
            self.update_canvas()

    def choose_dead_color(self):
        color = colorchooser.askcolor(title="Choose color for dead cells")[1]
        if color:
            self.dead_color = color
            self.update_canvas()

    def toggle_game(self):
        if self.is_running:
            self.stop_game()
            self.toggle_button.configure(text="Start")
            play_sound_in_thread("sound_effects/exit3.wav")
        else:
            self.start_game()
            self.toggle_button.configure(text="Pause")
            play_sound_in_thread("sound_effects/click2.wav")

    def start_game(self):
        self.is_running = True
        self.run_game()

    def run_game(self):
        if self.is_running:
            self.update_cells()
            self.update_canvas()
            self.frame.after(int(self.speed_scale.get()), self.run_game)

    def stop_game(self):
        self.is_running = False

    def clear_grid(self):
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.update_canvas()

    def randomize_grid(self):
        self.grid = [[random.choice([0, 1]) for _ in range(self.cols)] for _ in range(self.rows)]
        self.update_canvas()

    def update_cells(self):
        for i in range(self.rows):
            for j in range(self.cols):
                live_neighbors = self.count_live_neighbors(i, j)
                if self.grid[i][j] == 1:
                    self.temp_grid[i][j] = 1 if live_neighbors in (2, 3) else 0
                else:
                    self.temp_grid[i][j] = 1 if live_neighbors == 3 else 0
        self.grid, self.temp_grid = self.temp_grid, self.grid

    def count_live_neighbors(self, row, col):
        def finite_boundary(i, j):
            return 0 <= i < self.rows and 0 <= j < self.cols
        def infinite_boundary(i, j):
                return self.grid[i][j] if (0 <= i < self.rows and 0 <= j < self.cols) else 0
        def reflective_boundary(i, j):
            reflected_i = max(0, min(i, self.rows - 1))
            reflected_j = max(0, min(j, self.cols - 1))
            return reflected_i, reflected_j

        def toroidal_boundary(i, j):
            ni = (i + self.rows) % self.rows
            nj = (j + self.cols) % self.cols
            return ni, nj

        count = 0
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if i == row and j == col:
                    continue

                if self.boundary_condition == 'Finite':
                    if finite_boundary(i, j):
                        count += self.grid[i][j]

                elif self.boundary_condition == 'Reflective':
                    reflected_i, reflected_j = reflective_boundary(i, j)
                    count += self.grid[reflected_i][reflected_j]

                elif self.boundary_condition == 'Toroidal':
                    ni, nj = toroidal_boundary(i, j)
                    count += self.grid[ni][nj]

                elif self.boundary_condition == 'Infinite':
                    count += infinite_boundary(i, j)

        return count

    def save_pattern(self):
        file_path = ctk.filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "w") as file:
                json.dump(self.grid, file)

    def load_pattern(self):
        file_path = ctk.filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "r") as file:
                self.grid = json.load(file)
            self.draw_grid()