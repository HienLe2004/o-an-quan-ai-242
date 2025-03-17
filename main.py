from game import *
if __name__ == '__main__':
    game = Game()
    game.run()
# BASE GAME'S LOGIC

# board:list = [0,5,5,5,5,5,0,5,5,5,5,5]
# quan_count:list = [1,1]
# point_count:list = [0,0]
# is_player1_turn:bool = True
# QUAN_COEFFICIENT:int = 5
# def clamp(value):
#     while value < 0:
#         value += 12
#     while value > 11:
#         value -= 12
#     return value
# def Move(board:list, index:int, is_clockwise:bool):
#     print(f"index: {index}, is_clockwise: {is_clockwise}")
#     if index < 0 or index > 11 or index == 0 or index == 6:
#         return
#     if board[index] == 0:
#         return 
#     pieces_on_hand = board[index]
#     board[index] = 0
#     step = 1
#     if is_clockwise:
#         step = -1
#     current_index = index

#     while pieces_on_hand != 0:
#         current_index = clamp(current_index + step)
#         board[current_index] += 1
#         pieces_on_hand -= 1

#     current_index = clamp(current_index + step)
#     #Not empty and not O_QUAN -> new Move
#     if (board[current_index] != 0 and current_index != 0 and current_index != 6):
#         Move(board, current_index, is_clockwise)
#         return
#     #Empty and next square is not empty -> get Points
#     while (board[current_index] == 0 and board[clamp(current_index + step)] != 0):
#         points = board[clamp(current_index + step)]
#         if (clamp(current_index + step) in [0,6]):
#             points += quan_count[(clamp(current_index + step)%5)] * QUAN_COEFFICIENT
#             quan_count[(clamp(current_index + step)%5)] = 0
#         global point_count
#         if is_player1_turn:
#             point_count[0] += points
#         else:
#             point_count[1] += points
#         print(f"Get {board[clamp(current_index + step)]} points at index {clamp(current_index + step)}")
#         board[clamp(current_index + step)] = 0
#         current_index = clamp(current_index + 2 * step)
        


# print(board)
# print(point_count)
# # is_player1_turn = True
# # Move(board, 2, True)
# # print(board)
# # print(point_count)

# is_player1_turn = False
# Move(board, 10, False)
# print(board)
# print(point_count)

# is_player1_turn = True
# Move(board, 3, False)
# print(board)
# print(point_count)

# is_player1_turn = False
# Move(board, 9, True)
# print(board)
# print(point_count)

# is_player1_turn = True
# Move(board, 3, True)
# print(board)
# print(point_count)

# is_player1_turn = False
# Move(board, 11, False)
# print(board)
# print(point_count)

# is_player1_turn = True
# Move(board, 5, True)
# print(board)
# print(point_count)

# is_player1_turn = False
# Move(board, 7, True)
# print(board)
# print(point_count)

# is_player1_turn = True
# Move(board, 3, True)
# print(board)
# print(point_count)

# is_player1_turn = False
# Move(board, 11, False)
# print(board)
# print(point_count)

# is_player1_turn = True
# Move(board, 1, False)
# print(board)
# print(point_count)

# is_player1_turn = False
# Move(board, 7, True)
# print(board)
# print(point_count)

# is_player1_turn = True
# Move(board, 1, False)
# print(board)
# print(point_count)

# point_count[1] -= 5
# for i in range(7,12):
#     board[i] = 1
# is_player1_turn = False
# Move(board, 11, False)
# print(board)
# print(point_count)

# point_count[0] -= 5
# for i in range(1,6):
#     board[i] = 1
# is_player1_turn = True
# Move(board, 1, False)
# print(board)
# print(point_count)


# print(quan_count)