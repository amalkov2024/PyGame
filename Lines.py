import pygame


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board_2 = [[0] * width for _ in range(height)]
        self.board = [[0] * width for _ in range(height)] # нет - 0; красный - 1; синий - 2
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.motion = 1

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        self.screen = screen
        cnt_i = self.left
        for i in range(len(self.board_2)):
            cnt_j = self.top
            for j in range(len(self.board_2[i])):
                pygame.draw.rect(
                    self.screen,
                    ("white"),
                    (cnt_j, cnt_i, self.cell_size, self.cell_size),
                    width=1,
                )
                self.board_2[i][j] = [
                    cnt_i,
                    cnt_j,
                    self.cell_size,
                    "black",
                ]  # координаты клеток
                cnt_j += self.cell_size
            cnt_i += self.cell_size

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mouse_pos):
        for y in range(len(self.board_2)):
            for x in range(len(self.board_2[y])):
                if self.board_2[y][x][0] <= mouse_pos[1] <= (
                    self.board_2[y][x][0] + self.board_2[y][x][2]
                ) and self.board_2[y][x][1] <= mouse_pos[0] <= (
                    self.board_2[y][x][1] + self.board_2[y][x][2]
                ):
                    return (
                        self.board_2[y][x][0],
                        self.board_2[y][x][1],
                        self.board_2[y][x][3],
                    )
        return (-1, -1, "")

    def on_click(self, cell_coords):
        if cell_coords[2] == "blue":
            self.motion = 1
            # рисуем красные кружки
            pygame.draw.circle(
                self.screen,
                ("red"),
                (
                    cell_coords[1] + self.cell_size // 2,
                    cell_coords[0] + self.cell_size // 2,
                ),
                self.cell_size // 2 - 4,

            )
            for y in range(len(self.board_2)):
                for x in range(len(self.board_2[y])):
                    if (
                        self.board_2[y][x][0] == cell_coords[0]
                        and self.board_2[y][x][1] == cell_coords[1]
                    ):
                        self.board_2[y][x][3] = "red"
                        self.board[y][x] = 1
        elif cell_coords[2] == "red":
            self.motion = 1
            # рисуем красные кружки
            pygame.draw.circle(
                self.screen,
                ("blue"),
                (
                    cell_coords[1] + self.cell_size // 2,
                    cell_coords[0] + self.cell_size // 2,
                ),
                self.cell_size // 2 - 4,

            )
            for y in range(len(self.board_2)):
                for x in range(len(self.board_2[y])):
                    if (
                        self.board_2[y][x][0] == cell_coords[0]
                        and self.board_2[y][x][1] == cell_coords[1]
                    ):
                        self.board_2[y][x][3] = "blue"
                        self.board[y][x] = -1
        elif cell_coords[2] == "black":
            self.motion = 2
            # рисуем синие кружки
            pygame.draw.circle(
                self.screen,
                ("blue"),
                (
                    cell_coords[1] + self.cell_size // 2,
                    cell_coords[0] + self.cell_size // 2,
                ),
                self.cell_size // 2 - 4,

            )

            for y in range(len(self.board_2)):
                for x in range(len(self.board_2[y])):
                    if (
                        self.board_2[y][x][0] == cell_coords[0]
                        and self.board_2[y][x][1] == cell_coords[1]
                    ):
                        self.board_2[y][x][3] = "blue"
                        self.board[y][x] = -1
        else:
            pass
        pygame.display.flip()



class Lines(Board):

    def voln(self, x, y, cur, n, m, lab):
        lab[x][y] = cur
        if y + 1 < m:
            if lab[x][y + 1] == 0 or (lab[x][y + 1] != -1 and lab[x][y + 1] > cur):
                self.voln(x, y + 1, cur + 1, n, m, lab)
        if x + 1 < n:
            if lab[x + 1][y] == 0 or (lab[x + 1][y] != -1 and lab[x + 1][y] > cur):
                self.voln(x + 1, y, cur + 1, n, m, lab)
        if x - 1 >= 0:
            if lab[x - 1][y] == 0 or (lab[x - 1][y] != -1 and lab[x - 1][y] > cur):
                self.voln(x - 1, y, cur + 1, n, m, lab)
        if y - 1 >= 0:
            if lab[x][y - 1] == 0 or (lab[x][y - 1] != -1 and lab[x][y - 1] > cur):
                self.voln(x, y - 1, cur + 1, n, m, lab)
        return lab

    def has_path(self, x1, y1, x2, y2):
        lab = self.board
        n = len(lab)
        m = len(lab[0])
        finalout = self.voln(x1, y1, 1, n, m, lab)
        if lab[x2][y2] > 0:
            return True
        else:
            return False

    def red_blue(self,mouse_pos):
        y2,x2=mouse_pos[0],mouse_pos[1]
        cnt_red = 0
        for i in self.board:
            cnt_red += i.count(1)
        if cnt_red == 0:
            self.get_click(mouse_pos)
        else:
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    if self.board[i][j] == 1:
                        x1=i
                        y1=j
            cell=self.get_cell(mouse_pos)
            if self.has_path(x1, y1, (cell[0]-self.left)//self.cell_size, (cell[1]-self.top)//self.cell_size)==True:
                pygame.draw.circle(
                    self.screen,
                    ("black"),
                    (
                        y1 * self.cell_size + self.left + self.cell_size // 2,
                        x1*self.cell_size+self.top + self.cell_size // 2,
                    ),
                    self.cell_size // 2 - 4,

                )
                # не доделал
                for y in range(len(self.board_2)):
                    for x in range(len(self.board_2[y])):
                        if (
                                self.board_2[y][x][0] == cell[0]
                                and self.board_2[y][x][1] == cell[1]
                        ):
                            self.board_2[y][x][3] = "black"
                            self.board[y][x] = 0


                pygame.draw.circle(
                    self.screen,
                    ("blue"),
                    (
                        cell[1] + self.cell_size // 2,
                        cell[0] + self.cell_size // 2,

                    ),
                    self.cell_size // 2 - 4,

                )
            ''' for y in range(len(self.board_2)):
                    for x in range(len(self.board_2[y])):
                        if (
                                self.board_2[y][x][0] == cell_coords[0]
                                and self.board_2[y][x][1] == cell_coords[1]
                        ):
                            self.board_2[y][x][3] = "black"
                            self.board[y][x] = -1
'''





if __name__ == "__main__":
    # инициализация Pygame:
    board = Lines(5, 5)
    board.set_view(50, 50, 50)
    pygame.init()
    size = width, height = (board.left * 2 + board.width * board.cell_size), (
        board.top * 2 + board.height * board.cell_size
    )
    screen = pygame.display.set_mode(size)
    running = True
    screen.fill((0, 0, 0))
    board.render(screen)
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.red_blue(event.pos)
                print(board.board)
        pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    # завершение работы:
    pygame.quit()
