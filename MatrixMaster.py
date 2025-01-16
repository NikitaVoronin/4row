import random
import numpy as np


class ModeError(BaseException):
    pass


class TricksChoiceIsWrong(BaseException):
    pass


class MatrixMaster:
    def __init__(self, field_size, mode="classic", infinite_field=False, len_of_chain=-1):
        self.mode = mode
        if mode == "classic":
            self.len_of_chain = len_of_chain if len_of_chain == -1 else self.len_of_chain = 4
        elif mode == "score":
            self.len_of_chain = len_of_chain if len_of_chain == -1 else self.len_of_chain = 3
        else:
            raise ModeError("Неизвестный режим игры")
        self.infinite_field = infinite_field
        self.field_size = (field_size[1], field_size[0])
        self.field = np.full(self.field_size, "-")
        self.moving_now = random.choice(["X", "O"])

    def new_trick(self, coords):
        self.field[coords[1]][coords[0]] = self.moving_now
        if self.moving_now == "O":
            self.moving_now = "X"
        else:
            self.moving_now = "O"

        if self.mode == "classic":
            winner = self.check_winner()
            if winner:
                return winner
            if self.infinite_field:
                self.check_inf_field()

    def scoring(self, selected_tricks):
        selected_tricks = sorted(selected_tricks, key=lambda trick: (trick[0], trick[1]))
        if (len(set([i[0] for i in selected_tricks])) == 1
                and sum(map(lambda y: y[1], selected_tricks)) ==
                0.5 * (selected_tricks[0][1] + selected_tricks[-1][1]) * len(selected_tricks)) \
            or \
                (len(set([i[1] for i in selected_tricks])) == 1
                and sum(map(lambda x: x[0], selected_tricks)) ==
                0.5 * (selected_tricks[0][0] + selected_tricks[-1][0]) * len(selected_tricks)) \
            or \
                (sum(map(lambda x: x[0], selected_tricks)) ==
                0.5 * (selected_tricks[0][0] + selected_tricks[-1][0]) * len(selected_tricks)
                and sum(map(lambda y: y[1], selected_tricks)) ==
                0.5 * (selected_tricks[0][1] + selected_tricks[-1][1]) * len(selected_tricks)):

            selected_team = set([self.field[trick_coords[1], trick_coords[0]]] for trick_coords in selected_tricks)
            if len(selected_team) == 1:
                if tuple(selected_team)[0] == self.moving_now:
                    if len(selected_team) >= self.len_of_chain:
                        return 100 * len(selected_tricks) ** 2
                    else:
                        raise TricksChoiceIsWrong("Ряд слишком короткий")
                else:
                    raise TricksChoiceIsWrong("Сейчас ход другой команды")
            else:
                raise TricksChoiceIsWrong("Выберете только свои фишки")
        else:
            raise TricksChoiceIsWrong("Фишки не стоят в ряд")


    def check_winner(self):
        if self.mode == "score":
            raise ModeError("Данная функция не совместима с данными настройками игры или не имеет смысла при них")
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

    def check_inf_field(self):
        pass

def compare_matrices(matrix1, matrix2):
    np_matrix1 = np.array(matrix1)
    np_matrix2 = np.array(matrix2)
    if np.array_equal(np_matrix1, np_matrix2):
        return None
    else:
        for y in range(6):
            if not np.array_equal(np_matrix1[y], np_matrix2[y]):
                for x in range(7):
                    if np_matrix1[y][x] != np_matrix2[y][x]:
                        return x, y


a = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]

b = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]

# print(compare_matrices(a, b))


mm = MatrixMaster((2, 2))
mm.scoring([(4, 3), (3, 2), (2, 1)])