import pygame
import time
from LoadTextures import *
from Boxes import *


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.player = 1

        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                cords = (self.left + self.cell_size * j, self.top + self.cell_size * i, self.cell_size, self.cell_size)
                if self.board[i][j] != 0 and len(falling_boxes.sprites()) == 0:
                    if self.board[i][j] == 1:
                        BoxO(cords[0], cords[1], placed_boxes)
                    elif self.board[i][j] == 2:
                        BoxX(cords[0], cords[1], placed_boxes)

                pygame.draw.rect(screen, (255, 255, 255), cords, 1)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if (0 <= (x - self.left) // self.cell_size <= self.width and
                0 <= (y - self.top) // self.cell_size <= self.height):
            return (x - self.left) // self.cell_size, (y - self.top) // self.cell_size
        else:
            return None

    def on_click(self, cell_coords):
        if cell_coords is None or cell_coords[0] > 6 or cell_coords[1] > 5:
            return
        x, y = cell_coords

        if self.board[y][x] == 0:
            if self.player == 1:
                BoxO(self.left + self.cell_size * x, self.top + self.cell_size * y, falling_boxes)
            elif self.player == 2:
                BoxX(self.left + self.cell_size * x, self.top + self.cell_size * y, falling_boxes)

        while self.board[y][x] == 0:
            if y == 5 or self.board[y + 1][x] != 0:
                break
            else:
                y += 1

        if self.board[y][x] == 0:
            self.board[y][x] = self.player
            self.player = 1 if self.player == 2 else 2

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
board = Board(7, 6)
board.set_view(487, 180, 135)

placed_boxes = pygame.sprite.Group()
background = pygame.sprite.Group()
ground_border = pygame.sprite.Group()
falling_boxes = pygame.sprite.Group()

back = pygame.sprite.Sprite(background)
back.image = load_image("Background.jpg")
back.rect = back.image.get_rect()
back.rect.x = 0
back.rect.y = 0


ground = pygame.sprite.Sprite(ground_border)
ground.rect = pygame.Rect(board.left, board.top + board.cell_size * board.height,
                          board.left + board.cell_size * board.width, board.top + board.cell_size * board.height)

prev_time = time.perf_counter()
current_time = prev_time
FPS = 60
STEP_TIME = 1./FPS
running = True

while running:
    prev_time = current_time
    current_time = time.perf_counter()
    dt = current_time - prev_time

    while time.perf_counter() < (current_time + STEP_TIME):
        pass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
    background.draw(screen)
    falling_boxes.draw(screen)
    falling_boxes.update(None, ground_border, placed_boxes)
    placed_boxes.draw(screen)
    board.render(screen)
    pygame.display.update()
