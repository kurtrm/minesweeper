"""
Raw implementation of a minesweeper
game without the use of interfaces or coroutines.
"""
import random

from typing import List, Union

# initialize gameboard with mines, randomly (both are input with restrictions)
# count number of mines each cell is touching
# main game loop accepts user input
# logic determines which cells can be revealed to the user
# logic determines if user selected a mine
# (flags, no flags?)
# logic determines if all cells have been revealed that aren't mines


def initialize_grid(height: int=13, width: int=15, mines: int=40) -> List[List[Union[None, int]]]:
    """
    https://dash.harvard.edu/bitstream/handle/1/14398552/BECERRA-SENIORTHESIS-2015.pdf?sequence=1

    Game Difficulties
    ------------
    - Beginner:     8x8 | 9x9 | 10x10, 10 mines
    - Intermediate: 13x15 - 16x16,     40 mines
    - Expert:       16x30(30x16),      99 mines

    Parameters
    ----------
    height(int) -> default: 13
    width(int)  -> default: 15
    mines(int)  -> default: 40

    Default arguments correspond to an intermediate level.

    Returns
    -------
    A matrix consisting of a list of lists containing None or an integer

    For the time being, placing a min/max of height/width at 8/30, respectively.
    Number of mines can't exceed 20% of the total number of spots in the grid.
    Again, this is arbitrary and can be modified at a later date.
    """
    if _valid_parameters(height, width, mines):
        grid = [[None] * width for _ in range(height)]
        for _ in range(mines):
            x = random.randint(0, width)
            y = random.randint(0, height)
            while grid[y][x] is not None:
                x = random.randint(0, width)
                y = random.randint(0, height)
            grid[y][x] = 0

    return grid


def _valid_parameters(height, width, mines) -> bool:
    """
    Validate the inputs into the initialize_grid function.
    """
    if height < 8 or width < 8:
        raise ValueError('Height/width must be greater than or equal to 8.')
    elif height > 30 or width > 30:
        raise ValueError('Height/width must be less or equal to 30.')
    elif mines / (height * width) > .20:
        raise ValueError('Too many mines; total number of mines shall not exceed 20\% of available spaces.')
    return True
