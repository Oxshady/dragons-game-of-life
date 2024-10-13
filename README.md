# Conway's Game of Life

<div align="center">
  <a href="https://github.com/Oxshady/dragons-game-of-life/releases/tag/v1.2">
    <img src="https://img.shields.io/badge/Download-Latest%20Release-blue" alt="Download Latest Release">
  </a>
</div>

## Project Overview
**Title**: Conway's Game of Life    
**Competition**: Software Engineering Competition (ALX SE CUP Semi-finals)

## Project Description
This project is an implementation of Conway's Game of Life, a cellular automaton devised by the mathematician John Conway. The application is built using Python and the Tkinter library, providing an interactive interface where users can visualize and interact with the game's mechanics.

## Live demo using ***Tkinter***
[![Watch the video](https://raw.githubusercontent.com/Oxshady/dragons-game-of-life/assets/thumbnail.jpg)](https://github.com/Oxshady/dragons-game-of-life/assets/GameOfLife_tkinter.mp4)


## Features
- **User Interface**: A clean and intuitive UI built with Tkinter, allowing users to navigate easily between the lobby, settings, and game screens.
- **Settings Configuration**: Users can customize the grid size (rows and columns) and select colors for alive and dead cells.
- **Game Controls**: 
  - Start and Stop buttons to control the game's execution.
  - Reset functionality to clear the grid and start anew.
  - Randomize button to populate the grid with random cell states.
- **Interactive Grid**: Clickable grid cells that allow users to toggle between alive and dead states.
- **Dynamic Updates**: The game updates the grid based on the rules of Conway's Game of Life, providing a real-time visualization of cell evolution.

## Technical Stack
- **Programming Language**: Python
- **Framework**: Tkinter
- **Randomization Logic**: Utilizes Python's `random` module for initial grid state generation.

## Challenges Faced
- **Dynamic UI Updates**: Ensured smooth transitions between different UI frames and efficient updates of the game grid.
- **Cell State Management**: Implemented the logic for counting alive neighbors and updating cell states according to the rules of the game.
- **Error Handling**: Addressed issues related to the management of game states and transitions between settings and game pages.

## Learning Outcomes
- Gained experience in developing GUI applications using Tkinter.
- Improved understanding of algorithms related to cellular automata and dynamic state management.
- Enhanced skills in handling user input and managing application flow in Python.
