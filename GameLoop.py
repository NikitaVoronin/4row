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
                board.width = menu.board_width
                board.height = menu.board_height
                board.cell_size = menu.cell_size
                board.top = menu.top_intend
                board.left = menu.left_intend
                board.mode_classic = menu.mode_classic
                board.endless_height_flag = menu.endless_height_flag
                board.relief_field_flag = menu.relief_field_flag
                board.len_of_chain = menu.len_of_chain
                if not menu.menu_flag:
                    board.set_board(menu.create_board())
        menu.render()

    else:
        menu_sprites.empty()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
                game_sprites.update(event)
                if (not board.mode_classic and board.get_cell(event.pos) and
                        board.board[board.get_cell(event.pos)[1]][board.get_cell(event.pos)[0]][0] == board.player):
                    board.select_box(board.get_cell(event.pos)[0], board.get_cell(event.pos)[1])
                    board.selected_boxes.append((board.get_cell(event.pos)[0], board.get_cell(event.pos)[1]))

        board.render(screen)
        if board.winner:
            font = pygame.font.Font('chinese.stxinwei.ttf', 72)
            text = font.render(board.winner[0].upper(), True, (255, 255, 255))
            screen.blit(text, (menu.top_intend, menu.left_intend))

    while time.perf_counter() < (current_time + STEP_TIME):
        pass

    pygame.display.update()
