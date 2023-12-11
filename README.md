# MIC-MiniProject Othello Game
This document provides an overview of the Othello game and its functionalities.

Installation:

There are two ways to install the Othello game:

Docker-based deployment:

Install Docker on your machine.
Fetch the code.
Run docker-compose up -d to start the containers.
Access the server at localhost:8888.
Note that the database is stored in the db subdirectory.
This deployment uses the dc configuration.x
Basic deployment:

Install NodeJS (LTS recommended).
Install MongoDB.
Fetch the repository.
Run npm i to install dependencies.
Run node ./app.js to start the game.
By default, the game is accessible on port 8888 of your localhost.
Development:

To modify or add components to the game, you will need the following software:

NodeJS (LTS recommended)
WebGME-CLI (latest recommended)
Use NodeJS for managing components and dependencies. Use the CLI to generate or import design studio components and handle configuration updates.

Components:

Seed: Represents the Othello game.
Command to create seed: webgme new seed -n Othello -f ./meta_model_miniproject.webgmex OthelloGame

Plugins:
Command to create Plugins: webgme new plugin --language Python othelloPlugin

Highlight Valid Tiles: This functionality identifies and highlights valid tiles for the next move based on the current game state. It considers the rules of Othello, allowing placement only on tiles that would trigger color flips.

Count Pieces: This functionality counts the number of pieces on the board for each player at any given state. This information is displayed to inform players of the current game score.

Flipping: This functionality simulates the game mechanics after a player places a piece. It analyzes the last placed piece and performs the necessary color flips for any captured disks, updating the game state accordingly.

Undo: This functionality allows players to undo their last move, reverting the game state to the previous stage. This functionality provides greater flexibility and allows for strategic backtracking.

Auto: This AI functionality plays the game against the user, making valid moves based on the current game state. It aims to make optimal moves, maximizing its chances of winning. This functionality provides a challenging opponent for players.


CreateGame: (Python) Creates a game in the proper folder with the start state.
CheckWinCondition: (JavaScript) Checks if one player has won.
BuildDescriptor: (JavaScript) Creates a structured data representing the model for the visualization.

Gameplay:
Othello is played on an 8x8 board with two players, Black and White.
Players take turns placing discs of their color on the board.
A disc can be placed on an empty square if it "flips" any of the opponent's discs in a straight line.
The player with the most discs at the end of the game wins.
Features:

Single-player and two-player modes.
AI opponent.
Undo/redo moves.
Game statistics.
Known issues:

The AI opponent may not always make the best moves.
The game may not always accurately determine the winner in some complex situations.