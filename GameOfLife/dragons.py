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
        self.current_mode = "dark"  # Default mode
        self.is_music_playing = True
        self.volume = 0.5
        
        self.music_tracks = {
            "Mac DeMarco - Heart to Heart": "./music/Heart To Heart.mp3",
            "Duran Duran - Invisible": "./music/Duran Duran - INVISIBLE.mp3",
            "Arctic Monkeys - Arabella": "./music/Arctic Monkeys - Arabella (Official Audio).mp3",
            "Arctic Monkeys - Do I Wanna Know": "./music/Arctic Monkeys - Do I Wanna Know_ (Official Video).mp3",
            "Arctic Monkeys - R U Mine": "./music/Arctic Monkeys - R U Mine_.mp3",
            "Mac DeMarco - one more love song": "./music/Mac DeMarco  One More Love Song (Official Audio).mp3",
            "Arctic Monkeys - Why'd You Only Call Me When You're High": "./music/Arctic Monkeys - Why'd You Only Call Me When You're High_.mp3",
            "The Smiths - Back To The Old House": "./music/The Smiths - Back To The Old House.mp3",
            "The Smiths - Heaven Knows I'm Miserable Now": "./music/The Smiths - Heaven Knows I'm Miserable Now.mp3",
            "The Smiths - There Is A Light That Never Goes Out": "./music/The Smiths - There Is A Light That Never Goes Out.mp3"
        }
        self.music_file = "./music/Mac DeMarco  One More Love Song (Official Audio).mp3"
        
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

        self.current_music_label = ctk.CTkLabel(music_frame, text="Current Music: Mac DeMarco - one more love song", font=("Arial", 14))
        self.current_music_label.pack(pady=5)

        self.music_selection = ctk.CTkOptionMenu(self.lobby, values=list(self.music_tracks.keys()), command=self.update_music_selection)
        self.music_selection.pack(pady=10)
        self.music_selection.set("Mac DeMarco - one more love song")

        self.mute_button = ctk.CTkButton(self.lobby, text="Mute" if self.is_music_playing else "Unmute", command=self.toggle_music)
        self.mute_button.pack(pady=10, padx=20)

        self.play_music()

    def update_music_selection(self, choice):
        self.music_file = self.music_tracks[choice]
        self.play_music()
        self.current_music_label.configure(text=f"Current Music: {choice}")

    def play_music(self):
        if not self.is_muted and self.is_music_playing:
            try:
                pygame.mixer.music.load(self.music_file)
                pygame.mixer.music.play(-1)  # Loop indefinitely
                pygame.mixer.music.set_volume(self.volume)
            except Exception as e:
                print(f"Error playing music: {e}")


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

        # Add mode selection
        mode_label = ctk.CTkLabel(entry_frame, text="App Mode", font=("Arial", 14))
        mode_label.grid(row=2, column=0, columnspan=2, padx=5, pady=(20, 5))

        self.mode_var = ctk.StringVar(value=self.current_mode.capitalize())
        self.mode_menu = ctk.CTkOptionMenu(
            entry_frame, 
            values=["Dark", "Light"],
            variable=self.mode_var,
            command=self.change_mode
        )
        self.mode_menu.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Music controls
        music_frame = ctk.CTkFrame(self.settings)
        music_frame.pack(pady=10)

        self.music_button = ctk.CTkButton(music_frame, text="Stop Music" if self.is_music_playing else "Start Music", 
                                          command=self.toggle_music)
        self.music_button.pack(side=ctk.LEFT, padx=10)

        self.volume_slider = ctk.CTkSlider(music_frame, from_=0, to=1, number_of_steps=10,
                                           command=self.change_volume)
        self.volume_slider.set(self.volume)
        self.volume_slider.pack(side=ctk.LEFT, padx=10)

        volume_label = ctk.CTkLabel(music_frame, text="Volume")
        volume_label.pack(side=ctk.LEFT, padx=5)

        apply_button = ctk.CTkButton(self.settings, text="Apply", command=self.apply_settings)
        apply_button.pack(pady=10)

        return_button_music = ctk.CTkButton(self.settings, text="Lobby", command=lambda: [self.play_navigation_sound(), self.switch_frames(self.lobby)])
        return_button_music.pack(pady=10)


    def toggle_music(self):
        if self.is_music_playing:
            pygame.mixer.music.pause()
            self.music_button.configure(text="Start Music")
            self.mute_button.configure(text="Unmute")
            self.is_music_playing = False
        else:
            pygame.mixer.music.unpause()
            self.music_button.configure(text="Stop Music")
            self.mute_button.configure(text="Mute")
            self.is_music_playing = True
        self.play_sound_in_thread("sound_effects/click2.wav")

    def change_volume(self, value):
        self.volume = float(value)
        pygame.mixer.music.set_volume(self.volume)

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


    def change_mode(self, new_mode):
        self.current_mode = new_mode.lower()
        ctk.set_appearance_mode(self.current_mode)
        self.play_sound_in_thread("sound_effects/click2.wav")

    def apply_settings(self):
        try:
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())
            self.game_page(rows, cols)
            if not self.current_game:
                self.current_game.toggle_game()  # Stop the game if it's running
            self.change_mode(self.mode_var.get())  # Apply the selected mode
            self.play_music()  # Restart music with new settings
            if not self.is_muted:
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
