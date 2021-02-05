'''
Module for checking a board for
skyscrapers game

Link to GitHub: https://github.com/DariaMinieieva/skyscrapers
'''


def read_input(path: str):
    """
    Read game board file from path.
    Return list of str.

    >>> read_input("check.txt")
    ['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***']
    """
    result = []

    with open(path, "r", encoding="utf-8") as input_file:
        for line in input_file:
            result.append(line.strip())

    return result


def left_to_right_check(input_line: str, pivot: int):
    """
    Check row-wise visibility from left to right.
    Return True if number of building from the left-most hint is visible looking to the right,
    False otherwise.

    input_line - representing board row.
    pivot - number on the left-most hint of the input_line.

    >>> left_to_right_check("412453*", 4)
    True
    >>> left_to_right_check("452453*", 5)
    False
    """
    num = list(map(int, list(input_line.strip("*"))))
    num.pop(0)

    num = num[:pivot]

    if num[-1] == max(num):
        return True

    return False


def check_not_finished_board(board: list):
    """
    Check if skyscraper board is not finished, i.e., '?' present on the game board.

    Return True if finished, False otherwise.

    >>> check_not_finished_board(['***21**', '4?????*', '4?????*', '*?????5',\
         '*?????*', '*?????*', '*2*1***'])
    False
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*543215',\
         '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*5?3215',\
         '*35214*', '*41532*', '*2*1***'])
    False
    """
    for row in board:
        if "?" in row:
            return False

    return True


def check_uniqueness_in_rows(board: list):
    """
    Check buildings of unique height in each row.

    Return True if buildings in a row have unique length, False otherwise.

    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*',\
         '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_uniqueness_in_rows(['***21**', '452453*', '423145*',\
         '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*',\
         '*553215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    board = board[1:-1]
    for row in board:
        row = list(row)

        row.pop(0)
        row.pop(-1)

        row = list(filter(lambda x: x != "*", row))

        if len(row) != len(set(row)):
            return False

    return True


def check_horizontal_visibility(board: list):
    """
    Check row-wise visibility (left-right and vice versa)

    Return True if all horizontal hints are satisfiable,
     i.e., for line 412453* , hint is 4, and 1245 are the four buildings
      that could be observed from the hint looking to the right.

    >>> check_horizontal_visibility(['***21**', '412453*', '423145*',\
         '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_horizontal_visibility(['***21**', '452453*', '423145*',\
         '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_horizontal_visibility(['***21**', '452413*', '423145*',\
         '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    board = board[1:-1]
    results = []

    for row in board:
        row_1 = row[1:-1]
        row_1 = list(filter(lambda x: x != "*", list(row_1)))
        row_1 = list(map(int, row_1))

        if row[0] != "*":
            results.append(check_rows(row_1, int(row[0])))

        if row[-1] != "*":
            row_1.reverse()
            results.append(check_rows(row_1, int(row[-1])))

    if False in results:
        return False

    return True


def check_rows(row_1: list, num: int) -> bool:
    '''
    Check rows visibility
    '''
    first_num = row_1[0]
    temp = [first_num]

    for i in range(1, len(row_1)):
        if row_1[i] > first_num:
            temp.append(row_1[i])
        first_num = max(row_1[i], first_num)

    if len(temp) >= num:
        return True

    return False


def check_columns(board: list):
    """
    Check column-wise compliance of the board for uniqueness
    (buildings of unique height)
    and visibility (top-bottom and vice versa).

    Same as for horizontal cases, but aggregated in
    one function for vertical case, i.e. columns.

    >>> check_columns(['***21**', '412453*', '423145*',\
         '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_columns(['***21**', '412453*', '423145*',\
         '*543215', '*35214*', '*41232*', '*2*1***'])
    False
    >>> check_columns(['***21**', '412553*', '423145*',\
         '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    reversed_board = [[0 for j in range(len(board))] for i in range(len(board))]

    for i in range(len(board)):
        for j in range(len(board)):
            reversed_board[i][j] = board[j][i]

        reversed_board[i] = "".join(reversed_board[i])

    uniqueness = check_uniqueness_in_rows(reversed_board)
    visibility = check_horizontal_visibility(reversed_board)

    return uniqueness and visibility



def check_skyscrapers(input_path: str):
    """
    Main function to check the status of skyscraper game board.
    Return True if the board status is compliant with the rules,
    False otherwise.

    >>> check_skyscrapers("check.txt")
    True
    """
    board = read_input(input_path)

    columns = check_columns(board)
    h_visibility = check_horizontal_visibility(board)
    not_finished = check_not_finished_board(board)
    uniqueness = check_uniqueness_in_rows(board)

    return columns and h_visibility and not_finished and uniqueness


if __name__ == "__main__":
    print(check_skyscrapers("check.txt"))
