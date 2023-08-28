from PycharmProjects.Examenpracticum1010.skelet import Board
from PycharmProjects.Examenpracticum1010.skelet import Block
from math import factorial
from random import sample


def game_move(board, block, position):
    """
        Drop the given block at the given position on the given board, and
        clear all full rows and columns, if any, after the drop.
        - The function returns the score obtained from the give move.
        ASSUMPTIONS
        - The given board is a proper board
        - The given block is a proper block.
        - The given position is a proper position.
        - The given block can be dropped at the given position on the given
          board.
    """
    Board.drop_at(board, block, position)
    nb_filled_seqs = \
        len(Board.get_all_filled_columns(board)) + \
        len(Board.get_all_filled_rows(board))
    Board.clear_full_rows_and_columns(board)
    return \
        len(Block.get_all_dot_positions(block)) + \
        10 * ((nb_filled_seqs + 1) * nb_filled_seqs) // 2


def highest_score(board, blocks, start=0):
    """
        Return the highest possible score that can be obtained by dropping
        all the blocks in the given sequence of blocks starting from the given
        start index in the order from left to right on the given board.                # wat is van left to right? van (1,1) tot (10,10 proberen zetten?)
        - If a solution is possible, the function actually returns a tuple
          consisting of the highest score followed by a list of all positions
          at which the successive blocks must be dropped.
        - If the highest score can be reached in several possible ways, the
          function will give preference to the smallest position in the sense of                    # hoe check ik dit?
          the standard tuple comparison in Python (see section 6.7 of the book).
          For example, if there are two solutions s1 and s2 and s1 < s2, s1 will
          be returned.
        - If no solution is possible, the function returns the tuple (None,None).
        - At the end of the function, the board must still be in the same
          state it was in at the start of the function.
        ASSUMPTIONS
        - The given board is a proper board.
        - Each block in the given sequence of blocks is a proper block.
        - The given start index is not negative, but may be beyond the last element
          in the sequence of blocks.
        NOTE
        - You are allowed to take a copy of the given board.
        - You are not allowed to extend the heading of the function with
          additional parameters, nor to introduce an auxiliary function
          to be able to pass additional information.
        - The function should be worked out in a recursive way.
    """
    if start == len(blocks):
        return 0, list()

    droppable_positions = Board.get_droppable_positions(board, blocks[start])                                           # zijn automatisch gerangschikt van klein nr groot. zo vind hij automatisch de hoogste score als eerst met een blok dat een 'kleine tuple' heeft. daarna vindt hij heel vaak dezelfde hoogste score, maar met een hogere tuple dus slaat hij die niet op.
    if len(droppable_positions) == 0:
        return None, None

    highest_result = None, None
    copy_board = Board.copy_board(board)

    for droppable_pos in droppable_positions:

        current_score = game_move(copy_board, blocks[start], droppable_pos)
        current_result = highest_score(copy_board, blocks, start + 1)

        if not current_result[0] is None:
            current_score += current_result[0]
            current_positions = [droppable_pos] + current_result[1]

            if highest_result[0] is None or current_score > highest_result[0]:                                     # eerste de eerste compare want als die None is dan stopt het al meteen (want zou error geven als je None met integer vergelijkt)
                highest_result = current_score, current_positions

        copy_board = Board.copy_board(board)                                                                            # waarom dit nog op einde?

    return highest_result


#    if start == len(blocks):
#        return 0, list()
#
#    droppable_positions = Board.get_droppable_positions(board, blocks[start])                               # zijn automatisch gerangschikt van klein nr groot. zo vind hij automatisch de hoogste score als eerst met een blok dat een 'kleine tuple' heeft. daarna vindt hij heel vaak dezelfde hoogste score, maar met een hogere tuple dus slaat hij die niet op.
#    if len(droppable_positions) == 0:
#        return None, None
#
#    highest_result = None, None
#    copy_board = Board.copy_board(board)
#
#    for droppable_pos in droppable_positions:
#        Board.drop_at(copy_board, blocks[start], droppable_pos)
#        full_rows_and_cols = list(Board.get_all_filled_rows(copy_board)) + list(Board.get_all_filled_columns(copy_board))
#        Board.clear_full_rows_and_columns(copy_board)
#        current_result = highest_score(copy_board, blocks, start+1)
#
#        if current_result[0] is not None:                                                                             # wnr wel None,None?
#            current_positions = [droppable_pos]+current_result[1]                                           # moet in deze volgorde want de volgorde waarin de posities in deze lijst komen te staan is belangrijk. eerst moet de laatste positie eigenlijk ingevuld worden, en dan de voorlaatste,... want het is recursief    schrijfwijze [droppable pos] is zoiets als (1,2) daar [(1,2)] van maken, zodat je 2 lijsten van tuples bij elkaar kan optellen. je zou ook list((droppable_pos,)) kunnen nemen maar niet gwn list(droppable_pos,) want dan verandert de tuple gwn in een lijst en is het geen lijst van een tuple meer
#            current_score = current_result[0] + len(blocks[start]) + \
#                    (len(full_rows_and_cols) + 1) * 10 * (len(full_rows_and_cols))/2                        # vanwaar komt die +1? en *10 en /2 veranderen door *5?
#
#            if highest_result[0] is None or current_score > highest_result[0]:                              # eerste de eerste compare want als die None is dan stopt het al meteen (want zou error geven als je None met integer vergelijkt)
#                highest_result = current_score, current_positions
#
#        copy_board = Board.copy_board(board)                                                                          # waarom dit nog op einde?
#
#    return highest_result


