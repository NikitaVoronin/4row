class MatrixMaster:
    def __init__(self):
        self.now_move = True
        self.game_matrix = [
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None],
        ]
    def new_trick(self, coords):
        self.game_matrix[coords[0]][coords[1]] = self.now_move
        self.now_move = not self.now_move
        print(self.check_winner())

    def check_winner(self):
        for i in self.game_matrix:
            candidate = [None, 0]
            for j in i:
                if j is not None:
                    if candidate[0] == j:
                        candidate[1] += 1
                        if candidate[1] == 4:
                            return candidate[0]
                    else:
                        candidate[0] = j
                        candidate[1] = 0
                else:
                    candidate[0] = None
                    candidate[1] = 0
        return None

my_matrix = MatrixMaster()
my_matrix.new_trick((2, 1))


