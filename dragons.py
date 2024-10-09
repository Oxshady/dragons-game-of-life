from tkinter import *

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
        self.game.grid_rowconfigure(0, weight=1)
        self.game.grid_rowconfigure(1, weight=1)
        self.game.grid_rowconfigure(2, weight=1)
        self.game.grid_columnconfigure(0, weight=1)

        title = Label(self.game, text="Game Page", font=("Helvetica", 24, "bold"), bg="white")
        title.grid(row=1, column=0, pady=20, padx=20, sticky="n")

        loby_button = Button(self.game, text="Lobby", font=("Helvetica", 16), command=lambda: self.switch_frames(self.lobby))
        loby_button.grid(row=2, column=0, pady=10, padx=20)

    def switch_frames(self, frame):
        frame.tkraise()

    def run(self):
        self.lobby_page()
        self.setting_page()
        self.game_page()
        self.switch_frames(self.lobby)


x = Dragons()
