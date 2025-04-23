import pygame
from caro import caro
from minimax import minimax

class CaroAI(caro):
    def __init__(self, r, c, show=True):
        super().__init__(r, c, show)
    
    def bot_move(self):
        if self.result == 0 and not self.xo and self.vsbot:
            diagram_copy = [row.copy() for row in self.diagram]

            # Tìm nước đi tối ưu cho máy sử dụng Minimax
            _, best_move = minimax(diagram_copy, depth=3, alpha=float('-inf'),
                                beta=float('inf'), is_maximizing=True, player=2)

            if best_move:
                x, y = best_move
                self.botmove(x, y)

                # Kiểm tra kết quả sau khi máy đi
                if self.result == 2:  # Máy thắng
                    return 
if __name__ == "__main__":
    cr = CaroAI(18, 18)
    cr.vsbot = True
    while cr.runned():
        cr.bot_move()