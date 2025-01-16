import pygame
import time
from LoadTextures import *
from BoardLogic import Board
from Constants import *


board = Board(FIELD_WIDTH, FIELD_HEIGHT, LEFT_INDENT, TOP_INDENT, CELL_SIZE)


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
FPS = 100
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

    board.render(screen)
    if board.result:
        font = pygame.font.Font(None, 72)
        text = font.render(board.result[0], False, (255, 255, 255))
        screen.blit(text, (TOP_INDENT, LEFT_INDENT))

    pygame.display.update()
