"""
Raw implementation of a minesweeper
game without the use of interfaces or coroutines.
"""
import os
import random

from collections import deque
from typing import List, Union
from queue import Queue

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
        user_grid[y][x] = 1
        return user_grid
    else:
        for nx, ny in _reveal_nones(grid, x, y):
            user_grid[ny][nx] = 1
    return user_grid


def _reveal_nones(grid, x, y):
    """
    Return a list of all the cells that should be revealed.
    """
    reveal = []
    que = deque([(x, y)])
    seen = []
    while que:
        xi, yi = que.popleft()
        surrounding_cells = [(xi, yi-1),
                             (xi, yi+1),
                             (xi-1, yi+1),
                             (xi-1, yi),
                             (xi-1, yi-1),
                             (xi+1, yi+1),
                             (xi+1, yi),
                             (xi+1, yi-1)]
        for dxi, dyi in surrounding_cells:
            if dxi < 0 or dyi < 0:
                continue
            if (dxi, dyi) in seen:
                continue
            try:
                if grid[dyi][dxi] is None:
                    reveal.append((dxi, dyi))
                    que.append((dxi, dyi))
                elif grid[dyi][dxi] > 0:
                    reveal.append((dxi, dyi))
                else:
                    return "Something is amiss"
                seen.append((dxi, dyi))
            except IndexError:
                continue

    return reveal


def show_user_grid(grid: List[List[Union[None, int]]],
                   user_grid: List[List[Union[None, int]]]) -> List[List[Union[None, int]]]:
    """
    Display to the user the board game by iterating
    across the grid and user grid.
    """
    show_grid = [[0] * len(grid[0]) for _ in range(len(grid))]
    for yi, y in enumerate(grid):
        for xi, x in enumerate(y):
            if user_grid[yi][xi]:
                show_grid[yi][xi] = grid[yi][xi]
            else:
                show_grid[yi][xi] = 0
    return show_grid


def ascii_grid(show_grid: List[List[Union[None, int]]]) -> List[List[Union[None, int]]]:
    """
    Show an ascii grid of the grid produced by the show_user_grid function.
    """
    height = len(show_grid)
    width = len(show_grid[0])
    ascii_version = '  '
    for i in range(width):
        stringy_i = str(i)
        if len(stringy_i) > 1:
            ascii_version += f' {stringy_i[-1]}'
        else:
            ascii_version += f' {stringy_i}'
    place = 0
    top_string = ''
    for char in ascii_version:
        if char == '0':
            top_string += str(place)
            place += 1
        else:
            top_string += ' '
    top_string += '\n'
    ascii_version = top_string + '\033[4m' + ascii_version + '\033[0m'
    # top_string += ascii_version
    # ascii_version = top_string
    for iy, row in enumerate(show_grid):
        if len(str(iy)) == 1:
            ascii_version += f'\n{iy} |'
        else:
            ascii_version += f'\n{iy}|'
        for ix, element in enumerate(row):
            if element is None:
                ascii_version += '  '
            elif element > 0:
                try:
                    if show_grid[iy+1][ix] == 0 or show_grid[iy+1][ix] is not None:
                        ascii_version += '\033[4m'
                except IndexError:
                    pass
                ascii_version += str(element)
                ascii_version += '\033[0m'
                try:
                    if show_grid[iy][ix+1] is not None:
                        ascii_version += '|'
                    else:
                        ascii_version += ' '
                except IndexError:
                    pass
            else:
                ascii_version += '_|'
    print(ascii_version)


def welcome_message():
    """
    Prints a welcome message to the user and retrieves their valid inputs.
    """
    welcome = """
Welcome to Terminal Minesweeper!

First, please select the height, width, and the number of mines
you'd like to play with. Below, you can find some general guidelines
on how these parameters affect difficulty. If you don't put in a number,
the game will default to intermediate."""

    difficulties = """
Game Difficulties
------------
- Beginner:     8x8 | 9x9 | 10x10, 10 mines
- Intermediate: 13x15 - 16x16,     40 mines
- Expert:       16x30(30x16),      99 mines
"""

    print(welcome)
    print(difficulties)
    height = input('Height: ')
    while not (height.isdigit() or height == ''):
        height = input('Please enter a valid number: ')
    width = input('Width: ')
    while not (width.isdigit() or width == ''):
        width = input('Please enter a valid number: ')
    mines = input('Number of mines: ')
    while not (mines.isdigit() or mines == ''):
        mines = input('Please enter a valid number: ')
    height = 13 if height == '' else int(height)
    width = 15 if width == '' else int(width)
    mines = 40 if mines == '' else int(mines)

    return height, width, mines


def main():
    """
    Main game loop.
    """
    y, x, mines = welcome_message()
    # import pdb; pdb.set_trace()
    secret_grid = initialize_grid(x, y, mines)
    secret_grid = add_mine_counts(secret_grid)
    user_grid = [[0] * len(secret_grid[0]) for _ in range(len(secret_grid))]
    while user_grid and sum(row.count(0) for row in user_grid) > mines:
        shown_grid = show_user_grid(secret_grid, user_grid)
        ascii_grid(shown_grid)
        print('Select space to reveal (row, column) (e.g. 3, 6)')
        sel_y, sel_x = input('Select: ').split(', ')
        try:
            user_grid = select_cell(secret_grid, user_grid, int(sel_x), int(sel_y))
        except TypeError:
            while not sel_y.isdigit() or not sel_x.isdigit(): # Need more checking of user input, else error
                sel_y, sel_x = input('Please put in valid numbers: ')
            user_grid = select_cell(secret_grid, user_grid, int(sel_x), int(sel_y))

    return user_grid


if __name__ == '__main__':
    playing = True
    while playing:
        grid = main()
        if not grid:
            print('You struck a mine and died.')
        else:
            print('You won! Great job!!')
        play_again = input('Play again? (Y/n): ')
        while play_again not in {'Y', 'y', 'n', 'N'}:
            play_again = input('Play again? (Y/n): ')
        if play_again.lower() == 'n':
            playing = False
    print('Goodbye!')


    # grid = initialize_grid()
    # grid = add_mine_counts(grid)
    # user_grid = [[0] * len(grid[0]) for _ in range(len(grid))]
    # user_grid = select_cell(grid, user_grid, 1, 3)
    # if user_grid:
    #     shown_grid = show_user_grid(grid, user_grid)
    #     ascii_grid(grid)
    #     ascii_grid(shown_grid)
    # else:
    #     print("you hit a mine and died")
