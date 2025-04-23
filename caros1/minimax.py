from sapxepnuocdi import sapxepnuocdi
from tinhdiem import tinhdiem

def minimax(diagram, depth, alpha, beta, is_maximizing, player):
 
    if depth == 0 or is_terminal(diagram):
        return evaluate(diagram, player), None
    
    possible_moves = get_possible_moves(diagram)
    possible_moves = sapxepnuocdi(diagram, get_possible_moves(diagram), player)
    
    best_move = None
    
    if is_maximizing:
        max_eval = float('-inf')
        for x, y in possible_moves:
            # Make the move
            diagram[y][x] = player
            
            # Recursive call    
            current_eval, _ = minimax(diagram, depth-1, alpha, beta, False, player)
            
            # Undo the move
            diagram[y][x] = 0
            
            # Update best evaluation
            if current_eval > max_eval:
                max_eval = current_eval
                best_move = (x, y)
            
            # Alpha-beta pruning
            alpha = max(alpha, current_eval)
            if beta <= alpha:
                break
                
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for x, y in possible_moves:
            # Make the move
            diagram[y][x] = 3 - player  # opponent
            
            # Recursive call
            current_eval, _ = minimax(diagram, depth-1, alpha, beta, True, player)
            
            # Undo the move
            diagram[y][x] = 0
            
            # Update best evaluation
            if current_eval < min_eval:
                min_eval = current_eval
                best_move = (x, y)
            
            # Alpha-beta pruning
            beta = min(beta, current_eval)
            if beta <= alpha:
                break
                
        return min_eval, best_move

def is_terminal(diagram):
    """Kiểm tra kết thúc game nhanh (chỉ quanh các quân đã đánh)"""
    checked = set()
    for y in range(len(diagram)):
        for x in range(len(diagram[0])):
            if diagram[y][x] != 0 and (x, y) not in checked:
                # Kiểm tra 4 hướng
                for dx, dy in [(1,0), (0,1), (1,1), (1,-1)]:
                    count = 1
                    for step in [1, -1]:
                        nx, ny = x + dx*step, y + dy*step
                        while 0 <= nx < len(diagram[0]) and 0 <= ny < len(diagram):
                            if diagram[ny][nx] == diagram[y][x]:
                                count += 1
                                nx += dx*step
                                ny += dy*step
                            else:
                                break
                    if count >= 5:
                        return True
                checked.add((x, y))
    return False

def evaluate(diagram, player):
    """Evaluate the board state"""
    score = 0
    opponent = 3 - player
    
    # Evaluate all positions
    for y in range(len(diagram)):
        for x in range(len(diagram[0])):
            if diagram[y][x] == player:
                score += tinhdiem(diagram, x, y, player)
            elif diagram[y][x] == opponent:
                score -= tinhdiem(diagram, x, y, opponent)
    
    return score

def get_possible_moves(diagram, expand_range=2):
    """Lấy các ô trống xung quanh nước đã đánh (phạm vi expand_range)"""
    moves = set()
    for y in range(len(diagram)):
        for x in range(len(diagram[0])):
            if diagram[y][x] != 0:
                # Quét các ô lân cận
                for dy in range(-expand_range, expand_range + 1):
                    for dx in range(-expand_range, expand_range + 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < len(diagram[0]) and 0 <= ny < len(diagram):
                            if diagram[ny][nx] == 0:
                                moves.add((nx, ny))
    return list(moves)