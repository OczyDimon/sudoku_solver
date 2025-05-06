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
                return (i, j)


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


def solve(grid):
    """ Решение пазла, заданного в grid
    """

    empty_position = find_empty_positions(grid)
    if empty_position == None:
        return grid
    possible_values = find_possible_values(grid, empty_position)
    if len(possible_values) == 0:
        return -1

    for value in possible_values:
        grid[empty_position[0]][empty_position[1]] = value
        if solve(grid) == -1:
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
