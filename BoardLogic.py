import pygame
from Boxes import *
from Constants import *
from MatrixMaster import *
from MenuLogic import *


class Board:
    def __init__(self, width, height, left, top, cell_size):
        self.width = width
        self.height = height

        self.winner = None

        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        falling_boxes.draw(screen)
        player_mark.draw(screen)

        for i in range(self.height):
            for j in range(self.width):
                cords = (self.left + self.cell_size * j, self.top + self.cell_size * i, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, (255, 255, 255), cords, 1)

        falling_boxes.update(ground_border, placed_boxes)
        placed_boxes.draw(screen)

        if self.winner:
            for cell_cord in self.winner[1]:
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
        if cell_coords is None or cell_coords[0] > self.width - 1 or cell_coords[1] > self.height - 1:
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
            BoxX(self.left // 3, self.top // 3, self.cell_size, False, player_mark)
        else:
            BoxO(self.left // 3, self.top // 3, self.cell_size, False, player_mark)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def spawn_new_box(self, x, y):
        if self.player:
            BoxX(self.left + self.cell_size * x, self.top + self.cell_size * y, self.cell_size, self.board[y][x][1], falling_boxes)
        else:
            BoxO(self.left + self.cell_size * x, self.top + self.cell_size * y, self.cell_size, self.board[y][x][1], falling_boxes)

        # if len(falling_boxes.sprites()) > 1:
        #     falling_boxes.sprites()[0].kill()

        while self.board[y][x][0] is None:
            if y == self.height - 1 or self.board[y + 1][x][0] is not None:
                break
            else:
                y += 1

        self.board[y][x][0] = self.player
        self.winner = self.matrix_master.new_trick((x, y))

    def select_box(self, x, y):
        self.board[y][x][1] = not self.board[y][x][1]
        return True

    def set_board(self, board):
        self.board = board

        self.matrix_master = MatrixMaster((self.width, self.height))

        if self.matrix_master.moving_now == 'X':
            self.player = True
            BoxX(self.left // 4, self.top // 4, self.cell_size, False, player_mark)
        else:
            self.player = False
            BoxO(self.left // 4, self.top // 4, self.cell_size, False, player_mark)

