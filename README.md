# Conway's Game of Life
<div align="center">
  <a href="https://github.com/Oxshady/dragons-game-of-life/releases/tag/v1.4.1">
    <img src="https://img.shields.io/badge/Download-Latest%20Release-blue" alt="Download Latest Release">
  </a>
</div>


## Project Overview
**Title**: Conway's Game of Life    
**Competition**: Software Engineering Competition (***ALX SE CUP Semi-finals***🚀🏆)

## Table of Contents
- [Project Overview](#project-overview)
- [Project Description](#project-description)
- [Live Demos](#live-demo-using-customtkinter)
- [Transition from Tkinter to CustomTkinter](#transition-from-tkinter-to-customtkinter)
- [Features](#features)
- [Technical Stack](#technical-stack)
- [Challenges Faced](#challenges-faced)
- [Learning Outcomes](#learning-outcomes)
- [Installation (Running Locally)](#installation-running-locally)
- [Authors](#authors)

## Project Description
This project is an implementation of Conway's Game of Life, a cellular automaton devised by the mathematician John Conway. The application is built using Python and the Tkinter library, providing an interactive interface where users can visualize and interact with the game's mechanics.

## Live demo using ***CustomTkinter***
https://github.com/user-attachments/assets/718ba3eb-1142-4a39-822e-0004f0a18ce4

## Live demo using ***Tkinter***
https://github.com/user-attachments/assets/ba47420e-93e8-4cc9-aeb5-9bbcb99249cf

## Transition from Tkinter to CustomTkinter
Initially we developed the game of life using Tkinter, then the project was upgraded to CustomTkinter, offering a more modern and customizable interface, along with enhanced features such as improved game controls, dynamic UI elements, and better performance.

## Features
- **User Interface**: A clean and intuitive UI built with CustomTkinter, allowing users to navigate easily between the lobby, settings, and game screens.
- **Settings Configuration**: Users can customize the grid size (rows and columns) and select colors for alive and dead cells.
- **Save/Load Patterns**: Users can save grid states as patterns and load them later to continue their gameplay.

- **Game Controls**: 
  - Start and Stop buttons to control the game's execution.
  - Reset functionality to clear the grid and start anew.
  - Randomize button to populate the grid with random cell states.
  - Custom Themes: Users can apply different color themes and adjust the appearance of the grid and controls.

- **Interactive Grid**: Clickable grid cells that allow users to toggle between alive and dead states and also draw pattern on grid.
- **Dynamic Updates**: The game updates the grid based on the rules of Conway's Game of Life, providing a real-time visualization of cell evolution.

## Technical Stack
- **Programming Language**: Python
- **Framework**: Tkinter and Customtkinter
- **Randomization Logic**: Utilizes Python's `random` module for initial grid state generation.

## Challenges Faced
- **Dynamic UI Updates**: Ensured smooth transitions between different UI frames and efficient updates of the game grid.
- **Cell State Management**: Implemented the logic for counting alive neighbors and updating cell states according to the rules of the game.
- **Error Handling**: Addressed issues related to the management of game states and transitions between settings and game pages.

## Learning Outcomes
- Gained experience in developing GUI applications using Tkinter.
- Improved understanding of algorithms related to cellular automata and dynamic state management.
- Enhanced skills in handling user input and managing application flow in Python.

## Installation (Running Locally)
If you want to run the application locally on your terminal, follow these steps:
1. **Clone the Repository**

   ```bash
   git clone https://github.com/Oxshady/dragons-game-of-life.git
  
   cd dragons-game-of-life
   ```

2. **Create a Virtual Environment**
   Navigate to your project directory and create a virtual environment:

   ```bash
   python3 -m venv venv
   ```
3. **Activate the Virtual Environment**
   To activate the virtual environment:
   ```bash
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. **Install the backend dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
    ```bash
    cd GameOfLife

    python3 app.py
    ```

## Authors

- **Karem Hany** - Backend Developer - [GitHub Profile](https://github.com/K-a-r-e-e-m)
- **Shadi Mahmoud** - Backend Developer - [GitHub Profile](https://github.com/Oxshady)
- **Youssef Ahmed** - Backend Developer - [GitHub Profile](https://github.com/youssef3092004)
- **Ahmed Harhash** - backend Developer - [GitHub Profile](https://github.com/ah0048)
- **Sayed Abdelaal** - Frontend Developer - [GitHub Profile](https://github.com/sayedabdelal)
