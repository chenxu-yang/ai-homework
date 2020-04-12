#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import time
import sys
ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def backtracking(board):
    """Takes a board and returns solved board."""
    # TODO: implement this
    if complete(board):
        return board
    pose,domian=select_unassigned_values(board)
    for value in domian:
        if consistent(pose[0],pose[1],value,board):
            board[pose]=value
            ans=backtracking(board)
            if ans:
                return ans
            board[pose] = 0
    return False

def complete(board):
    for pose in board:
        if board[pose]==0:
            return False
    return True
def select_unassigned_values(board):
    best_pose=None
    min_count=float('inf')
    can_choose=set()
    for pose in board:
        if board[pose]==0:
            count,domain=remaining_val(board,pose)
            if count<min_count:
                min_count=count
                best_pose=pose
                can_choose=domain
    return best_pose,can_choose
def remaining_val(board,pose):
    cannot_choose=set()
    total_domain=set([i for i in range(1,10)])
    for i in range(len(COL)):
        if board[pose[0]+COL[i]]:
            cannot_choose.add(board[pose[0]+COL[i]])
        if board[ROW[i]+pose[1]]:
            cannot_choose.add(board[ROW[i]+pose[1]])
    # row_square = ROW.find(pose[0]) // 3 * 3
    # col_square = (int(pose[1]) - 1) // 3 * 3
    # for r in range(row_square, row_square + 3):
    #     for c in range(col_square, col_square + 3):
    #         if r == ROW.find(pose[0]) or c == int(pose[1]) - 1:
    #             continue
    #         pose = ROW[r] + COL[c]
    #         cannot_choose.add(board[pose])

    return len(COL)-len(cannot_choose),total_domain-cannot_choose


def consistent(row, col, value, board):
    for c in COL:
        pose = row + c
        if value == board[pose]:
            return False

    for r in ROW:
        pose = r + col
        if value == board[pose]:
            return False

    row_square = ROW.find(row) // 3 * 3
    col_square = (int(col) - 1) // 3 * 3
    for r in range(row_square, row_square + 3):
        for c in range(col_square, col_square + 3):
            if r == ROW.find(row) or c == int(col) - 1:
                continue

            pose = ROW[r] + COL[c]

            if value == board[pose]:
                return False
    return True



if __name__ == '__main__':
    #  Read boards from source.
    line=sys.argv[1]
    #src_filename = 'sudokus_start.txt'
    # try:
    #     srcfile = open(src_filename, "r")
    #     sudoku_list = srcfile.read()
    # except:
    #     print("Error reading the sudoku file %s" % src_filename)
    #     exit()

    # Setup output file
    out_filename = 'output.txt'
    outfile = open(out_filename, "w")
    max_cost=0
    min_cost=float('inf')
    cost=[]
    board = {ROW[r] + COL[c]: int(line[9 * r + c])for r in range(9) for c in range(9)}
    start_time=time.time()
    # Print starting board. TODO: Comment this out when timing runs.
    #print_board(board)

 # Solve with backtracking
    solved_board = backtracking(board)
    end_time=time.time()
    max_cost=max(max_cost,end_time-start_time)
    min_cost=min(min_cost,end_time-start_time)
    cost.append(end_time-start_time)
    print("time cost",end_time-start_time)
    # Print solved board. TODO: Comment this out when timing runs.
    print_board(solved_board)

    # Write board to file
    outfile.write(board_to_string(solved_board))
    outfile.write('\n')
    # Solve each board using backtracking
    # for line in sudoku_list.split("\n"):
    #
    #     if len(line) < 9:
    #         continue
    #
    #     # Parse boards to dict representation, scanning board L to R, Up to Down
    #     board = { ROW[r] + COL[c]: int(line[9*r+c])
    #               for r in range(9) for c in range(9)}
    #     start_time=time.time()
    #     # Print starting board. TODO: Comment this out when timing runs.
    #     #print_board(board)
    #
    #     # Solve with backtracking
    #     solved_board = backtracking(board)
    #     end_time=time.time()
    #     max_cost=max(max_cost,end_time-start_time)
    #     min_cost=min(min_cost,end_time-start_time)
    #     cost.append(end_time-start_time)
    #     print("time cost",end_time-start_time)
    #     # Print solved board. TODO: Comment this out when timing runs.
    #     print_board(solved_board)
    #
    #     # Write board to file
    #     outfile.write(board_to_string(solved_board))
    #     outfile.write('\n')
    deviation=0
    mean=sum(cost)/len(cost)
    for time in cost:
        deviation+=(time-mean)**2
    standard_deviation=(deviation/len(cost))**2
    print("Finishing all boards in file.")
    print("the biggest running time:",max_cost)
    print("the smallest running time:", min_cost)
    print("the mean running time:", mean)
    print("the running time standard deviation:",standard_deviation)