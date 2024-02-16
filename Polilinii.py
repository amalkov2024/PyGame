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
        self.color = {-1: 'blue', 0: 'black', 1:'red', -2:'blue'}
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
                #if self.board[i][j]<=2:
                if self.board[i][j] not in self.color:
                    col=0
                else:
                    col=self.color[self.board[i][j]]
                pygame.draw.circle(
                    self.screen,
                    (col),
                    (
                        cnt_j + 1+ self.cell_size//2,
                        cnt_i + 1+ self.cell_size//2

                    ),self.cell_size//2-4,
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
                self.board[cell_coords[1]][cell_coords[0]] = -1
            elif self.board[cell_coords[1]][cell_coords[0]] == -1:
                self.board[cell_coords[1]][cell_coords[0]] = 1
            else:
                self.board[cell_coords[1]][cell_coords[0]] = 0 # если другой цвет то пометим синим


class Lines(Board):
    def __init__(self,width, height):
        super().__init__(width,height)
        self.roads=None

    def road(self, mass, stx, sty, endx, endy): # возвращает список координат пути
        ans = [(endx, endy)]
        while (stx != endx or sty != endy):
            min_mass = [mass[endx - (0 < endx <= len(mass))][endy], mass[endx + (0 <= endx < len(mass) - 1)][endy],
                                     mass[endx][endy - (0 < endy <= len(mass[0]))], mass[endx][endy + (0 <= endy < len(mass[0]) - 1)]]
            min_r=min(min_mass, key=lambda x: 10000 if x <= -1 else x)
            if min_r == mass[endx - (0 < endx < len(mass))][endy]:
                endx, endy = endx - (0 < endx < len(mass)), endy
            elif min_r == mass[endx + (0 <= endx < len(mass) - 1)][endy]:
                endx, endy = endx + (0 <= endx < len(mass) - 1), endy
            elif min_r == mass[endx][endy - (0 < endy <= len(mass[0]))]:
                endx, endy = endx, endy - (0 < endy <= len(mass[0]))
            elif min_r == mass[endx][endy + (0 <= endy < len(mass[0]) - 1)]:
                endx, endy = endx, endy + (0 <= endy < len(mass[0]) - 1)
            ans.append((endx, endy))
        return ans[::-1]

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
        if x1==x2 and y2==y1:
            return False
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

            if self.has_path(x1, y1, cell[1], cell[0]) == True:
                # есть путь. Пометить нужные клетки в массиве
                #self.board[cell[1]][cell[0]] =-2 # финишная клетка
                #self.board[x1][y1]=0 # стартовая
                self.roads = self.road(self.board,x1,y1,cell[1],cell[0])
                # обнуляем массив с найденным путем
                for x in range(len(self.board)):
                    for y in range((len(self.board[x]))):
                        if self.board[x][y]>0:
                            self.board[x][y]=0
                #print('red x1, y1',x1,y1, cell)
                #print('red self.roads',self.roads)


if __name__ == "__main__":
    # инициализация Pygame:
    board = Lines(7, 7)
    board.set_view(50, 50, 50)
    pygame.init()
    size = width, height = (board.left * 2 + board.width * board.cell_size), (
        board.top * 2 + board.height * board.cell_size
    )
    screen = pygame.display.set_mode(size)
    fps = 5
    clock = pygame.time.Clock()
    running = True
    screen.fill((0, 0, 0))
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.red_blue(event.pos)
                #board.get_click(event.pos)
                #print('board.board',board.board)
                cnt_roads = 1
        if board.roads:
            # нужно мигнуть по пути следования тоесть изменять массив board.board
            #print('YES')
            #print(board.roads)
            prev_roads=cnt_roads-1
            board.board[board.roads[prev_roads][0]][board.roads[prev_roads][1]] = 0
            board.board[board.roads[cnt_roads][0]][board.roads[cnt_roads][1]] = -1
            cnt_roads+=1
            if cnt_roads==len(board.roads):
                board.roads=None
        board.render(screen)
        clock.tick(fps)
        pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    # завершение работы:
    pygame.quit()
