import pygame


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.color = ['black', 'red', 'blue']
    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        self.screen = screen
        cnt_i = self.left
        for i in range(len(self.board)):
            cnt_j = self.top
            for j in range(len(self.board[i])):
                pygame.draw.rect(
                    self.screen,
                    ("white"),
                    (cnt_j, cnt_i, self.cell_size, self.cell_size),
                    width=1,
                )
                # рисуем цветом
                pygame.draw.rect(
                    self.screen,
                    (self.color[self.board[i][j]]),
                    (
                        cnt_j + 1,
                        cnt_i + 1,
                        self.cell_size - 2,
                        self.cell_size - 2,
                    ),
                )
                cnt_j += self.cell_size
            cnt_i += self.cell_size

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mouse_pos):
        x = (
            (mouse_pos[0] - self.left) // self.cell_size
            + ((mouse_pos[0] - self.left) % self.cell_size != 0)
            - 1
        )
        y = (
            (mouse_pos[1] - self.top) // self.cell_size
            + ((mouse_pos[1] - self.top) % self.cell_size != 0)
            - 1
        )
        if 0 <= x < len(self.board[0]) and 0 <= y < len(self.board):
            return (x, y)
        return None

    def on_click(self, cell_coords=None):
        if cell_coords:
            if self.board[cell_coords[1]][cell_coords[0]] == 0:
                self.board[cell_coords[1]][cell_coords[0]] = 1
            elif self.board[cell_coords[1]][cell_coords[0]] == 1:
                self.board[cell_coords[1]][cell_coords[0]] = 2
            else:
                self.board[cell_coords[1]][cell_coords[0]] = 0


if __name__ == "__main__":
    # инициализация Pygame:
    board = Board(5, 7)
    board.set_view(100, 100, 50)
    pygame.init()
    size = width, height = (board.left * 2 + board.width * board.cell_size), (
        board.top * 2 + board.height * board.cell_size
    )
    screen = pygame.display.set_mode(size)
    running = True
    screen.fill((0, 0, 0))
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        board.render(screen)
        pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    # завершение работы:
    pygame.quit()
