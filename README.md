### Here are the steps to run the Python code:

1. Open main.py in some code editor like VS Code.
2. Run it and the chess interface will open.
3. You will be assigned a side (black/white) at random.
4. The Stockfish Chess Engine will respond to each of your move.

The Python code is a Chess game implementation using the Pygame library and Stockfish, an open-source chess engine. Here's a breakdown of the code:

### Libraries Used:

- `pygame`: For creating the game interface and handling user input.
- `chess`: Provides chess logic and board representation in algebraic notation.
- `stockfish`: A strong open-source chess engine used for calculating moves and determining best moves.

### Game Logic:

1. The code initializes a Pygame window and sets up the chessboard using classes (`Board`, `Square`, and various piece classes like `Rook`, `Bishop`, `Knight`, `King`, `Queen`, and `Pawn`).
2. The `Board` class handles the game logic, including generating squares, setting up pieces on the board, handling player clicks, checking for check/checkmate, and drawing the board.
3. Pieces have their movement logic implemented within their respective classes (`get_possible_moves`, `move`, `get_valid_moves`, etc.).
4. The game alternates turns between the user and Stockfish AI (which has been set up to play moves for the opposite color).

### Game Flow:

- The `while` loop manages the game's flow by continuously updating the display and handling events (such as user mouse clicks) to make moves.
- When it's the player's turn (`board1.turn == my_col`), the player can make moves by clicking on pieces and valid destinations.
- If it's Stockfish's turn, it retrieves the best move using the Stockfish engine and performs that move on the board.

### Win Conditions:

- The code checks for checkmate for both white and black players in each iteration of the loop. If checkmate is detected for either side, the game ends, and a message indicating the winning player is printed.

### User Interaction:

- The player interacts with the game by clicking on pieces to select them and clicking on valid destination squares to move the selected piece.

This implementation combines Pygame for the graphical interface, the chess library for managing the game state, and Stockfish for providing AI moves and determining check/checkmate conditions.
