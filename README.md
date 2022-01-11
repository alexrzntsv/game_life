# Game "Life"
## A game created by me to pass the exam in Tinkoff
The rules of the game:
  1. "Life" is played out on an infinite cellular field.
  2. Each cell has 8 neighboring cells.
  3. A creature can live in every cell.
  4. A creature with two or three neighbors survives in the next generation, otherwise it dies from loneliness or overpopulation.
  5. In an empty cage with three neighbors, a creature is born in the next generation.

To visualize the game, I used the "pygame" module. When the program starts, a user can see a window containing a checkered field of the game. In order to start the game, the user needs to fill in the field with creatures of the first generation ( manually: by clicking on the cells, or automatically: using the button). The buttons also made with module "pygame" allow users to perform the following ations:
1. "Start" - starts the game (generations are changed automatically with the speed set in program)
2. "Stop" - stops the game (the generation changing)
3. "New game" - clears the field.
4. "Fill randomly" - fills the playing field with creatures in random order.  
