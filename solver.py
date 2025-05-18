import cv2
import numpy as np
from datetime import datetime as dt


def group(values, n):
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    """
    return [values[i:i+n] for i in range(0, len(values), n)]


def get_row(values, pos):
    """ Возвращает все значения для номера строки, указанной в pos
    """
    return values[pos[0]]


def get_col(values, pos):
    """ Возвращает все значения для номера столбца, указанного в pos
    """
    answer = []
    for i in range(len(values)):
        answer.append(values[i][pos[1]])
    return answer


def get_block(values, pos):
    """ Возвращает все значения из квадрата, в который попадает позиция pos
    """
    i0 = (pos[0] // 3) * 3
    i1 = i0 + 3
    j0 = (pos[1] // 3) * 3
    j1 = j0 + 3
    ans = []
    for i in range(i0, i1):
        ans += values[i][j0:j1]
    return ans


def find_empty_positions(grid):
    """ Найти первую свободную позицию в пазле
    """
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == ".":
                return i, j


def find_possible_values(grid, pos):
    """ Вернуть все возможные значения для указанной позиции
    """
    row = get_row(grid, pos)
    column = get_col(grid, pos)
    block = get_block(grid, pos)
    used = set(row + column + block)
    result = {str(i) for i in range(1, 10)}
    result = result - used
    return result


def empty_grid():
    gray = (17, 32, 50)
    yellow = (230, 249, 255)

    img = (np.ones((271, 271, 3)) * yellow).astype(np.uint8)

    # img = cv2.rectangle(img, (0, 0), (200, 200), (255, 0, 0), 2)

    for i in range(10):
        img = cv2.line(img, (30 * i, 0), (30 * i, 270), gray, 2)
        img = cv2.line(img, (0, 30 * i), (270, 30 * i), gray, 2)

    return img


def solved_to_image(grid):
    img = empty_grid()

    print('solved_to image:\n', grid)

    if (grid == 1) or (grid == -1):
        return '0.png'

    # grid = [['5', '3', '4', '6', '7', '8', '9', '1', '2'],
    #         ['6', '7', '2', '1', '9', '5', '3', '4', '8'],
    #         ['1', '9', '8', '3', '4', '2', '5', '6', '7'],
    #         ['8', '5', '9', '7', '6', '1', '4', '2', '3'],
    #         ['4', '2', '6', '8', '5', '3', '7', '9', '1'],
    #         ['7', '1', '3', '9', '2', '4', '8', '5', '6'],
    #         ['9', '6', '1', '5', '3', '7', '2', '8', '4'],
    #         ['2', '8', '7', '4', '1', '9', '6', '3', '5'],
    #         ['3', '4', '5', '2', '8', '6', '1', '7', '9']]

    for i in range(9):
        for j in range(9):
            cords = (4 + 30 * i, 26 + 30 * j)
            img = cv2.putText(img, grid[j][i], cords, cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)

    now = dt.now().strftime('%Y-%m-%d_%H-%M-%S')

    filename = f'temp/solved_{now}.png'

    cv2.imwrite(f'static/{filename}', img)

    return filename


def solve_sudoku(grid):
    """ Решение пазла, заданного в grid """

    empty_position = find_empty_positions(grid)
    if empty_position is None:
        return grid
    possible_values = find_possible_values(grid, empty_position)
    if len(possible_values) == 0:
        return -1

    for value in possible_values:
        grid[empty_position[0]][empty_position[1]] = value
        if solve_sudoku(grid) == -1:
            continue
        else:
            return grid

    grid[empty_position[0]][empty_position[1]] = "."
    return -1


def check_solution(solution):
    """
    Если решение solution верно, то вернуть True, в противном случае False
    """
    for i in range(9):
        if set(get_row(solution, (i, 0))) != set('123456789'):
            return False
        if set(get_col(solution, (0, i))) != set('123456789'):
            return False
        if set(get_block(solution, (i, 0))) != set('123456789'):
            return False
    else:
        return True
