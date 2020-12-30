
MISS = "%"
HIT = "$"
EMPTY = "#"


class AwayBoard:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[EMPTY for _ in range(width)] for _ in range(height)]

    def set_hit_at(self, x, y):
        self.board[x][y] = HIT

    def set_miss_at(self, x, y):
        self.board[x][y] = MISS
