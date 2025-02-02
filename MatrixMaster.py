import random
import numpy as np


class ModeError(BaseException):
    pass


class TricksChoiceIsWrong(BaseException):
    pass


class MatrixMaster:
    def __init__(self, field_size, mode="classic", infinite_field=False, len_of_chain=-1, relief=False):
        self.mode = mode
        if mode == "classic":
            if len_of_chain == -1:
                self.len_of_chain = 4
            else:
                self.len_of_chain = len_of_chain
        elif mode == "score":
            if len_of_chain == -1:
                self.len_of_chain = 3
            else:
                self.len_of_chain = len_of_chain
        else:
            raise ModeError("Неизвестный режим игры")
        self.infinite_field = infinite_field
        self.field_size = (field_size[1], field_size[0])
        self.field = np.full(self.field_size, "-")
        if relief:
            self.relief = self.make_relief()
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

    def scoring(self, selected_tricks):
        if self.mode != "score":
            raise ModeError("Данная функция не совместима с данными настройками игры или не имеет смысла при них")
        if not selected_tricks:
            raise TricksChoiceIsWrong("Хоть что-нибудь то выберите")
        selected_tricks = sorted(selected_tricks, key=lambda trick: (trick[0], trick[1]))
        if (len(set([i[0] for i in selected_tricks])) == 1
                and sum(map(lambda y: y[1], selected_tricks)) ==
                0.5 * (selected_tricks[0][1] + selected_tricks[-1][1]) * len(selected_tricks)
                and len(selected_tricks) - 1 == selected_tricks[-1][1] - selected_tricks[0][1]) \
            or \
                (len(set([i[1] for i in selected_tricks])) == 1
                and sum(map(lambda x: x[0], selected_tricks)) ==
                0.5 * (selected_tricks[0][0] + selected_tricks[-1][0]) * len(selected_tricks)
                and len(selected_tricks) - 1 == selected_tricks[-1][0] - selected_tricks[0][0]) \
            or \
                (sum(map(lambda x: x[0], selected_tricks)) ==
                0.5 * (selected_tricks[0][0] + selected_tricks[-1][0]) * len(selected_tricks)
                and len(selected_tricks) - 1 == abs(selected_tricks[-1][0] - selected_tricks[0][0])
                and
                sum(map(lambda y: y[1], selected_tricks)) ==
                0.5 * (selected_tricks[0][1] + selected_tricks[-1][1]) * len(selected_tricks)
                and len(selected_tricks) - 1 == abs(selected_tricks[-1][1] - selected_tricks[0][1])):

            selected_team = set([self.field[trick_coords[1]][trick_coords[0]] for trick_coords in selected_tricks])
            if len(selected_team) == 1:
                if tuple(selected_team)[0] == self.moving_now:
                    if len(selected_tricks) >= self.len_of_chain:
                        if self.moving_now == "O":
                            self.moving_now = "X"
                        else:
                            self.moving_now = "O"
                        for trick in selected_tricks:
                            x = trick[0]
                            y = trick[1] - 1
                            while y >= 0:
                                self.field[y + 1][x] = self.field[y][x]
                                y -= 1
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
        if self.mode != "classic":
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

    def del_last_row(self, old_matrix):
        if not self.infinite_field:
            raise ModeError("Данная функция не совместима с данными настройками игры или не имеет смысла при них")
        self.field = self.field[0:-1]
        self.field = np.insert(self.field, 0, ["-", "-", "-", "-", "-", "-", "-"], axis=0)
        new_matrix = old_matrix[0:-1]
        new_matrix.insert(0, [[None, False], [None, False], [None, False], [None, False], [None, False], [None, False], [None, False]])
        return new_matrix

    def make_relief(self):
        obstacles_x = []
        while len(set(obstacles_x)) < self.field_size[1] * 0.4 or len(set(obstacles_x)) > self.field_size[1] * 0.75:
            obstacles_x = random.choices(list(range(self.field_size[1])), k=round(self.field_size[1] * 0.8))
        obstacles = []
        for obstacle in obstacles_x:
            y = self.field_size[0] - 1
            while self.field[y][obstacle] != "-":
                y -= 1
            self.field[y][obstacle] = "="
            obstacles.append((obstacle, y))
        return obstacles


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
