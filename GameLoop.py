import pygame
import time
from LoadTextures import *
from BoardLogic import Board
from Constants import *
from MenuLogic import *


menu = Menu()
board = Board()


ground = pygame.sprite.Sprite(ground_border)
ground.rect = pygame.Rect(0, SCREEN_SIZE[1] - menu.bottom_intend, SCREEN_SIZE[0], SCREEN_SIZE[1] - menu.bottom_intend)


prev_time = time.perf_counter()
current_time = prev_time
FPS = 100
STEP_TIME = 1./FPS
running = True

while running:
    prev_time = current_time
    current_time = time.perf_counter()
    dt = current_time - prev_time

    background.draw(screen)

    if menu.menu_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu_sprites.update(event)
                if not menu.menu_flag:
                    board.width = menu.board_width
                    board.height = menu.board_height
                    board.cell_size = menu.cell_size
                    board.top = menu.top_intend
                    board.left = menu.left_intend
                    board.mode_classic = menu.mode_classic
                    board.endless_height_flag = menu.endless_height_flag
                    board.relief_field_flag = menu.relief_field_flag
                    board.len_of_chain = menu.len_of_chain
                    board.game_flag = True
                    board.set_board()
        menu.render()

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
                game_sprites.update(event)
                score_sprites.update(event)
                pause_sprites.update(event)
                if not board.game_flag:
                    menu.menu_flag = True
                    rocks.empty()
                    falling_rocks.empty()
                    placed_boxes.empty()
                    falling_boxes.empty()
                    player_mark.empty()

        board.render(screen)

    while time.perf_counter() < (current_time + STEP_TIME):
        pass

    pygame.display.update()
