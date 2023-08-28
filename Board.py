from PycharmProjects.Examenpracticum1010.skelet import Position
from PycharmProjects.Examenpracticum1010.skelet import Block


def make_board(dimension=10, positions_to_fill=frozenset()):
    """
        Return a new board of the given dimension for which all cells at the
        given positions are already filled.
        ASSUMPTIONS
        - The given dimension is a positive integer number.
        - The filled positions is a collection of proper positions. Positions
          outside the boundaries of the new board have no impact on the content
          of the new board.
    """
    board = []
    for row in range(dimension):
        board.append([])
        for col in range(dimension):
            board[row].append(None)

    for position in positions_to_fill:
        for row in range(1, dimension+1):
            for col in range(1, dimension+1):
                if row == position[0] and col == position[1]:
                    board[row-1][col-1] = position

    return board


def copy_board(board):
    """
        Return a copy of the given board.
        ASSUMPTIONS
        - The given board is a proper board.
    """
    copy = []
    for elem in board:
        copy.append(list(elem))
    return copy


def is_proper_board(board):
    """
        Check wether the given board is a proper board.
        - The board must be a list
        - Each column in the board must be a list
        - Each position of the board must be a tuple containing 2 integer numbers
        ASSUMPTIONS
        - None
    """
    if not isinstance(board, list):
        return False
    for col in board:
        if not isinstance(col, list):
            return False
        for row in col:
            if row is not None:
                if not isinstance(row, tuple):
                    return False
                if len(row) != 2:
                    return False
                for coordinate in row:
                    if not isinstance(coordinate, int):
                        return False
    return True


def dimension(board):
    """
        Return the dimension of the given board.
        - The function returns the number of rows (== number of columns) of
          the given board.
        ASSUMPTIONS
        - The given board is a proper board.
    """
    return len(board)


def get_all_filled_positions(board):
    """
        Return a set of all the positions of filled cells on the given board.
        ASSUMPTIONS
        - The given board is a proper board.
    """
    filled_positions = set()

    for col in range(dimension(board)):
        for row in range(dimension(board)):
            if not board[col][row] is None:
                filled_positions.add(board[col][row])

    return filled_positions


def is_filled_at(board, position):
    """
        Return a boolean indicating whether or not the cell at the given position
        on the given board is filled.
        - Returns false if the given position is outside the boundaries of the
          given board.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given position is a proper position.
    """
    for col in range(dimension(board)):
        for row in range(dimension(board)):
            if board[col][row] == position:
                return True
    return False


def is_filled_row(board, row):
    """
        Return a boolean indicating whether or not all the cells of the given
        row on the given board are filled.
        - Returns false if the given row is not an integer number or if it is
          outside the boundaries of the given board.
        ASSUMPTIONS
        - The given board is a proper board.
        NOTE
        - You are not allowed to use for statements in the body of this function.
    """
    if not isinstance(row, int):
        return False
    if row <= 0 or row > dimension(board):
        return False

    col = 0
    while col < dimension(board):
        if board[col][row-1] is None:
            return False
        col += 1
    return True


def is_filled_column(board, column):
    """
        Return a boolean indicating whether or not all the cells of the given
        column on the given board are filled.
        - Returns false if the given column is not an integer number or if it is
          outside the boundaries of the given board.
        ASSUMPTIONS
        - The given board is a proper board.
        NOTE
        - You are not allowed to use while statements in the body of this function.
    """
    if not isinstance(column, int):
        return False
    if column <= 0 or column > dimension(board):
        return False

    for row in range(dimension(board)):
        if board[column-1][row] is None:
            return False
    return True


def get_all_filled_rows(board):
    """
        Return all the rows on the given board that are completely filled.
        - The function returns a list of the numbers in ascending order of
          all the rows that are completely filled.
        ASSUMPTIONS
        - The given board is a proper board.
        NOTE
        - You are not allowed to use for statements in the body of this function.
    """
    if dimension(board) == 0:
        return []

    filled_rows = []
    col = 0
    row = 0
    while row < dimension(board):
        while col < dimension(board) and row < dimension(board):
            if board[col][row] is None:
                col = -1
                row += 1
            col += 1
        if col == dimension(board):
            if row == dimension(board):
                return filled_rows
            filled_rows += (row+1,)
            row += 1
            col = 0
        if row == dimension(board):
            return filled_rows


def get_all_filled_columns(board):          # deze functie is gelijkaardig aan de vorige maar hier heb ik met "filled pos" gewerkt. het nadeel is wel dat hij alles blijft overlopen, ookal zijn er Nones geweest. bij mijn vorige functie stopte hij bij een None en ging naar de volgende row. dit is efficienter denk ik?
    """
        Return all the columns on the given board that are completely filled.
        - The function returns a tuple of the numbers in descending order of
          all the columns that are completely filled.
        ASSUMPTIONS
        - The given board is a proper board.
        NOTE
        - You are not allowed to use while statements in the body of this function.
    """
    if dimension(board) == 0:
        return []

    filled_cols = []
    filled_pos = 0

    for col in range(dimension(board)):
        for row in range(dimension(board)):
            if not board[col][row] is None:
                filled_pos += 1
        if filled_pos == dimension(board):
            filled_cols += (col+1,)
        filled_pos = 0

    return tuple(filled_cols[::-1])


