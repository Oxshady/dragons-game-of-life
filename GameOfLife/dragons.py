import customtkinter as ctk
import pygame
from gameOfLife import GameOfLife

class Dragons:
    is_muted = False

    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.set_volume(1.0)
        self.root = ctk.CTk()
        self.config_root()
        self.lobby = ctk.CTkFrame(self.root)
        self.settings = ctk.CTkFrame(self.root)
        self.game = ctk.CTkFrame(self.root)
        self.rules = ctk.CTkFrame(self.root)
        self.game_frame = ctk.CTkFrame(self.game)
        self.game_frame.pack(fill="both", expand=True)
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
        self.root.title("The Game of Life")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

    def frames_config(self):
        for frame in (self.lobby, self.settings, self.game, self.rules):
            frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def app_loop(self):
        self.root.mainloop()

    def play_navigation_sound(self):
        self.play_sound_in_thread("sound_effects/navigate.wav")

    def lobby_page(self):
        title = ctk.CTkLabel(self.lobby, text="The Game of Life", font=("Arial", 30, "bold"))
        title.pack(pady=(30, 10))

        button_frame = ctk.CTkFrame(self.lobby)
        button_frame.pack(pady=20)

        start_button = ctk.CTkButton(button_frame, text="Start Game", command=self.start_game)
        start_button.grid(row=0, column=0, padx=10, pady=10)

        setting_button = ctk.CTkButton(button_frame, text="Settings", command=lambda: [self.play_navigation_sound(), self.switch_frames(self.settings)])
        setting_button.grid(row=0, column=1, padx=10, pady=10)

        rules_button = ctk.CTkButton(button_frame, text="Rules", command=lambda: [self.play_navigation_sound(), self.switch_frames(self.rules)])
        rules_button.grid(row=0, column=2, padx=10, pady=10)

        quit_button = ctk.CTkButton(button_frame, text="Quit", command=lambda: [self.play_sound_in_thread("sound_effects/exit3.wav"), self.root.after(200, self.root.quit)])
        quit_button.grid(row=0, column=3, padx=10, pady=10)

        music_frame = ctk.CTkFrame(self.lobby)
        music_frame.pack(pady=10)

        self.current_music_label = ctk.CTkLabel(music_frame, text="Current Music: Ahmed Santa: Emna3-elklam", font=("Arial", 14))
        self.current_music_label.pack(pady=5)

        self.music_selection = ctk.CTkOptionMenu(self.lobby, values=list(self.music_tracks.keys()), command=self.update_music_selection)
        self.music_selection.pack(pady=10)
        self.music_selection.set("Ahmed Santa: Emna3-elklam")

        self.mute_button = ctk.CTkButton(self.lobby, text="Mute", command=self.toggle_mute)
        self.mute_button.pack(pady=10, padx=20, fill="x")

        self.play_music()

    def update_music_selection(self, choice):
        self.music_file = self.music_tracks[choice]
        self.play_music()
        self.current_music_label.configure(text=f"Current Music: {choice}")

    def toggle_mute(self):
        if not self.is_muted:
            pygame.mixer.music.set_volume(0)
            self.mute_button.configure(text="Unmute")
            self.play_sound_in_thread("sound_effects/click2.wav")
        else:
            pygame.mixer.music.set_volume(1)
            self.mute_button.configure(text="Mute")
            self.play_sound_in_thread("sound_effects/click2.wav")
        self.is_muted = not self.is_muted

        if self.is_muted:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def play_music(self):
        if not self.is_muted:
            try:
                pygame.mixer.music.load(self.music_file)
                pygame.mixer.music.play(-1)
            except Exception as e:
                print(f"Error playing music: {e}")

    def stop_music(self):
        pygame.mixer.music.stop()

    def setting_page(self):
        title = ctk.CTkLabel(self.settings, text="Settings", font=("Arial", 30, "bold"))
        title.pack(pady=(30, 10))

        entry_frame = ctk.CTkFrame(self.settings)
        entry_frame.pack(pady=20)

        width_label = ctk.CTkLabel(entry_frame, text="Width", font=("Arial", 14))
        width_label.grid(row=0, column=0, padx=5)

        height_label = ctk.CTkLabel(entry_frame, text="Height", font=("Arial", 14))
        height_label.grid(row=0, column=1, padx=5)

        self.rows_entry = ctk.CTkEntry(entry_frame, width=80, font=("Arial", 14), justify='center')
        self.rows_entry.insert(0, "20")
        self.rows_entry.grid(row=1, column=0, padx=5)

        self.cols_entry = ctk.CTkEntry(entry_frame, width=80, font=("Arial", 14), justify='center')
        self.cols_entry.insert(0, "20")
        self.cols_entry.grid(row=1, column=1, padx=5)

        apply_button = ctk.CTkButton(self.settings, text="Apply", command=self.apply_settings)
        apply_button.pack(pady=10)

        return_button_music = ctk.CTkButton(self.settings, text="Lobby", command=lambda: [self.play_navigation_sound(), self.switch_frames(self.lobby)])
        return_button_music.pack(pady=10)

        stop_button_music = ctk.CTkButton(self.settings, text="Stop Music", command=lambda: [self.play_sound_in_thread("./sound_effects/click2.wav"), self.stop_music()])
        stop_button_music.pack(pady=10)

    def rules_page(self):
        title_frame = ctk.CTkFrame(self.rules)
        title_frame.pack(pady=(30, 10))
        
        title = ctk.CTkLabel(title_frame, text="Game Rules", font=("Arial", 30, "bold"))
        title.pack()

        description_frame = ctk.CTkFrame(self.rules)
        description_frame.pack(pady=(10, 10), padx=20)

        description = (
            "The Game of Life is a cellular automaton devised by the British mathematician John Conway in 1970.\n\n"
            "It consists of a grid of cells that live, die, or multiply based on a set of rules:\n"
        )

        rules_label = ctk.CTkLabel(description_frame, text=description, font=("Arial", 14), wraplength=700, justify='left')
        rules_label.pack(anchor='w')

        rules_list = [
            "※ Any live cell with fewer than two live neighbors dies (underpopulation).",
            "※ Any live cell with two or three live neighbors lives on to the next generation.",
            "※ Any live cell with more than three live neighbors dies (overpopulation).",
            "※ Any dead cell with exactly three live neighbors becomes a live cell (reproduction)."
        ]
        
        for rule in rules_list:
            rule_label = ctk.CTkLabel(description_frame, text=rule, font=("Arial", 14), wraplength=700, justify='left')
            rule_label.pack(anchor='w')

        conclusion_label = ctk.CTkLabel(description_frame, text="These rules determine the fate of each cell in each generation.", font=("Arial", 14), wraplength=700, justify='left')
        conclusion_label.pack(anchor='w', pady=20)

        return_button = ctk.CTkButton(self.rules, text="Lobby", command=lambda: [self.play_navigation_sound(), self.switch_frames(self.lobby)])
        return_button.pack(pady=20)

    def apply_settings(self):
        try:
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())
            self.game_page(rows, cols)
            if self.current_game:
                self.current_game.toggle_game()
            if self.is_muted:
                self.play_sound_in_thread("sound_effects/start_game2.mp3")
        except ValueError:
            pass

    def game_page(self, rows=20, cols=20):
        if self.current_game is None:
            self.current_game = GameOfLife(self.game_frame, self, rows, cols)
        else:
            self.current_game.update_grid(rows, cols)
        self.switch_frames(self.game)

    def switch_frames(self, frame):
        frame.tkraise()

    def start_game(self):
        if self.is_muted:
            self.play_sound_in_thread("sound_effects/start_game2.mp3")
        self.game_page()

    def play_sound_in_thread(self, sound_file):
        sound = pygame.mixer.Sound(sound_file)
        sound.play()

    def run(self):
        self.lobby_page()
        self.setting_page()
        self.rules_page()
        self.switch_frames(self.lobby)

if __name__ == "__main__":
    Dragons()