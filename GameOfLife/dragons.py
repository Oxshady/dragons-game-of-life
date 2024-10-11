from tkinter import *
import pygame
from tkinter import ttk
# from playsound import playsound
# import threading

# def play_sound_in_thread(sound_file):
#     threading.Thread(target=playsound, args=(sound_file,), daemon=True).start()

def play_sound_in_thread(sound_file):
    # Load and play sound effect using pygame.mixer
    sound = pygame.mixer.Sound(sound_file)
    sound.play()

class Dragons:
    """The main application class for The Game of Life."""
    root = Tk()
    is_muted = False
    lobby = Frame(root, bg="#F0F0F0")

    def __init__(self):
        """Initialize the Dragons class and configure the main application window."""
        pygame.mixer.init()
        pygame.mixer.music.set_volume(1.0)
        self.root = self.__class__.root
        self.config_root()
        self.lobby = self.__class__.lobby
        self.settings = Frame(self.root, bg="#F0F0F0")
        self.game = Frame(self.root, bg="#F0F0F0")
        self.rules = Frame(self.root, bg="#F0F0F0")
        self.frames_config()
        self.current_game = None
        
        self.music_tracks = {
            "Ahemd Kamel": "./music/Ahmed Kamel - Baad El Kalam  Official Lyrics Video - 2023  احمد كامل - بعد الكلام.mp3",
            "Cairokee": "./music/Cairokee - Law Kan 3andi Guitar _ كايروكي - لو كان عندي جيتار ( 128kbps ).mp3",
            "Gipper Kings": "./music/Gipsy Kings - Volare (Nel blu dipinto di blu)(MP3_70K).mp3",
            "Ahmed Santa: Emna3-elklam": "./music/Ahmed Santa - Emna3 El Kalam  أحمد سانتا - امنع الكلام (Official Audio) (Prod. Alfy).mp3",
            "Ahmed Santa: Ahmed-santa": "./music/Ahmed Santa - Ahmed Santa  أحمد سانتا - أحمد سانتا (Prod. Mello) (Audio).mp3"
        }
        self.music_file = "./music/Ahmed Santa - Emna3 El Kalam  أحمد سانتا - امنع الكلام (Official Audio) (Prod. Alfy).mp3"
        
        self.run()
        self.app_loop()

    def config_root(self):
        """Configure the main application window."""
        self.root.title("The Game of Life")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#F0F0F0")

    def frames_config(self):
        """Configure the layout of the frames in the application."""
        for frame in (self.lobby, self.settings, self.game, self.rules):
            frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def app_loop(self):
        """Start the main application loop."""
        self.root.mainloop()

    def play_navigation_sound(self):
        """Play sound of navigation"""
        play_sound_in_thread("sound_effects/navigate.wav")

    def lobby_page(self):
        """Set up the lobby page with buttons to navigate to other pages."""
        title = Label(self.lobby, text="The Game of Life", font=("Arial", 30, "bold"), bg="#F0F0F0", fg="#333")
        title.pack(pady=(30, 10))

        button_frame = Frame(self.lobby, bg="#F0F0F0")
        button_frame.pack(pady=20)

        start_button = Button(button_frame, text="Start Game", font=("Arial", 16), command=self.start_game, bg="#4CAF50", fg="white", relief=FLAT)
        start_button.grid(row=0, column=0, padx=10, pady=10)

        setting_button = Button(button_frame, text="Settings", font=("Arial", 16), command=lambda: [self.play_navigation_sound(), self.switch_frames(self.settings)], bg="#2196F3", fg="white", relief=FLAT)
        setting_button.grid(row=0, column=1, padx=10, pady=10)

        rules_button = Button(button_frame, text="Rules", font=("Arial", 16), command=lambda: [self.play_navigation_sound(), self.switch_frames(self.rules)], bg="#FF9800", fg="white", relief=FLAT)
        rules_button.grid(row=0, column=2, padx=10, pady=10)

        quit_button = Button(button_frame, text="Quit", font=("Arial", 16), command=lambda: [play_sound_in_thread("sound_effects/exit3.wav"), self.root.after(200, self.root.quit)], bg="#F44336", fg="white", relief=FLAT)
        quit_button.grid(row=0, column=3, padx=10, pady=10)

        music_frame = Frame(self.lobby, bg="#F0F0F0")
        music_frame.pack(pady=10)

        self.current_music_label = Label(music_frame, text="Current Music: Ahmed Santa: Emna3-elklam", font=("Arial", 14), bg="#F0F0F0", fg="#333")
        self.current_music_label.pack(pady=5)

        self.music_selection = ttk.Combobox(self.lobby, values=list(self.music_tracks.keys()), state="readonly")
        self.music_selection.pack(pady=10)
        self.music_selection.set("Ahmed Santa: Emna3-elklam")
        self.music_selection.bind("<<ComboboxSelected>>", self.update_music_selection)

        self.mute_button = Button(self.lobby, text="Mute", font=("Arial", 16), command=self.toggle_mute, bg="#ff5722", fg="white", relief=FLAT)
        self.mute_button.pack(pady=10, padx=20, fill=X)

        self.play_music()


    def update_music_selection(self, event):
        selected_track = self.music_selection.get()
        self.music_file = self.music_tracks[selected_track]
        self.play_music()

    def toggle_mute(self):
        if not self.is_muted:
            pygame.mixer.music.set_volume(0)
            self.mute_button.config(text="Unmute")
            play_sound_in_thread("sound_effects/navigate.wav")
        else:
            pygame.mixer.music.set_volume(1)
            self.mute_button.config(text="Mute")
            play_sound_in_thread("sound_effects/navigate.wav")
        self.is_muted = not self.is_muted

    def play_music(self):
        """Play the background music."""
        try:
            pygame.mixer.music.load(self.music_file)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Error playing music: {e}") 

    def stop_music(self):
        pygame.mixer.music.stop()

    def setting_page(self):
        """Set up the settings page with options to configure the game grid."""
        title = Label(self.settings, text="Settings", font=("Arial", 30, "bold"), bg="#F0F0F0", fg="#333")
        title.pack(pady=(30, 10))

        entry_frame = Frame(self.settings, bg="#F0F0F0")
        entry_frame.pack(pady=20)

        # Width and height labels
        width_label = Label(entry_frame, text="Width", font=("Arial", 14), bg="#F0F0F0")
        width_label.grid(row=0, column=0, padx=5)

        height_label = Label(entry_frame, text="Height", font=("Arial", 14), bg="#F0F0F0")
        height_label.grid(row=0, column=1, padx=5)

        self.rows_entry = Entry(entry_frame, width=5, font=("Arial", 14), justify='center')
        self.rows_entry.insert(0, "20")
        self.rows_entry.grid(row=1, column=0, padx=5)

        self.cols_entry = Entry(entry_frame, width=5, font=("Arial", 14), justify='center')
        self.cols_entry.insert(0, "20")
        self.cols_entry.grid(row=1, column=1, padx=5)

        apply_button = Button(self.settings, text="Apply", font=("Arial", 14), command=self.apply_settings, bg="#4CAF50", fg="white", relief=FLAT)
        apply_button.pack(pady=10)

        return_button_music = Button(self.settings, text="Lobby", font=("Arial", 16), command=lambda: [self.play_navigation_sound(), self.switch_frames(self.lobby)], bg="#FF5722", fg="white", relief=FLAT)
        return_button_music.pack(pady=10)

        stop_button_music = Button(self.settings, text="Stop Music", font=("Arial", 16), command=self.stop_music, bg="#FF5722", fg="white", relief=FLAT)
        stop_button_music.pack(pady=10)


    def rules_page(self):
        """Set up the rules page with a description of the game rules."""
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

        return_button = Button(self.rules, text="Lobby", font=("Arial", 16), command=lambda: [self.play_navigation_sound(), self.switch_frames(self.lobby)], bg="#FF5722", fg="white", relief=FLAT)
        return_button.pack(pady=10)

    def apply_settings(self):
        """Apply the settings for the game grid and start the game."""
        try:
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())
            self.game_page(rows, cols)
            if self.current_game:
                self.current_game.start_game()
            play_sound_in_thread("sound_effects/start_game2.mp3")
        except ValueError:
            pass

    def game_page(self, rows=20, cols=20):
        """Set up the game page with the specified grid size."""
        if self.current_game is None:
            from gameOfLife import GameOfLife
            self.current_game = GameOfLife(self.game, rows, cols)
        else:
            self.current_game.update_grid(rows, cols)
        self.switch_frames(self.game)

    def switch_frames(self, frame):
        """Switch to the specified frame."""
        frame.tkraise()

    def start_game(self):
        """Start the game by setting up the game page."""
        play_sound_in_thread("sound_effects/start_game2.mp3")
        self.game_page()

    def run(self):
        """Run the application by setting up all pages and showing the lobby page."""
        self.lobby_page()
        self.setting_page()
        self.rules_page()
        self.switch_frames(self.lobby)
