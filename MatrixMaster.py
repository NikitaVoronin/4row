# Файл, собирающий всю работу с матрицами и логикой
# В течении игры поле необходимо постоянно контролировать, следить, не собраны ли ы ряд фишки, удалять их, передвигать и пр.
# Игровое поле хранится в матрице в экземпляре класса MatrixMaster и создается при инициализации
# После каждого хода игрока игра обращается к экземпляру и передает ему изменение, а экземпляр выносит какой-либо вердикт


# Импорт библиотек
import random
import numpy as np

# Класс ошибки режима, вызывается когда при данном режиме игры невозможно совершить над полем те или иные махинации
class ModeError(BaseException):
    pass


# Класс ошибки для режима на очки, возвращается когда пользователем некорректно выбраны фишки
class TricksChoiceIsWrong(BaseException):
    pass


# Главный класс с матрицей и инструментами работы с ней
class MatrixMaster:

    # В начале игры создается экземпляр, ему передаются размер поля, режим игры, длина цепи и необходимы ли рельеф и бесконечное поле
    def __init__(self, field_size, mode="classic", infinite_field=False, len_of_chain=-1, relief=False):
        self.mode = mode
        self.infinite_field = infinite_field
        self.field_size = (field_size[1], field_size[0])
        self.field = np.full(self.field_size, "-")      # Создание матрицы и заполнение ее "пустотой"
        self.moving_now = random.choice(["X", "O"])             # Кто ходит первым, выбирается случайно

        # Для разных режимов минимальная длина цепи отличается
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

        # Генерация рельефа при необходимости
        if relief:
            self.relief = self.make_relief()

    # Вызывается, когда на поле появилась новая фишка, принимает ее координаты
    def new_trick(self, coords):
        self.field[coords[1]][coords[0]] = self.moving_now      # Добавление в матрицу
        # Смена хода
        if self.moving_now == "O":
            self.moving_now = "X"
        else:
            self.moving_now = "O"

        # Если мы играем в классический режим, после каждой новой фишки необходимо проверять, не собрался ли ряд
        if self.mode == "classic":
            winner = self.check_winner()
            if winner:
                return winner

    # Функция для режима игры на очки, вызывается когда игрок выбрал фишки и хочет их "обналичить"
    def scoring(self, selected_tricks):

        # Базовые проверки
        if self.mode != "score":
            raise ModeError("Данная функция не совместима с данными настройками игры или не имеет смысла при них")
        if not selected_tricks:
            raise TricksChoiceIsWrong("Хоть что-нибудь то выберите")

        # Сортировка переданных координат
        selected_tricks = sorted(selected_tricks, key=lambda trick: (trick[0], trick[1]))

        # Проверяется, стоят ли фишки в ряд по вертикали/горизонтали/диагонали
        # Алгоритм основан на вычислении суммы арифметической прогрессии
        # Если сумма абсцисс/ординат равна сумме арифметической прогрессии по первому и последнему члену списка
        # и при этом разница между ними равна длине списка, то числа составляют арифметическую прогрессию, т.е идут
        # по порядку. По диагонали и абсциссы и ординаты должны составлять прогрессию, по горизонтали/вертикали - только
        # абсциссы или ординаты, остальные должны быть одинаковы
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

            # Проверка, что выбраны только клетки с фишками ходящего сейчас игрока и ряд достаточно длинный
            selected_team = set([self.field[trick_coords[1]][trick_coords[0]] for trick_coords in selected_tricks])
            if len(selected_team) == 1:
                if tuple(selected_team)[0] == self.moving_now:
                    if len(selected_tricks) >= self.len_of_chain:

                        # Смена ходящего игрока
                        if self.moving_now == "O":
                            self.moving_now = "X"
                        else:
                            self.moving_now = "O"

                        # Передвижение всех вышестоящих фишек вниз
                        for trick in selected_tricks:
                            x = trick[0]
                            y = trick[1] - 1
                            while y >= 0:
                                self.field[y + 1][x] = self.field[y][x]
                                y -= 1

                        # Если все звезды сошлись, возвращаем количество очков
                        return 100 * len(selected_tricks) ** 2

                    else:
                        raise TricksChoiceIsWrong("Ряд слишком короткий")
                else:
                    raise TricksChoiceIsWrong("Сейчас ход другой команды")
            else:
                raise TricksChoiceIsWrong("Выберете только свои фишки")
        else:
            raise TricksChoiceIsWrong("Фишки не стоят в ряд")

    # Функция для классического режима, вызывается после нового хода, проверяет, есть ли победитель
    def check_winner(self):
        # Стандартная проверка
        if self.mode != "classic":
            raise ModeError("Данная функция не совместима с данными настройками игры или не имеет смысла при них")

        # Берем строки и проверяем, есть ли в каждой строке нужное количество символов в ряд
        for y in range(self.field.shape[0]):
            row_str = "".join(self.field[y, :])
            if self.len_of_chain * "O" in row_str:
                position = row_str.find(self.len_of_chain * "O")
                return "nulls win", [(x, y) for x in range (position, position + self.len_of_chain)]
            elif self.len_of_chain * "X" in row_str:
                position = row_str.find(self.len_of_chain * "X")
                return "crosses win", [(x, y) for x in range (position, position + self.len_of_chain)]

        # Аналогично со строками
        for x in range(self.field.shape[1]):
            row_str = "".join(self.field[:, x])
            if self.len_of_chain * "O" in row_str:
                position = row_str.find(self.len_of_chain * "O")
                return "nulls win", [(x, y) for y in range (position, position + self.len_of_chain)]
            elif self.len_of_chain * "X" in row_str:
                position = row_str.find(self.len_of_chain * "X")
                return "crosses win", [(x, y) for y in range(position, position + self.len_of_chain)]

        # Проверяем диагонали слева направо сверху вниз, причем не проверяем углы, так как они все равно не могут вместить ряд
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

        # Numpy не возвращает диагонали справа налево, потому вначале отзеркаливаем поле,
        # проводим те же операции и отзеркаливаем результат обратно
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

    # Функция для режима бесконечного поля, по вызову удаляет нижний ряд и сдвигает вниз остальные,
    # возвращает поле в требуемом формате
    def del_last_row(self, old_matrix):
        if not self.infinite_field:
            raise ModeError("Данная функция не совместима с данными настройками игры или не имеет смысла при них")
        self.field = self.field[0:-1]
        self.field = np.insert(self.field, 0, ["-", "-", "-", "-", "-", "-", "-"], axis=0)
        new_matrix = old_matrix[0:-1]
        new_matrix.insert(0, [[None, False], [None, False], [None, False], [None, False], [None, False], [None, False], [None, False]])
        return new_matrix

    # Функция отрисовки рельефа
    def make_relief(self):

        # Рисуем рельеф пока он получится естественным, то есть не слишком плоским и не слишком крутым
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


# Функция сделанная под заказ Ивана, сравнивает две матрицы и возвращает координаты отличающейся ячейки, если таковая имеется
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
