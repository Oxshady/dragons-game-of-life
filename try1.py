from tkinter import *

class Dragons:
    def __init__(self):
        self.width=800
        self.height=700
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
        self.root.geometry(f"1000x1000")
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

        start_button = Button(self.lobby, text="Start Game", font=("Helvetica", 16), command=self.start_game)
        start_button.grid(row=2, column=0, pady=10, padx=20)

        setting_button = Button(self.lobby, text="Setting", font=("Helvetica", 16), command=lambda: self.switch_frames(self.settings))
        setting_button.grid(row=3, column=0, pady=10, padx=20)

    def setting_page(self):
        self.settings.grid_rowconfigure(0, weight=1)
        self.settings.grid_rowconfigure(1, weight=1)
        self.settings.grid_rowconfigure(2, weight=1)
        self.settings.grid_columnconfigure(0, weight=1)

        title = Label(self.settings, text="Settings", font=("Helvetica", 24, "bold"), bg="white")
        title.grid(row=1, column=0, pady=20, padx=20, sticky="n")

        return_button = Button(self.settings, text="Lobby", font=("Helvetica", 16), command=lambda: self.switch_frames(self.lobby))
        return_button.grid(row=2, column=0, pady=10, padx=20)

    def game_page(self):
        title = Label(self.game, text="Game Page", font=("Helvetica", 24, "bold"), bg="white")
        title.grid(row=1, column=0, pady=20, padx=20, sticky="n")

        lobby_button = Button(self.game, text="Lobby", font=("Helvetica", 16), command=lambda: self.switch_frames(self.lobby))
        lobby_button.grid(row=2, column=0, pady=10, padx=20)

    def switch_frames(self, frame):
        frame.tkraise()

    def start_game(self):
        self.switch_frames(self.game)
        self.initialize_game_canvas()

    def initialize_game_canvas(self):
        self.canvas = Canvas(self.game, width=self.width, height=self.height - 65)
        self.canvas.grid(row=3, column=0, sticky="nsew")

        self.draw_grid()

        controls_frame = Frame(self.game)
        controls_frame.grid(row=4, column=0, pady=10)

        Label(controls_frame, text="Width:").grid(row=0, column=0)
        self.width_entry = Entry(controls_frame, width=5)
        self.width_entry.grid(row=0, column=1)
        self.width_entry.insert(0, "800")

        Label(controls_frame, text="Height:").grid(row=0, column=2)
        self.height_entry = Entry(controls_frame, width=5)
        self.height_entry.grid(row=0, column=3)
        self.height_entry.insert(0, "600")

        self.speed_scale = Scale(controls_frame, from_=0, to=100, orient=HORIZONTAL, command=self.update_speed)
        self.speed_scale.grid(row=0, column=5, ipady=7)
        self.speed_label = Label(controls_frame, text="Speed: 0")
        self.speed_label.grid(row=0, column=6)

        resize_button = Button(controls_frame, text="Update", padx=10, command=self.resize)
        resize_button.grid(row=0, column=4)

    def draw_grid(self):
        self.canvas.delete("all")
        for row in range((self.height - 65) // 10):
            for col in range(self.width // 10):
                x1 = col * 10
                y1 = row * 10
                x2 = x1 + 10
                y2 = y1 + 10
                # Fill with white
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")

    def resize(self):
        self.width = int(self.width_entry.get())
        self.height = int(self.height_entry.get())
        self.canvas.config(width=self.width, height=self.height - 65)
        self.draw_grid()

    def update_speed(self, value):
        self.speed_label.config(text=f"Speed: {value}")

    def run(self):
        self.lobby_page()
        self.setting_page()
        self.game_page()
        self.switch_frames(self.lobby)

if __name__ == "__main__":
    x = Dragons()
