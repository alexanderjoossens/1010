# Positions are used to
#  (1) identify cells on the board
#  (2) dots on blocks relative to the block's anchor.


def is_proper_position(position):
    """
        Check whether the given position is a proper position.
        - True if and only if the given position is a tuple of length 2
          whose elements are both integer numbers.
        ASSUMPTIONS
        - None
    """
    if not isinstance(position, tuple):
        return False

    if not len(position) == 2:
        return False

    for element in position:
        if not isinstance(element, int):
            return False

    return True


def is_proper_position_for_board(dimension, position):
    """
        Check whether the given position is a proper position for a square
        board with the given dimension.
        - True if and only if (1) the given dimension is a positive integer
          number and (2) if the given position is a proper position within
          the boundaries of a board with the given dimension, i.e not below
          1 nor above the given dimension in both directions.
        ASSUMPTIONS
        - None
    """
    if not isinstance(dimension, int):
        return False

    if not dimension >= 0:
        return False

    if not is_proper_position(position):
        return False

    for element in position:
        if not 1 <= element <= dimension:
            return False

    return True


def left(dimension, position):
    """
        Return the position on any board with the given dimension immediately to
        the left of the given position.
        - None is returned if the generated position is outside the boundaries of
          a board with the given dimension.
        ASSUMPTIONS
        - The given position is a proper position for any board with the
          given dimension.
    """
    if position[0] <= 1 and dimension is not None:
        return None

    return position[0]-1, position[1]


def right(dimension, position):
    """
       Return the position on any board with the given dimension immediately to
       the right of the given position.
       - None is returned if the generated position is outside the boundaries of
         a board with the given dimension.
       ASSUMPTIONS
       - The given position is a proper position for any board with the
         given dimension.
     """
    if position[0] >= dimension:
        return None

    return position[0]+1, position[1]


def up(dimension, position):
    """
        Return the position on any board with the given dimension immediately
        above the given position.
        - None is returned if the generated position is outside the boundaries of
          a board with the given dimension.
        ASSUMPTIONS
        - The given position is a proper position for any board with the
          given dimension.
     """
    if position[1] >= dimension:
        return None

    return position[0], position[1] + 1


def down(dimension, position):
    """
        Return the position on any board with the given dimension immediately
        below the given position.
        - None is returned if the generated position is outside the boundaries of
          a board with the given dimension.
        ASSUMPTIONS
        - The given position is a proper position for any board with the
          given dimension.
     """
    if position[1] <= 1 and dimension is not None:
        return None

    return position[0], position[1]-1


def next(dimension, position):
    """
        Return the position on any board with the given dimension next to the
        given position.
        - If the given position is not at the end of a row, the resulting position
          is immediately to the right of the given position.
        - If the given position is at the end of a row, the resulting position is
          the leftmost position of the row above. If that next row does not exist,
          None is returned.
        ASSUMPTIONS
        - The given position is a proper position for any board with the
          given dimension.
     """
    if position[0] < dimension:
        return right(dimension, position)

    if position[1] < dimension:
        return 1, position[1]+1

    return None


def translate_over(position, delta_x, delta_y):
    """
        Return the position resulting from translating the given position horizontally
        and vertically over the given delta's.
        ASSUMPTIONS
        - The given position is a proper position.
        - The given delta's are integer numbers.
    """
    return position[0] + delta_x, position[1] + delta_y


def get_adjacent_positions(position, dimension=None):
    """
        Return a mutable set of all positions immediately adjacent to the
        given position and within the boundaries of a board with the given
        dimension.
        - Adjacent positions are either at a horizontal distance or at a vertical
          distance of 1 from the given position.
        - If the given dimension is None, no boundaries apply.
        ASSUMPTIONS
        - The given position is a proper position for any board with the
          given dimension, or simply a proper position if no dimension is supplied.
    """
    adjacent_positions = set()

    if dimension is None:
        adjacent_positions.add((position[0] - 1, position[1]))
        adjacent_positions.add((position[0] + 1, position[1]))
        adjacent_positions.add((position[0], position[1] - 1))
        adjacent_positions.add((position[0], position[1] + 1))
        return adjacent_positions

    if not position[1] <= 1:
        adjacent_positions.add((position[0], position[1]-1))
    if not position[1] >= dimension:
        adjacent_positions.add((position[0], position[1]+1))
    if not position[0] <= 1:
        adjacent_positions.add((position[0]-1, position[1]))
    if not position[0] >= dimension:
        adjacent_positions.add((position[0]+1, position[1]))

    return adjacent_positions


def is_adjacent_to(position, other_positions):
    """
        Check whether the given position is adjacent to at least one of the positions
        in the collection of other positions.
        - True if and only if at least one of the other positions is one of the positions
          adjacent to the given position in an unbounded area.
        ASSUMPTIONS
        - The given position is a proper position
        - All positions in the collection of other positions are proper positions.
    """
    for other_position in other_positions:
        for adj_pos in get_adjacent_positions(position):
            if adj_pos == other_position:
                return True

    return False


