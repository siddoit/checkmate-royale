# Checkmate Royale - AI Chess Game

![Checkmate Royale Screenshot](ss.png) 


Checkmate Royale is a graphical chess game built entirely in Python using Tkinter for the UI and the powerful Stockfish engine for chess AI. Born from an afternoon idea to watch two AIs battle, it evolved into a project featuring Player vs AI combat with a customizable difficulty system and AI banter.

This project served as a unique step in my learning journey, allowing me to explore GUI development, process interaction, and game state management by integrating several libraries and an external engine.

## Features

*   **Game Modes:**
    *   Play vs AI (Choose White or Black)
    *   AI vs AI Simulation
*   **Stockfish Integration:** Utilizes the Stockfish chess engine for strong chess play.
*   **Customizable AI:**
    *   Adjustable AI Skill Level (0-20).
    *   Configurable AI thinking time per move.
*   **User Interface:**
    *   Clean graphical board built with Tkinter.
    *   Custom "Checkmate Royale V2" theme.
    *   Move Highlights: Legal moves, last move, selected piece, king in check.
    *   Game Log / AI Banter display area.
    *   Settings Screen: Adjust AI, resolution, and fullscreen options.
*   **Game Controls:** Start, Stop, Pause, and Resume game flow (especially useful in AI vs AI mode).
*   **Standalone Build:** Can be built into a Windows executable using PyInstaller (requires manual setup).

## Technology Stack

