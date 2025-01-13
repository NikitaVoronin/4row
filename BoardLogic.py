import pygame
from Boxes import *
from Constants import *


class Board:
    def __init__(self, width, height, left, top, cell_size):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.player = 1

        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        background.draw(screen)
        falling_boxes.draw(screen)

        for i in range(self.height):
            for j in range(self.width):
                cords = (self.left + self.cell_size * j, self.top + self.cell_size * i, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, (255, 255, 255), cords, 1)

                if self.board[i][j] != 0:
                    if (falling_boxes.sprites() and falling_boxes.sprites()[0].rect.x == cords[0] and
                            self.board[i - 1][j] == 0):
                        continue
                    if self.board[i][j] == 1:
                        BoxO(cords[0], cords[1], placed_boxes)
                    elif self.board[i][j] == 2:
                        BoxX(cords[0], cords[1], placed_boxes)

        placed_boxes.draw(screen)
        falling_boxes.update(None, ground_border, placed_boxes)
        placed_boxes.empty()

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

        if self.board[y][x] == 0:
            if self.player == 1:
                BoxO(self.left + self.cell_size * x, self.top + self.cell_size * y, falling_boxes)
            elif self.player == 2:
                BoxX(self.left + self.cell_size * x, self.top + self.cell_size * y, falling_boxes)

        if len(falling_boxes.sprites()) > 1:
            falling_boxes.sprites()[0].kill()

        while self.board[y][x] == 0:
            if y == self.height - 1 or self.board[y + 1][x] != 0:
                break
            else:
                y += 1

        if self.board[y][x] == 0:
            self.board[y][x] = self.player
            self.player = 1 if self.player == 2 else 2

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)
