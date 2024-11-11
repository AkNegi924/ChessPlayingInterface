# Chess Playing Interface

A complete chess interface built in Python using the Pygame library. This interface supports three game modes: Player vs Player, Player vs Stockfish, and Player vs Custom Chess Engines. The project includes custom chess engines with distinct evaluation strategies, providing a versatile and competitive chess experience.

## Features

- **Graphical User Interface (GUI):** A user-friendly interface built with Pygame, displaying an interactive chessboard for seamless gameplay.
- **Game Modes:**
  - **Player vs Player (PvP):** Traditional chess between two human players.
  - **Player vs Stockfish:** Challenge yourself against the Stockfish chess engine for a competitive experience.
  - **Player vs Custom Engine:** Play against one of five custom chess engines, each with unique evaluation strategies.
- **Custom Chess Engines:** 
  - Created 5 engines with distinct evaluation metrics, including **mobility**, **king safety**, **material balance**, **pawn structure**, and **piece-square tables (PST)**.
  - Engines were compared in a round-robin tournament, with the mobility-based engine achieving a 37.5% win rate, though with a longer evaluation time.

## Requirements

- **Python** 3.12
- **Pygame**: `pip install pygame`
- **Stockfish** chess engine installed and configured

## Setup and Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/AkNegi924/Chess-Playing-Interface.git
   cd Chess-Playing-Interface
   ```
2. Install the required libraries:
   ```bash
   pip install pygame
   ```

3. Configure Stockfish:
   - Download and install the Stockfish chess engine.
   - Ensure the Stockfish executable path is set correctly in the code.

## How to Run

1. Open `main.py` in a code editor, such as VS Code.
2. Run `main.py` to launch the initial window.
3. Select one of the three game modes:
   - **Player vs Player**
   - **Player vs Stockfish**
   - **Player vs Custom Engine**
4. After selecting a mode, begin playing!

## Screenshots

### Game Modes Selection
![initialWindow](https://github.com/user-attachments/assets/101be7fd-b353-4d1d-90b6-3369c097a230)

### Chessboard Interface
![chess](https://github.com/user-attachments/assets/e616daa9-5cf6-4f22-858d-08b0df0b53c8)

### Performance Comparison
Round-robin tournament results of the custom chess engines.
![graph](https://github.com/user-attachments/assets/e1fafffc-3588-4460-aec6-be9546f7f0bc)

## Custom Engines Tournament Results

The custom engines were evaluated based on their unique strategies in a round-robin format. The **mobility-based engine** showed the highest win rate (37.5%) but required more computational time compared to other engines.

## Future Work

- Optimization of engine performance, especially for the mobility-based engine.
- Addition of more evaluation functions and combinations for enhanced gameplay.
- Improved user interface for move suggestions and analysis tools.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

--- 


