# Othello Game

This README provides an overview of the Othello game and its functionalities.

## Installation

### Docker-based deployment:

1. Install Docker on your machine.
2. Fetch the code.
3. Run `docker-compose up -d` to start the containers.
4. Access the server at `localhost:8888`.

### Basic deployment:

1. Install NodeJS (LTS recommended).
2. Install MongoDB.
3. Fetch the repository.
4. Run `npm i` to install dependencies.
5. Run `node ./app.js` to start the game.
6. By default, the game is accessible on port `8888` of your localhost.

## Development

To modify or add components to the game, you will need the following software:

- NodeJS (LTS recommended)
- WebGME-CLI (latest recommended)

Use NodeJS for managing components and dependencies. Use the CLI to generate or import design studio components and handle configuration updates.

## Components

### Seed

Represents the Othello game.

Command to create seed: `webgme new seed -n Othello -f ./meta_model_miniproject.webgmex OthelloGame`

### Plugins

Command to create Plugins: `webgme new plugin --language Python othelloPlugin`

1. **Highlight Valid Tiles:**
   - Identifies and highlights valid tiles for the next move based on the current game state.
   - Follows Othello rules, allowing placement only on tiles that would trigger color flips.

2. **Count Pieces:**
   - Counts the number of pieces on the board for each player at any given state.
   - Displays information about the current game score.

3. **Flipping:**
   - Simulates the game mechanics after a player places a piece.
   - Analyzes the last placed piece and performs necessary color flips for any captured disks, updating the game state accordingly.

4. **Undo:**
   - Allows players to undo their last move, reverting the game state to the previous stage.
   - Provides flexibility and allows for strategic backtracking.

5. **Auto:**
   - AI functionality that plays the game against the user.
   - Makes valid moves based on the current game state, aiming to maximize its chances of winning.
   - Provides a challenging opponent for players.

## Gameplay

- Othello is played on an 8x8 board with two players, Black and White.
- Players take turns placing discs of their color on the board.
- A disc can be placed on an empty square if it "flips" any of the opponent's discs in a straight line.
- The player with the most discs at the end of the game wins.

## Features

- Single-player and two-player modes.
- AI opponent.
- Undo/redo moves.
- Game statistics.

## Known Issues

- The AI opponent may not always make the best moves.
- The game may not always accurately determine the winner in some complex situations.

