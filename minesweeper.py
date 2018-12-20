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


def initialize_grid(height: int=13,
                    width: int=15,
                    mines: int=40) -> List[List[Union[None, int]]]:
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
    The grid has not been initialized with the mine counts, only None and
    mines represented as zeros.

    For the time being, placing a min/max of height/width at 8/30, respectively.
    Number of mines can't exceed 25% of the total number of spots in the grid.
    Again, this is arbitrary and can be modified at a later date.
    """
    if _valid_parameters(height, width, mines):
        grid = [[None] * width for _ in range(height)]
        for _ in range(mines):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            while grid[y][x] is not None:
                x = random.randint(0, width - 1)
                y = random.randint(0, height - 1)
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
    elif mines / (height * width) > .25:
        raise ValueError('Too many mines; total number of '
                         'mines shall not exceed 20% of available spaces.')
    elif mines <= 0:
        raise ValueError('mines argument must be greater than 0')
    return True


def add_mine_counts(grid: List[List[Union[None, int]]]) -> List[List[Union[None, int]]]:
    """
    This function counts how many mines are around a given cell
    and sets that grid cell equal to that value.

    Paramaters
    ----------
    grid -> list of lists of None and integers(0)

    Returns
    -------
    grid -> list of lists of None and integers(0 - 8)
    """
    for iy, y in enumerate(grid):
        for ix, x in enumerate(y):
            if x is None:
                grid[iy][ix] = _count_mines(grid, ix, iy)
    return grid


def _count_mines(grid, x, y):
    """
    Helper function to count mines around a given cell.
    """
    surrounding_cells = [(x, y-1),
                         (x, y+1),
                         (x-1, y+1),
                         (x-1, y),
                         (x-1, y-1),
                         (x+1, y+1),
                         (x+1, y),
                         (x+1, y-1)]

    count = 0
    for dx, dy in surrounding_cells:
        if dx < 0 or dy < 0:
            continue
        try:
            count += 1 if grid[dy][dx] == 0 else 0
        except IndexError:
            continue

    return count if count > 0 else None


def select_cell(grid: List[List[Union[None, int]]],
                user_grid: List[List[Union[None, int]]],
                x: int,
                y: int) -> List[List[Union[None, int]]]:
    """
    Determine action on the user_grid based on
    the selected cell in the generated grid.

    Parameters
    ----------
    grid: underlying matrix containing all mine locations.
    user_grid: grid that the user sees, where cells have been selected.
    x, y: column and row of selected cell

    Returns
    -------
    user_grid: Altered version of user_grid based on action of
    selected cell or False if a mine was tripped.
    """
    user_cell = user_grid[y][x]
    grid_cell = grid[y][x]
    if user_cell == 1:
        return user_grid
    if grid_cell == 0:
        return False
    if grid_cell is not None:
        user_cell[y][x] = grid_cell[y][x]
        return user_cell
    else:
        pass

