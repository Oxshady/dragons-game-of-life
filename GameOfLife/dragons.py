from tkinter import *

class Dragons:
    root = Tk()
    lobby = Frame(root, bg="#F0F0F0")

    def __init__(self):
        self.root = self.__class__.root
        self.config_root()
        self.lobby = self.__class__.lobby
        self.settings = Frame(self.root, bg="#F0F0F0")
        self.game = Frame(self.root, bg="#F0F0F0")
        self.rules = Frame(self.root, bg="#F0F0F0")
        self.frames_config()
        self.current_game = None
        self.run()
        self.app_loop()

    def config_root(self):
        self.root.title("The Game of Life")
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#F0F0F0")

    def frames_config(self):
        for frame in (self.lobby, self.settings, self.game, self.rules):
            frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def app_loop(self):
        self.root.mainloop()

    def lobby_page(self):
        title = Label(self.lobby, text="The Game of Life", font=("Arial", 30, "bold"), bg="#F0F0F0", fg="#333")
        title.pack(pady=(30, 10))

        start_button = Button(self.lobby, text="Start Game", font=("Arial", 16), command=self.start_game, bg="#4CAF50", fg="white", relief=FLAT)
        start_button.pack(pady=10, padx=20, fill=X)

        setting_button = Button(self.lobby, text="Settings", font=("Arial", 16), command=lambda: self.switch_frames(self.settings), bg="#2196F3", fg="white", relief=FLAT)
        setting_button.pack(pady=10, padx=20, fill=X)

        rules_button = Button(self.lobby, text="Rules", font=("Arial", 16), command=lambda: self.switch_frames(self.rules), bg="#FF9800", fg="white", relief=FLAT)
        rules_button.pack(pady=10, padx=20, fill=X)

        quit_button = Button(self.lobby, text="Quit", font=("Arial", 16), command=self.root.quit, bg="#F44336", fg="white", relief=FLAT)
        quit_button.pack(pady=10, padx=20, fill=X)

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

    def rules_page(self):
        title = Label(self.rules, text="Game Rules", font=("Arial", 30, "bold"), bg="#F0F0F0", fg="#333")
        title.pack(pady=(30, 10))

        description = (
            "The Game of Life is a cellular automaton devised by the British mathematician John Conway in 1970.\n"
            "It consists of a grid of cells that live, die, or multiply based on a set of rules:\n"
            "1. Any live cell with fewer than two live neighbors dies (underpopulation).\n"
            "2. Any live cell with two or three live neighbors lives on to the next generation.\n"
            "3. Any live cell with more than three live neighbors dies (overpopulation).\n"
            "4. Any dead cell with exactly three live neighbors becomes a live cell (reproduction).\n"
            "These rules determine the fate of each cell in each generation."
        )
        
        rules_label = Label(self.rules, text=description, font=("Arial", 14), bg="#F0F0F0", fg="#333", wraplength=700, justify='left')
        rules_label.pack(pady=(10, 10))

        return_button = Button(self.rules, text="Lobby", font=("Arial", 16), command=lambda: self.switch_frames(self.lobby), bg="#FF5722", fg="white", relief=FLAT)
        return_button.pack(pady=10)

    def apply_settings(self):
        try:
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())
            self.game_page(rows, cols)
        except ValueError:
            pass

    def game_page(self, rows=20, cols=20):
        if self.current_game is None:
            from gameOfLife import GameOfLife
            self.current_game = GameOfLife(self.game, rows, cols)
        else:
            self.current_game.update_grid(rows, cols)
        self.switch_frames(self.game)

    def switch_frames(self, frame):
        frame.tkraise()

    def start_game(self):
        self.game_page()

    def run(self):
        self.lobby_page()
        self.setting_page()
        self.rules_page()
        self.switch_frames(self.lobby)
