def tinhdiem(diagram, x, y, player):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    score = 0
    opponent = 3 - player

    for dx, dy in directions:
        # Tấn công
        line = 1
        for direction in [1, -1]:
            for i in range(1, 5):
                nx, ny = x + i * dx * direction, y + i * dy * direction
                if 0 <= nx < len(diagram[0]) and 0 <= ny < len(diagram):
                    if diagram[ny][nx] == player:
                        line += 1
                    elif diagram[ny][nx] == 0:
                        break
                    else:
                        break
                else:
                    break

        if line >= 5:
            return 100000
        elif line == 4:
            score += 10000
        elif line == 3:
            score += 100
        elif line == 2:
            score += 10

        # Phòng thủ
        opponent_count = 1
        open_ends = 0
        for direction in [-1, 1]:
            step = 1
            while step <= 3:
                nx = x + dx * direction * step
                ny = y + dy * direction * step
                if 0 <= nx < len(diagram[0]) and 0 <= ny < len(diagram):
                    if diagram[ny][nx] == opponent:
                        opponent_count += 1
                    elif diagram[ny][nx] == 0:
                        open_ends += 1
                        break
                    else:
                        break
                else:
                    break
                step += 1

        if opponent_count >= 3 and open_ends > 0:
            score += 2000

    return score