def fill_cell(board, position):
    """
        Fill the cell at the given position on the given board.
        - Nothing happens if the given position is outside the
          boundaries of the given board or if the given cell is
          already filled.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given position is a proper position.
    """
    if 0 < position[0] <= dimension(board) and 0 < position[1] <= dimension(board):
        board[position[0]-1][position[1]-1] = position


def fill_all_cells(board, positions):
    """
        Fill all the cells at each position in the given collection of
        positions on the given board.
        - Positions outside the boundaries of the given board are ignored.
        - Positions that are already filled are left untouched.
        ASSUMPTIONS
        - The given board is a proper board.
        - Each position in the collection of positions is a proper position.
    """
    for position in positions:
        fill_cell(board, position)


def free_cell(board, position):
    """
        Free the cell at the given position of the given board.
        - Nothing happens if the cell is already free or if the given
          position is outside the boundaries of the given board.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given position is a proper position.
    """
    if 0 < position[0] <= dimension(board) and 0 < position[1] <= dimension(board):
            board[position[0] - 1][position[1] - 1] = None


def free_all_cells(board, positions):
    """
        Free all the cells at each position in the tuple of positions on
        the given board.
        - Positions outside the boundaries of the given board are ignored.
        - Positions that are already free are left untouched.
        ASSUMPTIONS
        - The given board is a proper board.
        - Each position in the tuple of positions is a proper position.
        NOTE
        - This function must be worked out in a recursive way.
    """
    for pos in positions:
        free_cell(board, pos)
        positions.remove(pos)
        return free_all_cells(board, positions)


def free_row(board, row):
    """
        Free all the cells of the given row on the given board.
        - Nothing happens if the given row is not an integer number or if
          it is outside the boundaries of the given board.
        ASSUMPTIONS
        - The given board is a proper board.
    """
    if isinstance(row, int) and 0 < row <= dimension(board):
        for col in board:
            col[row-1] = None


def free_column(board, column):
    """
        Free all the cells of the given column on the given board.
        - Nothing happens if the given column is not an integer number or if
          it is outside the boundaries of the given board.
        ASSUMPTIONS
        - The given board is a proper board.
    """
    if isinstance(column, int) and 0 < column <= dimension(board):
        for row in range(dimension(board)):
            board[column-1][row] = None


def can_be_dropped_at(board, block, position):
    """
        Check whether the given block can be dropped at the given position.
        - The given position determines the position for the anchor of the
          given block.
        - True if and only if for each of the dot positions D of the given block
          there is a FREE cell at a position within the boundaries of the given
          board and at the same horizontal- and vertical distance from the
          given position as the horizontal- and vertical distance of the dot
          position D from the anchor of the given block.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given block is a proper block.
        - The given position is a proper position.
    """
    new_block = set()
    for dot in block:
        dot = list(dot)
        dot[0] += position[0]
        dot[1] += position[1]
        new_block.add(tuple(dot))

    checked_dots = 0

    for dot in new_block:
        for col in range(dimension(board)):
            for row in range(dimension(board)):
                if col == dot[0]-1 and row == dot[1]-1:
                    if board[col][row] is None:
                        checked_dots += 1
                        if checked_dots == len(new_block):
                            return True
    return False


def get_droppable_positions(board, block):
    """
        Return a list of all positions at which the given block can be dropped
        on the given board.
        - The positions in the resulting list are in ascending order.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given block is a proper block.
        NOTE
        - The function should only examine positions at which the given block
          fully fits within the boundaries of the given board.
    """
    droppable_positions = list()
    smallest_col = Block.get_horizontal_offsets_from_anchor(block)[0]
    largest_col = Block.get_horizontal_offsets_from_anchor(block)[1]
    smallest_row = Block.get_vertical_offsets_from_anchor(block)[0]
    largest_row = Block.get_vertical_offsets_from_anchor(block)[1]

    for col in range(-smallest_col, dimension(board) - largest_col):
        for row in range(-smallest_row, dimension(board) - largest_row):
            position = (col+1, row+1)
            if can_be_dropped_at(board, block, position):
                droppable_positions.append(position)
    return droppable_positions


def drop_at(board, block, position):
    """
        Drop the given block at the given position on the given board.
        - Each of the cells on the given board at a position with the same
          horizontal- and vertical distance from the given position as a dot
          position of the given block from the block's anchor, is filled.
        - Nothing happens if the given block can not be dropped at the given
          position on the given board.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given position is a proper position.
        - The given block is a proper block.
    """
    if can_be_dropped_at(board, block, position):
        for pos in block:
            pos = list(pos)
            pos[0] += position[0]
            pos[1] += position[1]
            board[pos[0]-1][pos[1]-1] = pos[0], pos[1]


