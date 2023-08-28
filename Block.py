from PycharmProjects.Examenpracticum1010.skelet import Position


def make_block(dot_positions):
    """
       Create a new block involving the given mutable set of dot positions.
       ASSUMPTIONS
       - The given set of dot positions is not empty and each of its
         elements is a proper position.
       - The given dot positions are chained together.
    """
    return set(dot_positions)


def get_all_dot_positions(block):
    """
        Return a mutable set of all the dot positions of the given block.
        - Dot positions are relative towards the block's anchor.
        ASSUMPTIONS
        - The given block is a proper block.
    """
    return set(block)


def is_proper_block(block):
    """
        Check whether the given block is a proper block.
        - True if and only if the set of dot positions of the given block is not empty,
          if each of its elements is a proper position, and if the dot positions of the
          given block are chained together.
        ASSUMPTIONS:
        - None
    """
    if not isinstance(block, set):
        return False

    for position in block:
        if not isinstance(position, tuple):
            return False
        for coordinate in position:
            if not isinstance(coordinate, int):
                return False

    return True


def add_dot(block, dot_position):
    """
        Add the given dot position to the given block.
        - Nothing happens if the given block already has a dot at the given position, or
          if the given dot cannot be chained with existing dots of the given block.
        ASSUMPTIONS
        - The given block is a proper block.
        - The given position is a proper position.
    """
    if Position.is_adjacent_to(dot_position, block):
        block.add(dot_position)


def remove_dot(block, dot_position):
    """
        Remove the given dot position from the given block.
        - Nothing happens if the given dot is not part of the given block, if the
          given block only has the dot to be removed as its single dot, or if the dots
          in the resulting block can no longer be chained.
        ASSUMPTIONS
        - The given block is a proper block.
        - The given position is a proper position.
    """
    if len(block) != 1 and Position.are_chained(block-{dot_position}):
        block.discard(dot_position)


def get_horizontal_offsets_from_anchor(block):
    """
        Return the horizontal offsets from the anchor of this block.
        - The function returns a tuple involving the smallest horizontal offset
          to the left of the anchor, followed by the largest horizontal offset
          to the right the anchor.
          More formally, if the function returns the tuple (L,R), then for each dot
          position (x,y) of the given block, L <= x <= R
        ASSUMPTIONS
        - The given block is a proper block.
    """
    smallest = list(block)[0][0]
    for position in block:
        if position[0] < smallest:
            smallest = position[0]

    largest = list(block)[0][0]
    for position in block:
        if position[0] > largest:
            largest = position[0]

    return smallest, largest


def get_vertical_offsets_from_anchor(block):
    """
        Return the vertical offsets from the anchor of this block.
        - The function returns a tuple involving the smallest vertical offset
          below the anchor, followed by the largest vertical offset above the anchor.
          More formally, if the function returns the tuple (B,A), then for each dot
          position (x,y) of the given block, B <= y <= A
        ASSUMPTIONS
        - The given block is a proper block.
    """
    smallest = list(block)[0][1]
    for position in block:
        if position[1] < smallest:
            smallest = position[1]

    largest = list(block)[0][1]
    for position in block:
        if position[1] > largest:
            largest = position[1]

    return smallest, largest


def get_anchor(block):
    """
    Returns the anchor of the block.
    The anchor is a list containing the smallest column and the smallest row
    from a position in the block.
    ASSUMPTIONS
        - The given block is a proper block.
    """
    smallest_col = get_horizontal_offsets_from_anchor(block)[0]
    smallest_row = get_vertical_offsets_from_anchor(block)[0]

    return [smallest_col, smallest_row]


def distances_to_anchor(block):
    """
    Returns a set, containing de distances from every position in the block to the anchor of the block.
    ASSUMPTIONS
        - The given block is a proper block.
    """
    distances = set()
    block = list(block)
    anchor = get_anchor(block)

    for position in block:
        col_distance = position[0] - anchor[0]
        row_distance = position[1] - anchor[1]
        distance_to_anchor = (col_distance, row_distance)
        distances.add(distance_to_anchor)

    return distances


def are_equivalent(block, other_block):
    """
       Check whether the given blocks are equivalent, i.e. cover equivalent
       chains of dots.
       - A block is equivalent with some other block , if there exists a position
         for the anchor of the one block such that the set of dots covered by that
         block relative towards that anchor position, is identical to the set of
         dots covered by the other block.
        ASSUMPTIONS
        - Both given blocks are proper blocks.
    """
    if distances_to_anchor(block) == distances_to_anchor(other_block):
        return True

    return False


