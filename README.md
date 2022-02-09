# chess
**A python chess library with legal move generation, custom chess variant support, move making and unmaking, PGN/FEN loading/generating, and many other features**
## Requirements
Python 2.7 or Python 3
## Installation
The library can be installed directly from github using pip: `pip install git+https://github.com/DanielMiao1/chess`.
## Basic Features
**See the features section of the wiki for a list of features**

### Creating a new game
```py
>>> game = chess.Game()
```
To load a custom FEN, use the fen argument:
```py
>>> game = chess.Game(fen="fen text")
```
Or, use the `loadFEN` function to load a FEN after the game is initialized:
```py
>>> game.loadFEN("fen text")
```
### Printing the board
To generate a unicode representation of the board, use the `Game.visualized()` function.
### Making a move
To make a move, use the `Game.move()` function:
```py
>>> game.move("e4")
e4
### Takeback
To take back a move, use the `Game.takeback()` function:
```py
>>> game.takeback()
```
