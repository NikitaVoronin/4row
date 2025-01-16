import pygame
from Boxes import *
from Constants import *
from MatrixMaster import *

matrix_master = MatrixMaster((FIELD_WIDTH, FIELD_HEIGHT))


class Board:
    def __init__(self, width, height, left, top, cell_size):
        self.width = width
        self.height = height
        self.board = [[[None, False], [None, False], [None, False], [None, False], [None, False], [None, False], [None, False]],
                      [[None, False], [None, False], [None, False], [None, False], [None, False], [None, False], [None, False]],
                      [[None, False], [None, False], [None, False], [None, False], [None, False], [None, False], [None, False]],
                      [[None, False], [None, False], [None, False], [None, False], [None, False], [None, False], [None, False]],
                      [[None, False], [None, False], [None, False], [None, False], [None, False], [None, False], [None, False]],
                      [[None, False], [None, False], [None, False], [None, False], [None, False], [None, False], [None, False]]]

        self.player = True
        self.result = None

        self.left = left
        self.top = top
        self.cell_size = cell_size

        BoxX(self.left // 4, self.top // 4, False, player_mark)

    def render(self, screen):
        background.draw(screen)
        falling_boxes.draw(screen)
        player_mark.draw(screen)

        for i in range(self.height):
            for j in range(self.width):
                cords = (self.left + self.cell_size * j, self.top + self.cell_size * i, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, (255, 255, 255), cords, 1)

                if self.board[i][j][0] is not None:
                    if (falling_boxes.sprites() and falling_boxes.sprites()[0].rect.x == cords[0] and
                            self.board[i - 1][j][0] is None):
                        continue
                    if self.board[i][j][0] is False:
                        BoxO(cords[0], cords[1], self.board[i][j][1], placed_boxes)
                    elif self.board[i][j][0] is True:
                        BoxX(cords[0], cords[1], self.board[i][j][1], placed_boxes)

        placed_boxes.draw(screen)
        falling_boxes.update(None, ground_border, placed_boxes)
        placed_boxes.empty()

        if self.result:
            for cell_cord in self.result[1]:
                rect_cords = (self.left + self.cell_size * cell_cord[0], self.top + self.cell_size * cell_cord[1],
                              self.cell_size, self.cell_size)
                pygame.draw.rect(screen, (255, 255, 75), rect_cords, 10)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if (0 <= (x - self.left) // self.cell_size <= self.width and
                0 <= (y - self.top) // self.cell_size <= self.height):
            return (x - self.left) // self.cell_size, (y - self.top) // self.cell_size
        else:
            return None

    def on_click(self, cell_coords):
        if cell_coords is None or cell_coords[0] > FIELD_WIDTH - 1 or cell_coords[1] > FIELD_HEIGHT - 1:
            return
        x, y = cell_coords

        if self.board[y][x][0] is None:
            self.spawn_new_box(x, y)

        elif self.board[y][x][0] == self.player:
            if self.select_box(x, y):
                self.player = not self.player

        self.player = not self.player
        player_mark.empty()
        if self.player:
            BoxX(self.left // 3, self.top // 3, False, player_mark)
        else:
            BoxO(self.left // 3, self.top // 3, False, player_mark)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def spawn_new_box(self, x, y):
        if self.player:
            BoxX(self.left + self.cell_size * x, self.top + self.cell_size * y, self.board[y][x][1], falling_boxes)
        else:
            BoxO(self.left + self.cell_size * x, self.top + self.cell_size * y, self.board[y][x][1], falling_boxes)

        if len(falling_boxes.sprites()) > 1:
            falling_boxes.sprites()[0].kill()

        while self.board[y][x][0] is None:
            if y == self.height - 1 or self.board[y + 1][x][0] is not None:
                break
            else:
                y += 1

        self.board[y][x][0] = self.player
        self.result = matrix_master.new_trick((x, y))

    def select_box(self, x, y):
        self.board[y][x][1] = not self.board[y][x][1]
        return True