def get_surrounding_positions(position, dimension=None):
    """
        Return a mutable set of all positions immediately surrounding the
        given position and within the boundaries of a board with the given
        dimension.
        - Surrounding positions are at a horizontal distance and/or a vertical
          distance of 1 from the given position.
        - If the given dimension is None, no boundaries apply.
        ASSUMPTIONS
        - The given position is a proper position for any board with the
          given dimension, or simply a proper position if no dimension is supplied.
    """
    surrounding_positions = set()

    if dimension is None:
        for adj_pos in get_adjacent_positions(position):
            surrounding_positions.add(adj_pos)
        surrounding_positions.add((position[0] - 1, position[1] - 1))
        surrounding_positions.add((position[0] + 1, position[1] - 1))
        surrounding_positions.add((position[0] - 1, position[1] + 1))
        surrounding_positions.add((position[0] + 1, position[1] + 1))
        return surrounding_positions

    for adj_pos in get_adjacent_positions(position, dimension):
        surrounding_positions.add(adj_pos)

    if not position[1] <= 1 and not position[0] <= 1:
        surrounding_positions.add((position[0]-1, position[1]-1))
    if not position[1] <= 1 and not position[0] >= dimension:
        surrounding_positions.add((position[0]+1, position[1]-1))
    if not position[1] >= dimension and not position[0] <= 1:
        surrounding_positions.add((position[0]-1, position[1]+1))
    if not position[1] >= dimension and not position[0] >= dimension:
        surrounding_positions.add((position[0]+1,position[1]+1))

    return surrounding_positions


def are_chained(positions):
    """
        Check whether the given collection of positions make up a chain.
        - True if and only if each position in the given collection of positions
          can be reached from each other position in that collection.
          A position P1 can be reached from another position P2 if
            (1) P1 and P2 are adjacent to each other, or
            (2) there exists at least one position P3 in the given collection
                of positions that can be reached from both P1 and P2.
       ASSUMPTIONS
       - Each position in the collection of positions is a proper position.
       NOTE
       - This version of the function must be worked out in an iterative way.
         The body may use while statements and/or for statements.
    """
    if len(positions) <= 1:
        return True

    positions_without_duplicates = []
    for item in positions:
        if item not in positions_without_duplicates:
            positions_without_duplicates.append(item)

    checked_positions = [positions_without_duplicates[0]]

    for pos in checked_positions:
        if is_adjacent_to(pos, positions):
            adjacent_positions = get_adjacent_positions(pos)
            for adjacent_pos in adjacent_positions:
                if adjacent_pos in positions and adjacent_pos not in checked_positions:
                    checked_positions.append(adjacent_pos)

    if len(checked_positions) == len(positions_without_duplicates):
        return True

    return False


def are_chained_rec \
                (positions, checked_positions=None, no_duplicates=None, index_checked_pos=0, index_adjacent_pos=0):
    """
        Check whether the given collection of positions make up a chain.
        - True if and only if each position in the given collection of positions
          can be reached from each other position in that collection.
          A position P1 can be reached from another position P2 if
            (1) P1 and P2 are adjacent to each other, or
            (2) there exists at least one position P3 in the given collection
                of positions that can be reached from both P1 and P2.
       ASSUMPTIONS
       - Each position in the collection of positions is a proper position.
       NOTE
       - This version of the function must be worked out in a recursive way. The body
         may not use while statements nor for statements.
       TIP
       - Extend the heading of the function with two additional parameters:
          - chained_positions: a frozen set of positions that already form a chain.
          - non_chainable_positions: a frozen set of positions that are not
            adjacent to any of the positions in the set of chained positions.
         Assign both extra parameters the empty frozen set as their default value.
    """
    if len(positions) <= 1:
        return True

    if checked_positions is None:
        checked_positions = [(list(positions)[0])]

    if is_adjacent_to(checked_positions[index_checked_pos], positions):
        adjacent_positions = list(get_adjacent_positions(checked_positions[index_checked_pos]))
        if index_adjacent_pos == 4:
            if index_checked_pos == len(checked_positions) - 1:
                no_duplicates = set(positions)
                if len(checked_positions) == len(no_duplicates):
                    return True
                return False
            return are_chained_rec(positions, checked_positions, no_duplicates, index_checked_pos+1, index_adjacent_pos=0)
        if adjacent_positions[index_adjacent_pos] in positions and adjacent_positions[index_adjacent_pos] not in checked_positions:
            checked_positions.append(adjacent_positions[index_adjacent_pos])
        index_adjacent_pos += 1
        return are_chained_rec(positions, checked_positions, no_duplicates, index_checked_pos, index_adjacent_pos)
    return False
