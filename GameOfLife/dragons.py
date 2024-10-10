from tkinter import *
from gameOfLife import GameOfLife
class Dragons:
    def __init__(self):
        self.root = Tk()
        self.config_root()
        self.lobby = Frame(self.root, bg="#F0F0F0")
        self.settings = Frame(self.root, bg="#F0F0F0")
        self.game = Frame(self.root, bg="#F0F0F0")
        self.frames_config()
        self.current_game = None
        self.run()
        self.app_loop()

    def config_root(self):
        """Configure the main application window."""
        self.root.title("The Game of Life")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#F0F0F0")

    def frames_config(self):
        """Configure the layout for the different frames in the application."""
        for frame in (self.lobby, self.settings, self.game):
            frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def app_loop(self):
        """Start the main event loop of the application."""
        self.root.mainloop()

    def lobby_page(self):
        """Create the lobby page with the game title and buttons."""
        title = Label(self.lobby, text="The Game of Life", font=("Arial", 30, "bold"), bg="#F0F0F0", fg="#333")
        title.pack(pady=(30, 10))

        start_button = Button(self.lobby, text="Start Game", font=("Arial", 16), command=self.start_game, bg="#4CAF50", fg="white", relief=FLAT)
        start_button.pack(pady=10, padx=20, fill=X)

        setting_button = Button(self.lobby, text="Settings", font=("Arial", 16), command=lambda: self.switch_frames(self.settings), bg="#2196F3", fg="white", relief=FLAT)
        setting_button.pack(pady=10, padx=20, fill=X)

    def setting_page(self):
        """Create the settings page for adjusting game parameters."""
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
        """Apply the new settings for rows and columns."""
        try:
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())
            self.game_page(rows, cols)
        except ValueError:
            pass

    def game_page(self, rows=20, cols=20):
        """Create the game instance or update it if it already exists."""
        if self.current_game is None:
            self.current_game = GameOfLife(self.game, rows, cols)
        else:
            self.current_game.update_grid(rows, cols)

        self.switch_frames(self.game)

    def switch_frames(self, frame):
        """Switch between different frames in the application."""
        frame.tkraise()

    def start_game(self):
        """Start the game with default settings."""
        self.game_page()

    def run(self):
        """Initialize the application pages."""
        self.lobby_page()
        self.setting_page()
        self.switch_frames(self.lobby)