*   **Language:** Python 3.x
*   **GUI:** Tkinter (Python's built-in GUI library) + `ttk` themed widgets
*   **Chess Logic:** [`python-chess`](https://github.com/niklasf/python-chess) library
*   **Image Handling:** [`Pillow`](https://python-pillow.org/) (PIL Fork)
*   **Chess Engine:** [Stockfish](https://stockfishchess.org/) (External application)
*   **Building:** [PyInstaller](https://pyinstaller.org/en/stable/) (To create `chess.exe`)

## Requirements

Before you begin, ensure you have the following installed/downloaded:

1.  **Python 3.x:** Download from [python.org](https://www.python.org/downloads/).
    *   **IMPORTANT:** During installation on Windows, make sure to check the box "Add Python to PATH".
2.  **Stockfish Chess Engine:** Download the appropriate version for your system from [stockfishchess.org](https://stockfishchess.org/download/). You will need the path to the executable file later.

## Setup & Installation

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/siddoit/checkmateroyale.git 
    cd checkmateroyale
    ```

2.  **Download Stockfish:** 
        If you haven't already, download Stockfish (see Requirements) and place the executable in
        (`C:\ChessEngines\stockfish\stockfish.exe`).

3.  **Install Python Dependencies:**
        Double-click the `install_dependencies.bat` file in the main project directory. It will check for Python/pip and install the packages.

4.  **Ensure Assets:** Make sure the `assets` folder (containing piece images like `wp.png`, `bn.png`, etc., and optionally `logo.png`) is present:
    *   If running from source, it should typically be inside or accessible from the `src` directory, or place it in the root and adjust `ASSETS_FOLDER = "assets"` in `main.py` if needed (the current code expects it in the root).
    *   If running the pre-built `chess.exe`, the `assets` folder must be in the same directory as the `.exe` (the `bin` folder).

## Running the Application

*   **From Source Code:**
    Navigate to the project's root directory in your terminal and run:
    ```bash
    python src/main.py
    ```
*   **Using the Pre-built Executable:**
    1.  Navigate to the directory containing `CheckmateRoyale.exe` (in the `bin` folder).
    2.  Ensure the `assets` folder and `logo.png` are also in this directory.
    3.  Double-click `CheckmateRoyale.exe` to run the game.

## Configuration
*   **In-Game Settings:** Use the "Settings" menu within the application to adjust AI difficulty, think time, resolution, and fullscreen mode.

## Project Structure
Use code with caution.
Markdown
checkmateroyale/
├── src/ # Python source code
│ └── main.py
├── bin/ # Output directory for the packaged executable (optional)
│ ├── CheckmateRoyale.exe # Standalone executable (if built)
│ ├── assets/ # Runtime assets for executable
│ └── logo.png # Runtime logo for executable
├── assets/ # Game assets (pieces, logo) for running from source
│ ├── pieces/ # Piece images (wp.png, bn.png...)
│ └── logo.png
├── build/ # PyInstaller build artifacts (temporary)
├── .gitignore # Git ignore file
├── install_dependencies.bat # Windows script to install Python packages
├── README.md # This file
└── LICENSE # Project license file (e.g., MIT)

*(Note: Depending on your exact setup, you might have the `assets` folder only in the root or only in `bin` if you primarily use the built executable.)*

## Acknowledgements

*   Chess pieces graphics sourced from [Green Chess](https://greenchess.net/info.php?item=downloads)
*   The brilliant [python-chess](https://github.com/niklasf/python-chess) library maintainers.
*   The [Stockfish](https://stockfishchess.org/) team for their incredibly strong chess engine.
*   The developers of [Pillow](https://python-pillow.org/).
=======
# Checkmate Royale - AI Chess Game

![Checkmate Royale Screenshot](ss.png) 


Checkmate Royale is a graphical chess game built entirely in Python using Tkinter for the UI and the powerful Stockfish engine for chess AI. Born from an afternoon idea to watch two AIs battle, it evolved into a project featuring Player vs AI combat with a customizable difficulty system and AI banter.

This project served as a unique step in my learning journey, allowing me to explore GUI development, process interaction, and game state management by integrating several libraries and an external engine.

## Features

*   **Game Modes:**
    *   Play vs AI (Choose White or Black)
    *   AI vs AI Simulation
*   **Stockfish Integration:** Utilizes the Stockfish chess engine for strong chess play.
*   **Customizable AI:**
    *   Adjustable AI Skill Level (0-20).
    *   Configurable AI thinking time per move.
*   **User Interface:**
    *   Clean graphical board built with Tkinter.
    *   Custom "Checkmate Royale V2" theme.
    *   Move Highlights: Legal moves, last move, selected piece, king in check.
    *   Game Log / AI Banter display area.
    *   Settings Screen: Adjust AI, resolution, and fullscreen options.
*   **Game Controls:** Start, Stop, Pause, and Resume game flow (especially useful in AI vs AI mode).
*   **Standalone Build:** Can be built into a Windows executable using PyInstaller (requires manual setup).

## Technology Stack

*   **Language:** Python 3.x
*   **GUI:** Tkinter (Python's built-in GUI library) + `ttk` themed widgets
*   **Chess Logic:** [`python-chess`](https://github.com/niklasf/python-chess) library
*   **Image Handling:** [`Pillow`](https://python-pillow.org/) (PIL Fork)
*   **Chess Engine:** [Stockfish](https://stockfishchess.org/) (External application)
*   **Building:** [PyInstaller](https://pyinstaller.org/en/stable/) (To create `chess.exe`)

## Requirements

Before you begin, ensure you have the following installed/downloaded:

1.  **Python 3.x:** Download from [python.org](https://www.python.org/downloads/).
    *   **IMPORTANT:** During installation on Windows, make sure to check the box "Add Python to PATH".
2.  **Stockfish Chess Engine:** Download the appropriate version for your system from [stockfishchess.org](https://stockfishchess.org/download/). You will need the path to the executable file later.

## Setup & Installation

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/siddoit/checkmate-royale.git 
    cd checkmateroyale
    ```

2.  **Download Stockfish:** 
        If you haven't already, download Stockfish (see Requirements) and place the executable in
        (`C:\ChessEngines\stockfish\stockfish.exe`).

3.  **Install Python Dependencies:**
        Double-click the `install_dependencies.bat` file in the main project directory. It will check for Python/pip and install the packages.

4.  **Ensure Assets:** Make sure the `assets` folder (containing piece images like `wp.png`, `bn.png`, etc., and optionally `logo.png`) is present:
    *   If running from source, it should typically be inside or accessible from the `src` directory, or place it in the root and adjust `ASSETS_FOLDER = "assets"` in `main.py` if needed (the current code expects it in the root).
    *   If running the pre-built `chess.exe`, the `assets` folder must be in the same directory as the `.exe` (the `bin` folder).

## Running the Application

*   **From Source Code:**
    Navigate to the project's root directory in your terminal and run:
    ```bash
    python src/main.py
    ```
*   **Using the Pre-built Executable:**
    1.  Navigate to the directory containing `CheckmateRoyale.exe` (in the `bin` folder).
    2.  Ensure the `assets` folder and `logo.png` are also in this directory.
    3.  Double-click `CheckmateRoyale.exe` to run the game.

## Configuration
*   **In-Game Settings:** Use the "Settings" menu within the application to adjust AI difficulty, think time, resolution, and fullscreen mode.

## Project Structure
Use code with caution.
Markdown
checkmateroyale/
├── src/ # Python source code
│ └── main.py
├── bin/ # Output directory for the packaged executable (optional)
│ ├── CheckmateRoyale.exe # Standalone executable (if built)
│ ├── assets/ # Runtime assets for executable
│ └── logo.png # Runtime logo for executable
├── assets/ # Game assets (pieces, logo) for running from source
│ ├── pieces/ # Piece images (wp.png, bn.png...)
│ └── logo.png
├── build/ # PyInstaller build artifacts (temporary)
├── .gitignore # Git ignore file
├── install_dependencies.bat # Windows script to install Python packages
├── README.md # This file
└── LICENSE # Project license file (e.g., MIT)

*(Note: Depending on your exact setup, you might have the `assets` folder only in the root or only in `bin` if you primarily use the built executable.)*

## Acknowledgements

*   Chess pieces graphics sourced from [Green Chess](https://greenchess.net/info.php?item=downloads)
*   The brilliant [python-chess](https://github.com/niklasf/python-chess) library maintainers.
*   The [Stockfish](https://stockfishchess.org/) team for their incredibly strong chess engine.
*   The developers of [Pillow](https://python-pillow.org/).
>>>>>>> c59e5c415ffe9ef3f28c15480228a2a638f89b60