def best_placement(board, blocks):
    """
    Return: 1) the highest score that can be obtained by placing the blocks (max 3 blocks)
            2) the positions of those placements
            3) the order in which the given blocks must be placed
    - If a solution has been found, return the score
    - if no solution has been found, return None
    ASSUMPTIONS:
    - The given board is a proper board
    - The given blocks are proper blocks
    """
    if len(blocks) == 0:
        return 0, list(), list()

    # create a list that contains all the possible combinations in which the blocks can be placed
    nb_possible_combinations = factorial(len(blocks))
    possibile_combinations = list()
    while len(possibile_combinations) < nb_possible_combinations:
        possibility = list(sample(blocks, len(blocks)))
        if possibility not in possibile_combinations:
            possibile_combinations.append(possibility)

    best_result = None, None, None

    for possible_combination in possibile_combinations:

        result = highest_score(board, possible_combination)

        if result[0] is None:
            return None, None, None

        if best_result[0] is None or best_result[0] < result[0]:
            best_result = result[0], result[1], possible_combination

    return best_result


def play_greedy(board, blocks):
    """
        Drop the given sequence of blocks in the order from left to right on
        the given board in a greedy way.
        - The function will take blocks in triplets (groups of 3) in the order from
          left tot right, and drop them on the given board in the best possible way
          (i.e yielding the highest possible score) not taking into account blocks
          that still need to be dropped further on.
        - If the number of blocks is not a multiple of 3, the function will take the
          remaining blocks (1 or 2) in the last step.
        - The function will search for the best possible positions to drop each
          of the 3 blocks in succession. If several positions yield the same highest
          score, the function will give preference to positions closest to the bottom
          left corner.
        - If a solution is possible, the function returns the total score obtained
          from dropping all the blocks.
        - If no solution is possible, the function returns None. All the blocks that
          could be dropped are effectively dropped on the given board.
        ASSUMPTIONS
        - The given board is a proper board.
        - The number of blocks in the given sequence of blocks is a multiple of 3.
    """
    highscore = 0

    while len(blocks) != 0:
        best_result = best_placement(board, blocks[0:3])
        if best_result[0] is None:
            return None
        else:
            for index in range(len(best_result[1])):
                Board.drop_at(board, best_result[2][index], best_result[1][index])
                Board.clear_full_rows_and_columns(board)
            highscore += best_result[0]
        blocks = blocks[3:]

    return highscore


def play_game():
    """
        Play the game.
    """
    the_board = Board.make_board(5)
    score = 0
    current_block = Block.select_standard_block()
    print("Score: ", score)
    print()
    print("Next block to drop:")
    Block.print_block(current_block)
    print()
    Board.print_board(the_board)
    print()

    while len(Board.get_droppable_positions(the_board, current_block)) > 0:

        position = input("Enter the position to drop the block: ")
        if position == "":
            position = \
                random.choice(Board.get_droppable_positions(the_board, current_block))
            print("   Using position: ", position[0], ",", position[1])
        else:
            position = eval(position)
            if not isinstance(position, tuple):
                print("Not a valid position")
                continue

        if not Board.can_be_dropped_at(the_board, current_block, position):
            print("Block cannot be dropped at the given position")
            continue

        score += game_move(the_board, current_block, position)

        current_block = Block.select_standard_block()
        print("Score: ", score)
        print()
        print("Next block to drop:")
        Block.print_block(current_block)
        print()
        Board.print_board(the_board)
        print()

    print("End of game!")
    print("   Final score: ", score)


if __name__ == '__main__':
    play_game()