def clear_full_columns(board):
    """
        Clear all full columns on the given board.
        ASSUMPTIONS
        - The given board is a proper board.
    """
    col = 0
    while col < dimension(board):
        filled = 0
        for row in range(dimension(board)):
            if not board[col][row] is None:
                filled += 1
                if filled == dimension(board):
                    for index in range(dimension(board)):
                        board[col][index] = None
        col += 1


def clear_full_rows(board):
    """
        Clear all full rows on the given board.
        ASSUMPTIONS
        - The given board is a proper board.
    """
    for row in range(dimension(board)):
        nb_filled_positions = 0
        for col in range(dimension(board)):
            if not board[col][row] is None:
                nb_filled_positions += 1
                if nb_filled_positions == dimension(board):
                    for index in range(dimension(board)):
                        board[index][row] = None


def clear_full_rows_and_columns(board):
    """
        Clear all full rows and all full columns on the given board.
        ASSUMPTIONS
        - The given board is a proper board.
    """
    full_columns = get_all_filled_columns(board)
    full_rows = get_all_filled_rows(board)

    for col in range(1, dimension(board)+1):
        if col in full_columns:
            for row in range(dimension(board)):
                board[col-1][row] = None

    for row in range(1, dimension(board)+1):
        if row in full_rows:
            for col in range(dimension(board)):
                board[col][row-1] = None


def get_filled_positions(board):
    """
    Returns all the filled positions of the board.
    ASSUMPTIONS:
        - the given board is a proper board
    """
    filled_positions = list()
    for col in range(dimension(board)):
        for row in range(dimension(board)):
            if not board[col][row] is None:
                filled_positions.append(board[col][row])

    return set(filled_positions)


def get_empty_positions(board):
    """
    Returns all the empty positions of the board.
    ASSUMPTIONS:
        - the given board is a proper board
    """
    empty_positions = list()
    for col in range(dimension(board)):
        for row in range(dimension(board)):
            if board[col][row] is None:
                empty_positions.append(tuple((col+1, row+1)))

    return empty_positions


def reverse_board(board):
    """
    Reverse the given board.
    A board is reversed if all the filled positions are turned empty and if all the empty positions are filled.
    ASSUMPTIONS:
        - the given board is a proper board
    """
    filled = get_filled_positions(board)
    empty = get_empty_positions(board)

    for position in empty:
        fill_cell(board, position)

    for position in filled:
        free_cell(board, position)


def are_chainable(board, positions, checked_positions=None, index_checked_pos=0, adj_pos=0):
    """
        Check whether the given collection of positions is chained on the
        given board.
        - True if and only if at least one collection of chained positions exists
          on the given board that includes all given positions and for which all
          the cells in that collection are either all filled or all empty.
        ASSUMPTIONS
        - The given board is a proper board.
        - Each of the given positions is a proper position for the given board.
        - All the cells on the given board at the given positions all have the
          same state, i.e. they are all filled or all empty.
        NOTE
        - This function should be worked out in a recursive way
    """
    if len(positions) <= 1:
        return True

    if Position.are_chained_rec(positions):
        return True

    if board[list(positions)[0][0]-1][list(positions)[0][1]-1] is None:
        reverse_board(board)

    filled_positions = get_filled_positions(board)
    for element in positions:
        filled_positions.add(element)  # moet hier eerst set blijven zodat er geen duplacates in komen
    filled_positions = list(filled_positions)

    if checked_positions is None:
        checked_positions = [(list(positions)[0])]

    if Position.is_adjacent_to(checked_positions[index_checked_pos], filled_positions):
        adjacent_positions = list(Position.get_adjacent_positions(checked_positions[index_checked_pos]))  # zijn er altijd 4
        if adj_pos == 4:
            if index_checked_pos == len(checked_positions) - 1:
                # check if all given positions are in the (chained) checked positions
                if len(set(positions).intersection(checked_positions)) == len(positions):
                    return True             # verschil tussen deze functie en are_chainable_rec is dat ik hier in checked positions ook posities ga hebben die oorspronkelijk al gefilled waren. ik moet dus nog extra checken hier of alle gegeven positions chained zijn, dus of alle gegeven positions in de checked positions zitten. (en niet enkel of alle checked positions de gegeven positions ZIJN)
                return False
            return are_chainable(board, positions, checked_positions, index_checked_pos + 1, 0)
        if adjacent_positions[adj_pos] in filled_positions and adjacent_positions[adj_pos] not in checked_positions:
            checked_positions.append(adjacent_positions[adj_pos])
        adj_pos += 1
        return are_chainable(board, positions, checked_positions, index_checked_pos, adj_pos)
    return False


def print_board(board):
    """
        Print the given board on the standard output stream.
        ASSUMPTIONS
        - The given board is a proper board.
    """
    for row in range(dimension(board), 0, -1):
        print('{:02d}'.format(row), end="  ")
        for column in range(1, dimension(board) + 1):
            if is_filled_at(board, (column, row)):
                print(" \u25A9 ", end=" ")
            else:
                print("   ", end=" ")
        print()
    print("    ", end="")
    for column in range(1, dimension(board) + 1):
        print('{:02d}'.format(column), end="  ")
    print()
