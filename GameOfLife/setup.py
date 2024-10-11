import os
from cx_Freeze import setup, Executable

# Determine the operating system (posix) or (nt)
is_windows = os.name == 'nt' # Check if it windows assign true else false

# Define the build options, this will include any necessary packages that may not be detected automatically.
build_exe_options = {
    "packages": ["tkinter", "random"],  # Add all the modules/packages your app requires
    "includes": ["dragons", "gameOfLife"],
    "include_files": [
        ("sound_effects", "sound_effects"),  # Include the sound_effects folder
        ("music", "music"),  # Include the music folder
        "Gipsy Kings - Volare (Nel blu dipinto di blu)(MP3_70K).mp3"
    ]
}

# Set target name based on the operating system
target_name = "TheGameOfLife.exe" if is_windows else "TheGameOfLife"

# Define the setup
setup(
    name="The Game of Life",
    version="1.0",
    description="Game of Life Application",
    options={"build_exe": build_exe_options},
    executables=[Executable("app.py", target_name=target_name)],
)
