def sapxepnuocdi(diagram, possible_moves, player, max_moves=20, defensive_weight=1.5, pattern_weight=3.0):

    if not possible_moves:
        return []
    
    from tinhdiem import tinhdiem
    from naphinhco import naphinhco
    
    opponent = 3 - player
    scored_moves = []
    
    for x, y in possible_moves:
        offensive = tinhdiem(diagram, x, y, player)
        defensive = tinhdiem(diagram, x, y, opponent)
        pattern_block = naphinhco(diagram, x, y, player)
        
        total_score = offensive + defensive * defensive_weight + pattern_block * pattern_weight
        scored_moves.append((total_score, x, y))
    
    # Sắp xếp theo điểm giảm dần
    scored_moves.sort(reverse=True, key=lambda item: item[0])
    
    return [(x, y) for (score, x, y) in scored_moves[:max_moves]]