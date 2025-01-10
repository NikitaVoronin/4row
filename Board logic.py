import pygame


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
                fill = 1 if self.board[i][j] == 0 else 0
                if self.board[i][j] == 1:
                    color = (255, 0, 0)
                elif self.board[i][j] == 2:
                    color = (0, 0, 255)
                else:
                    color = (255, 255, 255)
                cords = (self.left + self.cell_size * j, self.top + self.cell_size * i, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, color, cords, fill)

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
        self.board[y][x] = self.player
        self.player = 1 if self.player == 2 else 2

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


screen = pygame.display.set_mode((500, 500))
board = Board(7, 6)
board.set_view(100, 100, 50)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
    screen.fill((0, 0, 0))
    board.render(screen)
    pygame.display.flip()
