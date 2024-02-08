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
        for i in range(len(self.board)):
            cnt_j = self.top
            for j in range(len(self.board[i])):
                pygame.draw.rect(self.screen,('white'), (cnt_j, cnt_i, self.cell_size, self.cell_size), width=1)
                self.board[i][j] = (cnt_i, cnt_j, self.cell_size) # координаты клеток
                cnt_j += self.cell_size
            cnt_i += self.cell_size

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mouse_pos):
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if  (self.board[y][x][0]<=mouse_pos[0]<=(self.board[y][x][0]+self.board[y][x][2]) and
                        self.board[y][x][1]<=mouse_pos[1]<=(self.board[y][x][1]+self.board[y][x][2])):
                    return (self.board[y][x][0], self.board[y][x][1])


    def on_click(self, cell_coords):
        pygame.draw.rect(self.screen, ('red'), (cell_coords[0], cell_coords[1], self.cell_size, self.cell_size), width=1)
        pygame.display.flip()


if __name__ == '__main__':
    # инициализация Pygame:
    board = Board(4, 3)
    board.set_view(100, 100, 50)
    print(board.board)
    #board = Board(5, 7)
    pygame.init()
    size = width, height = (board.left*2+board.width*board.cell_size), (board.top*2+board.height*board.cell_size)
    screen = pygame.display.set_mode(size)
    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                #x_y = event.pos  # координаты нажатия мышки
                board.get_click(event.pos)

        board.render(screen)
        pygame.display.flip()
    # смена (отрисовка) кадра:

    # ожидание закрытия окна:
    while pygame.event.wait().type != pygame.QUIT:
        pass
    # завершение работы:
    pygame.quit()
