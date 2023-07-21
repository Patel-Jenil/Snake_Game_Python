# Snake Game using Python and Tkinter module

The base of this game is taken from https://github.com/Python-World/python-mini-projects.git.
As it is open source I tried to add some new features to the Snake_Game project.

Features added:

1. Changed the color of head of snake to easily differentiate Head and Body and direction of snake.
2. Added NewGame and exit buttons which were not present in game before. Because to play new game, we had to restart the game.
3. Binded "Enter" button to start New Game and "Escape" to Exit Game.
4. Removed wall collision. Snake will pass through wall and come out of the opposite wall.
5. Fixed Bug. BEFORE : Food was randomly spawned anywhere even on body of the snake. NOW : Food is programmed to not spawn at any snake's body part in an optimised way.
