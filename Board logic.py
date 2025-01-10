import pygame
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
                if self.board[i][j] == 1:
                    Box_O(self.left + self.cell_size * j, self.top + self.cell_size * i, all_sprites)
                elif self.board[i][j] == 2:
                    Box_X(self.left + self.cell_size * j, self.top + self.cell_size * i, all_sprites)

                cords = (self.left + self.cell_size * j, self.top + self.cell_size * i, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, (255, 255, 255), cords, 1)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if (0 <= (x - self.left) // self.cell_size <= self.width and
                0 <= (y - self.top) // self.cell_size <= self.height):
            return (x - self.left) // self.cell_size, (y - self.top) // self.cell_size
        else:
            return None

    def on_click(self, cell_coords):
        x, y = cell_coords
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


screen = pygame.display.set_mode((1920, 1080))
board = Board(7, 6)
board.set_view(487, 135, 135)

all_sprites = pygame.sprite.Group()
back = pygame.sprite.Sprite(all_sprites)
back.image = load_image("back.jpg")
back.rect = back.image.get_rect()

back.rect.x = 0
back.rect.y = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    board.render(screen)
    pygame.display.flip()