def is_normalized(block):
    """
       Check whether the given block is normalized.
       - True if and only if the anchor of the given block is one of the dot positions
         of that block.
       ASSUMPTIONS
       - The given block is a proper block.
    """
    if tuple((0, 0)) in block:
        return True

    return False


def normalize(block):
    """
       Return a new block that is a normalized version of the given block.
       - The resulting block must be equivalent with the given block.
       - The function is free to choose a proper anchor for the normalized
         block.
       ASSUMPTIONS
       - The given block is a proper block.
    """
    random_position = list(block)[0]
    anchor = []
    for coordinate in random_position:
        anchor.append(coordinate)

    # make the block listed
    block_listed = []
    for position in block:
        block_listed.append(list(position))

    # manipulate each position, so it accords to the anchor [0,0]
    for position in block_listed:
        position[0] -= anchor[0]
        position[1] -= anchor[1]

    # put every position in shape of tuple in a new set
    new_block = set()
    for position in block_listed:
        new_block.add(tuple(position))

    return new_block


def print_block(block):
    """
        Print the given block on the standard output stream.
        - The anchor of the given block will be revealed in the print-out.
        ASSUMPTIONS
        - The given block is a proper block.
    """
    horizontal_offsets = get_horizontal_offsets_from_anchor(block)
    width = max(horizontal_offsets[1], 0) - min(horizontal_offsets[0], 0) + 1
    vertical_offsets = get_vertical_offsets_from_anchor(block)
    height = max(vertical_offsets[1], 0) - min(vertical_offsets[0], 0) + 1
    printout = [[" " for column in range(1, width + 1)]
                for row in range(1, height + 1)]
    dot_positions = get_all_dot_positions(block)
    for (column, row) in dot_positions:
        printout[row - min(vertical_offsets[0], 0)] \
            [column - min(horizontal_offsets[0], 0)] = "\u25A9"
    if (0, 0) in dot_positions:
        anchor_symbol = "\u25A3"
    else:
        anchor_symbol = "\u25A2"
    printout[-min(vertical_offsets[0], 0)][-min(horizontal_offsets[0], 0)] = anchor_symbol
    for row in range(len(printout) - 1, -1, -1):
        for col in range(0, len(printout[0])):
            print(printout[row][col], end=" ")
        print()


# collection of standard blocks used to play the game.


standard_blocks = \
    (  # Single dot
        make_block({(0, 0)}),
        # Horizontal line of length 2
        make_block({(0, 0), (1, 0)}),
        # Horizontal line of length 3
        make_block({(-1, 0), (0, 0), (1, 0)}),
        # Horizontal line of length 4
        make_block({(-3, 0), (-2, 0), (-1, 0), (0, 0)}),
        # Horizontal line of length 5
        make_block({(0, 2), (1, 2), (2, 2), (3, 2), (4, 2)}),
        # Vertical line of length 2
        make_block({(0, 0), (0, 1)}),
        # Vertical line of length 3
        make_block({(0, -1), (0, 0), (0, 1)}),
        # Vertical line of length 4
        make_block({(-2, 2), (-2, 3), (-2, 4), (-2, 5)}),
        # Vertical line of length 5
        make_block({(0, -6), (0, -5), (0, -4), (0, -3), (0, -2)}),
        # T-squares 1x1
        make_block({(-1, 0), (0, 0), (0, 1)}),
        make_block({(0, 0), (0, 1), (1, 0)}),
        make_block({(0, 0), (0, -1), (1, 0)}),
        make_block({(-1, 0), (0, 0), (0, -1)}),
        # T-squares 2x2
        make_block({(-2, 0), (-1, 0), (0, 0), (0, 1), (0, 2)}),
        make_block({(0, 2), (1, 2), (2, 2), (2, 1), (2, 0)}),
        make_block({(2, 0), (1, 0), (0, 0), (0, -1), (0, -2)}),
        make_block({(-2, -2), (-1, -2), (0, -2), (-2, -1), (-2, 0)}),
        # Square block 2x2
        make_block({(0, 0), (1, 0), (0, 1), (1, 1)}),
        # Square block 3x3
        make_block({(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)}),
    )


def select_standard_block():
    """
        Return one of the standard blocks.
        - The resulting block is selected randomly.
    """
    import random
    return random.choice(standard_blocks)
