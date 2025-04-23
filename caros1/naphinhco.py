def naphinhco(diagram, x, y, player):
    patterns = {
        'five': ([(0,1),(0,2),(0,3),(0,4)], 100000),
        'open_four': ([(-1,0),(1,0),(2,0),(3,0)], 10000),
        'block_three': ([(0,-1),(0,0),(0,1)], 3000),  # từ phiên bản 1
    }

    score = 0
    opponent = 3 - player
    directions = [(1,0), (0,1), (1,1), (1,-1)]

    for dx, dy in directions:
        for name, (pattern, value) in patterns.items():
            matched = True
            for px, py in pattern:
                nx = x + px * dx
                ny = y + py * dy
                if not (0 <= nx < len(diagram[0]) and 0 <= ny < len(diagram)):
                    matched = False
                    break

                if name == 'block_three':
                    if diagram[ny][nx] != opponent:
                        matched = False
                        break
                else:
                    if diagram[ny][nx] != player:
                        matched = False
                        break

            if matched:
                score += value

    return score
