import random
import numpy as np


class MatrixMaster:
    def __init__(self, field_size, len_of_chain=4):
        self.field_size = (field_size[1], field_size[0])
        self.len_of_chain = len_of_chain
        self.field = np.full(self.field_size, "-")
        self.moving_now = random.choice(["X", "O"])

    def new_trick(self, coords):
        self.field[coords[1]][coords[0]] = self.moving_now
        if self.moving_now == "O":
            self.moving_now = "X"
        else:
            self.moving_now = "O"
        return self.check_winner()

    def check_winner(self):
        for y in range(self.field.shape[0]):
            row_str = "".join(self.field[y, :])
            if self.len_of_chain * "O" in row_str:
                position = row_str.find(self.len_of_chain * "O")
                return "nulls win", [(x, y) for x in range (position, position + self.len_of_chain)]
            elif self.len_of_chain * "X" in row_str:
                position = row_str.find(self.len_of_chain * "X")
                return "crosses win", [(x, y) for x in range (position, position + self.len_of_chain)]

        for x in range(self.field.shape[1]):
            row_str = "".join(self.field[:, x])
            if self.len_of_chain * "O" in row_str:
                position = row_str.find(self.len_of_chain * "O")
                return "nulls win", [(x, y) for y in range (position, position + self.len_of_chain)]
            elif self.len_of_chain * "X" in row_str:
                position = row_str.find(self.len_of_chain * "X")
                return "crosses win", [(x, y) for y in range(position, position + self.len_of_chain)]

        for d1 in range(4 - self.field.shape[0], self.field.shape[1] - 3):
            row_str = "".join(self.field.diagonal(d1))
            if self.len_of_chain * "O" in row_str:
                position = row_str.find(self.len_of_chain * "O")
                if d1 >= 0:
                    return "nulls win", [(n + d1, n) for n in range(position, position + self.len_of_chain)]
                else:
                    return "nulls win", [(n, n - d1) for n in range(position, position + self.len_of_chain)]
            elif self.len_of_chain * "X" in row_str:
                position = row_str.find(self.len_of_chain * "X")
                if d1 >= 0:
                    return "crosses win", [(n + d1, n) for n in range(position, position + self.len_of_chain)]
                else:
                    return "crosses win", [(n, n - d1) for n in range(position, position + self.len_of_chain)]

        for d2 in range(4 - self.field.shape[0], self.field.shape[1] - 3):
            row_str = "".join(np.fliplr(self.field).diagonal(d2))
            if self.len_of_chain * "O" in row_str:
                position = row_str.find(self.len_of_chain * "O")
                if d2 >= 0:
                    return "nulls win", [(self.field_size[0] - n + d2, n) for n in range(position, position + self.len_of_chain)]
                else:
                    return "nulls win", [(self.field_size[0] - n, n - d2) for n in range(position, position + self.len_of_chain)]
            elif self.len_of_chain * "X" in row_str:
                position = row_str.find(self.len_of_chain * "X")
                if d2 >= 0:
                    return "crosses win", [(self.field_size[0] - n - d2, n) for n in range(position, position + self.len_of_chain)]
                else:
                    return "crosses win", [(self.field_size[0] - n, n - d2) for n in range(position, position + self.len_of_chain)]
