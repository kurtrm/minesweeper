"""
Coroutine versions of various functions in minesweeper.py.
"""
from coro_decorator import coroutine_primer


# def _valid_parameters(height, width, mines) -> bool:
#     """
#     Validate the inputs into the initialize_grid function.
#     """
#     if height < 8 or width < 8:
#         print('Height/width must be greater than or equal to 8.')
#         return False
#     elif height > 30 or width > 30:
#         print('Height/width must be less or equal to 30.')
#         return False
#     elif mines / (height * width) > .25:
#         print('Too many mines; total number of '
#               'mines shall not exceed 20% of available spaces.')
#         return False
#     elif mines <= 0:
#         print('mines argument must be greater than 0')
#         return False
#     return True


# def get_input():
#     """
#     Encapsulates logic for taking user input for height, width, and
#     the number of mines.
#     """
#     height = input('Height: ')
#     while not (height.isdigit() or height == ''):
#         height = input('Please enter a valid number: ')
#     height = 13 if height == '' else int(height)

#     width = input('Width: ')
#     while not (width.isdigit() or width == ''):
#         width = input('Please enter a valid number: ')
#     width = 15 if width == '' else int(width)

#     mines = input('Number of mines: ')
#     while not (mines.isdigit() or mines == ''):
#         mines = input('Please enter a valid number: ')
#     mines = 40 if mines == '' else int(mines)


#     return height, width, mines


@coroutine_primer
def _valid_parameters():
    """
    """
    while True:
        height = yield
        while not (height.isdigit() or height == ''):
            print('Height must be an integer,'
                  ' or you may leave blank for default intermediate value.')
            height = yield False
        height = 13 if height == '' else int(height)

        if not 10 <= height <= 40:
            print('Height must be greater than or equal to 10 '
                  'and less than or equal to 40.')
        else:
            break

    while True:
        width = yield
        while not (width.isdigit() or width == ''):
            print('Width must be an integer,'
                  ' or you may leave blank for default intermediate value.')
            width = yield False
        width = 15 if width == '' else int(width)

        if not 10 <= width <= 40:
            print('Width must be greater than or equal to 10 '
                  'and less than or equal to 40.')
        else:
            break

    while True:
        mines = yield
        while not (mines.isdigit() or mines == ''):
            print('Mines must be an integer,'
                  ' or you may leave blank for default intermediate value.')
            mines = yield False
        mines = 40 if mines == '' else int(mines)

        if mines >= height * width:
            print('Number of mines must be less than the number of available spaces.')
        else:
            break
    yield height, width, mines
