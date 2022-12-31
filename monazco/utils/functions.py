from monazco.board import Board
import monazco.constants as cs


def print_board(board: Board):

    throne1 = board[cs.THRONE_1_NUM].stones
    throne2 = board[cs.THRONE_2_NUM].stones
    dimples = board.board

    row = ("+" + "*" * 9) * 8 + "+"

    throne_1_section = "|" + " " * 4 + str(throne1)
    if len(str(throne1)) == 1:
        throne_1_section += " " * 4
    else:
        throne_1_section += " " * 3

    throne_2_section = " " * 4 + str(throne2)
    if len(str(throne2)) == 1:
        throne_2_section += " " * 4
    else:
        throne_2_section += " " * 3
    throne_2_section += "|"

    mid = throne_1_section + "|" + row[11:-11] + "|" + throne_2_section
    print(row)
    stone_values_1 = [str(dimples[i].stones) for i in [2, 1, 0, 13, 12, 11]]
    stone_values_2 = [str(dimples[i].stones) for i in [4, 5, 6, 7, 8, 9]]

    print("|", " " * 9, sep="", end="")

    for stone_value in stone_values_1:
        if len(stone_value) == 1:
            print("|" + " " * 4, stone_value, " " * 4, end="", sep="")
        else:
            print("|" + " " * 4, stone_value, " " * 3, end="", sep="")

    print("|" + " " * 9 + "|")
    print(mid)

    print("|", " " * 9, sep="", end="")
    for stone_value in stone_values_2:
        print("|" + " " * 4, stone_value, " " * 4, end="", sep="")

    print("|" + " " * 9 + "|")
    print(row)
