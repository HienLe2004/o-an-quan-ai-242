import copy
import math


# Ở file này nếu muốn lấy AI đánh thì có thể lấy player hay opponent đều được, truyền vào các tham chiếu liên quan thì nó sẽ return best_move gồm (new_board, new_quan_count, new_point_count)
# Lưu ý thêm là opponent(board, quan_count, point_count, depth), depth là độ sâu tối đa cho minimax duyệt tới, tuy nhiên tui thấy cho depth = 4 lại ngon hơn depth = 6 :)))


# Trong hàm logic_game_clone thì có 2 tham số là indx(đó là index của vị trí muốn đánh) và dir(0 nếu muốn rải quân theo chiều giảm indx, 1 theo chiều tăng indx)

max_depth = 4

def logic_game_clone(board, quan_count, point_count, indx: int, dir: int, is_player1_turn: bool):
    if is_player1_turn:
        if indx < 1 or indx >= 6:
            return False  # Nước đi không hợp lệ

        check_empty = all(board[i] == 0 for i in range(1, 6))
        if check_empty:
            for i in range(1, 6):
                board[i] += 1
            point_count[0] -= 5
    else:
        if indx < 7 or indx >= 12:
            return False

        check_empty = all(board[i] == 0 for i in range(7, 12))
        if check_empty:
            for i in range(7, 12):
                board[i] += 1
            point_count[1] -= 5

    if board[indx] == 0:
        return False  # Ô trống không thể đi

    seeds = board[indx]
    board[indx] = 0
    pos = indx
    step = 1 if dir == 1 else -1

    def count_next_step(temp_pos, temp_step):
        return len(board) - 1 if (temp_pos == 0 and temp_step == -1) else (temp_pos + temp_step) % len(board)

    while seeds > 0:
        pos = count_next_step(pos, step)
        board[pos] += 1
        seeds -= 1

        if seeds == 0:
            temp = count_next_step(pos, step)
            if temp == 0 or temp == 6:  # Ô quan
                break

            if board[temp] > 0:
                seeds = board[temp]
                board[temp] = 0
                pos = temp
                continue
            else:
                temp = count_next_step(temp, step)
                while board[temp] > 0:
                    if (temp == 0 or temp == 6) and board[temp] < 5:
                        break
                    if is_player1_turn:
                        point_count[0] += board[temp]
                        if temp == 0:
                            point_count[0] += 5
                            quan_count[0] = 0
                        if temp == 6:
                            point_count[0] += 5
                            quan_count[1] = 0
                    else:
                        point_count[1] += board[temp]
                        if temp == 0:
                            point_count[1] += 5
                            quan_count[0] = 0
                        if temp == 6:
                            point_count[1] += 5
                            quan_count[1] = 0
                    board[temp] = 0
                    if quan_count[0] == 0 and quan_count[1] == 0:
                        break
                    temp = count_next_step(temp, step)
                    if board[temp] > 0 or temp == 0 or temp == 6:
                        break
                    temp = count_next_step(temp, step)

    return True

def evaluate(board, quan_count, point_count):
    #Số quân trên sân của mỗi người chơi
    s1 = sum(board[1:6])
    s2 = sum(board[7:12])

    #Số điểm đã ăn được
    Q1 = point_count[0]
    Q2 = point_count[1]

    #Số quân trong túi
    T1 = Q1
    T2 = Q2

    #Trọng số w1 thay đổi theo số quân trong túi
    k = 2
    C = 10
    w1 = k * math.exp(-T1 / C)

    return (Q1 - Q2) + w1 * (s1 - s2)

def minimax(board, quan_count, point_count, depth, is_maximizing):
    if depth == 0 or (quan_count[0] == 0 and quan_count[1] == 0):
        return evaluate(board, quan_count, point_count)
    
    if is_maximizing:
        max_eval = -math.inf
        for move in find_successor_player(board, quan_count, point_count):
            new_board, new_quan_count, new_point_count = move
            eval = minimax(new_board, new_quan_count, new_point_count, depth - 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = math.inf
        for move in find_successor_opponent(board, quan_count, point_count):
            new_board, new_quan_count, new_point_count = move
            eval = minimax(new_board, new_quan_count, new_point_count, depth - 1, True)
            min_eval = min(min_eval, eval)
        return min_eval

def find_successor_player(board, quan_count, point_count):
    successor_player = []

    for i in range(1,6):
        for direction in [-1,1]:
            new_board = copy.deepcopy(board)
            new_quan_count = copy.deepcopy(quan_count)
            new_point_count = copy.deepcopy(point_count)

            if logic_game_clone(new_board, new_quan_count, new_point_count, i, direction, True):
                successor_player.append((new_board, new_quan_count, new_point_count))
    return successor_player

def player(board, quan_count, point_count, depth):
    best_move = None
    best_value = -math.inf

    for move in find_successor_player(board, quan_count, point_count):
        new_board, new_quan_count, new_point_count = move
        move_value = minimax(new_board, new_quan_count, new_point_count, depth - 1, False)
        if move_value > best_value:
            best_value = move_value
            best_move = move
    return best_move

def find_successor_opponent(board, quan_count, point_count):
    successors = []

    for i in range(7,12):
        for direction in [-1,1]:
            new_board = copy.deepcopy(board)
            new_quan_count = copy.deepcopy(quan_count)
            new_point_count = copy.deepcopy(point_count)

            if logic_game_clone(new_board, new_quan_count, new_point_count, i, direction, False):
                successors.append((new_board, new_quan_count, new_point_count))
    return successors

def opponent(board, quan_count, point_count, depth):
    best_move = None
    best_value = math.inf
    
    for move in find_successor_opponent(board, quan_count, point_count):
        new_board, new_quan_count, new_point_count = move
        move_value = minimax(new_board, new_quan_count, new_point_count, depth - 1, True)
        if move_value < best_value:
            best_value = move_value
            best_move = move
    
    return best_move
