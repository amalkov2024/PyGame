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


    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        self.screen = screen
        cnt_i=self.left
        for i in self.board:
            cnt_i+=self.cell_size
            cnt_j = self.top
            for j in i:
                cnt_j+=self.cell_size
                pygame.draw.rect(self.screen,('white'), (cnt_j, cnt_i, self.cell_size,self.cell_size), width=1)


if __name__ == '__main__':
    # инициализация Pygame:
    board = Board(4, 3)
    board.set_view(100, 100, 50)
   # board = Board(5, 7)
    pygame.init()
    size = width, height = (board.left*2+board.width*board.cell_size), (board.top*2+board.height*board.cell_size)
    screen = pygame.display.set_mode(size)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))

        board.render(screen)

        pygame.display.flip()
    # смена (отрисовка) кадра:

    # ожидание закрытия окна:
    while pygame.event.wait().type != pygame.QUIT:
        pass
    # завершение работы:
    pygame.quit()
