import copy
import pickle
import pygame
import random
import sys

pygame.init()
clock = pygame.time.Clock()
FILES = {1: "image/Ball_1.png", 2: "image/Ball_2.png", 3: "image/Ball_3.png", 4: "image/Ball_4.png",
         5: "image/Ball_5.png", 6: "image/Ball_6.png", 7: "image/Ball_7.png"}
RANG_LEVEL = 500


class Ring(pygame.sprite.Sprite):
    def __init__(self, image, row, column):
        super().__init__()
        self.long_image = image
        self.image = pygame.Surface([96, 96], pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(column * 64 + 32, row * 64 + 32))
        self.counter = 0

    def update(self):
        self.counter += 1
        if self.counter < 3:
            self.image = pygame.Surface([96, 96], pygame.SRCALPHA)
            self.image.blit(self.long_image, (0, 0), (0, 0, 96, 96))
        elif self.counter < 6:
            self.image = pygame.Surface([96, 96], pygame.SRCALPHA)
            self.image.blit(self.long_image, (0, 0), (96, 0, 96, 96))
        elif self.counter < 9:
            self.image = pygame.Surface([96, 96], pygame.SRCALPHA)
            self.image.blit(self.long_image, (0, 0), (192, 0, 96, 96))
        elif self.counter < 12:
            self.image = pygame.Surface([96, 96], pygame.SRCALPHA)
            self.image.blit(self.long_image, (0, 0), (288, 0, 96, 96))
        elif self.counter == 12:
            self.image = pygame.Surface([96, 96], pygame.SRCALPHA)
            self.image.blit(self.long_image, (0, 0), (384, 0, 96, 96))
        else:
            ring_activ = False


class Ball(pygame.sprite.Sprite):
    vibor = False
    value = 0
    level = 0
    shot = 0

    def __init__(self, coor, color, rost=7):
        super().__init__()
        self.coor = coor
        self.color = color
        self.etalon_image = pygame.image.load(FILES[color]).convert_alpha()
        self.rost = rost
        self.image = pygame.transform.scale(self.etalon_image, (self.rost, self.rost))
        self.rect = self.image.get_rect(center=(self.coor[1] * 64 + 32, self.coor[0] * 64 + 32))
        self.push = False
        self.puls = -1
        self.scale = 47
        self.vector = []

    def update(self):
        if self.rost <= 47:  # появляется новый шарик
            self.image = pygame.transform.scale(self.etalon_image, (self.rost, self.rost))
            self.rect = self.image.get_rect(center=(self.coor[1] * 64 + 32, self.coor[0] * 64 + 32))
            self.rost += 4
        if self.push == True and self.vector == []:  # если выбран шарик заставляем его пульсировать
            self.scale = self.scale + self.puls
            if self.scale <= 42:
                self.puls = 1
            elif self.scale >= 52:
                self.puls = -1
            self.image = pygame.transform.scale(self.etalon_image, (self.scale, self.scale))
            self.rect = self.image.get_rect(center=(self.coor[1] * 64 + 32, self.coor[0] * 64 + 32))
        elif self.push == False and self.vector == []:  # если выбрали другой шарик, то пульсирование остановить
            self.image = pygame.transform.scale(self.etalon_image, (self.rost, self.rost))
            self.rect = self.image.get_rect(center=(self.coor[1] * 64 + 32, self.coor[0] * 64 + 32))

        if self.vector:  # если у шарира есть атрибут vector, то передвинуть его
            if self.vector[0] == "T":
                self.rect.y -= 16
                if self.rect.centery % 64 == 32:
                    self.vector.pop(0)  # удаляю пройденный путь
            elif self.vector[0] == "D":
                self.rect.y += 16
                if self.rect.centery % 64 == 32:
                    self.vector.pop(0)
            elif self.vector[0] == "R":
                self.rect.x += 16
                if self.rect.centerx % 64 == 32:
                    self.vector.pop(0)
            elif self.vector[0] == "L":
                self.rect.x -= 16
                if self.rect.centerx % 64 == 32:
                    self.vector.pop(0)
            if self.vector == []:  # если путь пройден
                self.coor = coor_put[-1]  # то в координаты шарика записать последнее значение из coor_put
                search, lines = poisk(matrix)  # ищу 5+ шариков
                if not search:  # если не нашёл
                    add_balls(free_pole, matrix)  # то создаю 3 новых шарика
                    search2, lines = poisk(matrix)  # проверяю, что после добавления не сложились 5+ шариков
                    if search2:  # если сложились
                        Ball.value = Ball.value + len(lines) * 2
                        Ball.level += len(lines) * 2
                        if Ball.level >= RANG_LEVEL:
                            Ball.shot += 1
                            print(Ball.shot, Ball.level)
                            Ball.level -= RANG_LEVEL
                        clear(lines)  # запускаю стирание шариков и восстановление свободных полей
                else:
                    Ball.value += len(lines) * 2
                    Ball.level += len(lines) * 2
                    if Ball.level >= RANG_LEVEL:
                        Ball.shot += 1
                        Ball.level -= RANG_LEVEL
                    clear(lines)  # запускаю стирание шариков и восстановление свободных полей

    def coding(self, coor_put):
        """ Превращает путь выраженный в координатах в путь в направлениях"""
        put = []
        while len(coor_put) > 1:
            if coor_put[0][0] == coor_put[1][0]:
                if coor_put[0][1] > coor_put[1][1]:
                    put.append("L")
                else:
                    put.append("R")
            else:
                if coor_put[0][0] > coor_put[1][0]:
                    put.append("T")
                else:
                    put.append("D")
            coor_put.pop(0)
        return put


def begin():
    gr_balls.empty()  # очищаю группу шариков
    file = open("data/save.dat", "rb")
    f_save = pickle.load(file)
    matrix, free_pole, Ball.value, Ball.shot, Ball.level = f_save[1], f_save[2], f_save[3], f_save[4], f_save[5]
    file.close()
    for i in range(9):
        for j in range(9):
            if matrix[i][j] != "N":
                gr_balls.add(Ball((i, j), matrix[i][j], 7))
    return matrix, free_pole, Ball.value, Ball.shot, Ball.level


def new_balls():
    """ Начинает игру заново"""
    gr_balls.empty()  # очищаю группу шариков
    matrix = [["N" for j in range(9)] for i in range(9)]  #
    free_pole = []  # очищаю список свободных полей
    Ball.value = 0
    Ball.shot = 0
    Ball.level = 0
    for i in range(9):
        for j in range(9):
            free_pole.append([i, j])  # заполняю список свободных полей всеми ячейками
    add_balls(free_pole, matrix)  # вызываю фн. создания 3-х новых шариков
    return matrix, free_pole, Ball.value, Ball.shot, Ball.level


def add_balls(free_pole, matrix):
    """Добавляет новые шарики """
    for i in range(3):
        if len(free_pole) > 0:
            coor = random.choice(free_pole)  # выбираю случайное поле
            free_pole.remove(coor)  # удаляю его из списка
            color = random.randint(1, 7)  # выбираю случайный цвет
            matrix[coor[0]][coor[1]] = color  # вставляю в выбранное поле этот цвет
            gr_balls.add(Ball(coor, color, 7))  # создаю шарик с координатами и цветом размера 7


def clear(lines):
    """Удаляет собранные линии из 5+ шариков"""
    for j in lines:
        matrix[j[0]][j[1]] = "N"
        gr_balls.empty()
        free_pole.clear()
        for i in range(9):
            for j in range(9):
                if matrix[i][j] != "N":
                    coor = [i, j]
                    color = matrix[i][j]
                    gr_balls.add(Ball(coor, color, 51))
                else:
                    free_pole.append([i, j])


def put(matrix, s, end):
    """ функция принимает квадратную матрицу, координаты начала [x,y] и конца движения [x,y]
        возвращает список координат движения
        от начала до конца [[2, 4], [2, 5], [2, 6], [3, 6], [4, 6]]
        если путь не найдет возвращает None
    """
    map_list = copy.deepcopy(matrix)
    razmer = len(map_list)
    stop = False
    begin = [s]
    start = begin[:]
    map_list[int(start[0][0])][int(start[0][1])] = 0, 0
    map_list[end[0]][end[1]] = "end"
    while len(start):

        if start[0][0] - 1 >= 0 and map_list[start[0][0] - 1][start[0][1]] == "N":
            map_list[start[0][0] - 1][start[0][1]] = start[0]
            start.append([start[0][0] - 1, start[0][1]])
        elif start[0][0] - 1 >= 0 and map_list[start[0][0] - 1][start[0][1]] == "end":
            map_list[start[0][0] - 1][start[0][1]] = start[0]
            break

        if start[0][1] + 1 < razmer and map_list[start[0][0]][start[0][1] + 1] == "N":
            map_list[start[0][0]][start[0][1] + 1] = start[0]
            start.append([start[0][0], start[0][1] + 1])
        elif start[0][1] + 1 < razmer and map_list[start[0][0]][start[0][1] + 1] == "end":
            map_list[start[0][0]][start[0][1] + 1] = start[0]
            break

        if start[0][0] + 1 < razmer and map_list[start[0][0] + 1][start[0][1]] == "N":
            map_list[start[0][0] + 1][start[0][1]] = start[0]
            start.append([start[0][0] + 1, start[0][1]])
        elif start[0][0] + 1 < razmer and map_list[start[0][0] + 1][start[0][1]] == "end":
            map_list[start[0][0] + 1][start[0][1]] = start[0]
            break

        if start[0][1] - 1 >= 0 and map_list[start[0][0]][start[0][1] - 1] == "N":
            map_list[start[0][0]][start[0][1] - 1] = start[0]
            start.append([start[0][0], start[0][1] - 1])
        elif start[0][1] - 1 >= 0 and map_list[start[0][0]][start[0][1] - 1] == "end":
            map_list[start[0][0]][start[0][1] - 1] = start[0]
            break
        start.pop(0)
    else:
        stop = True
    if stop == False:
        put = [end]
        while 1:
            coor = map_list[put[0][0]][put[0][1]]
            if coor == (0, 0):
                break
            put.insert(0, coor)
        return put
    else:
        return None


def poisk(matrix):
    """Ищет собранные линии"""
    # поиск по горизонтали
    summa = 1
    lines1 = []
    search = False
    for row in range(9):
        for col in range(5):
            if matrix[row][col] == "N":
                summa = 1
                continue
            for i in range(1, 9 - col):
                if matrix[row][col] == matrix[row][col + i] and (col + i) == 8:
                    summa += 1
                    for j in range(summa):
                        if [row, col + j] not in lines1:
                            lines1.append([row, col + j])
                    search = True
                    summa = 1
                elif matrix[row][col] == matrix[row][col + i]:
                    summa += 1
                else:
                    if summa >= 5:
                        for j in range(summa):
                            if [row, col + j] not in lines1:
                                lines1.append([row, col + j])
                        search = True
                    summa = 1
                    break
    # поиск по вертикали
    summa = 1
    lines2 = []
    for col in range(9):
        for row in range(5):
            if matrix[row][col] == "N":
                summa = 1
                continue
            for i in range(1, 9 - row):
                if matrix[row][col] == matrix[row + i][col] and (row + i) == 8:
                    summa += 1
                    for j in range(summa):
                        if [row + j, col] not in lines2:
                            lines2.append([row + j, col])
                    search = True
                    summa = 1
                elif matrix[row][col] == matrix[row + i][col]:
                    summa += 1
                else:
                    if summa >= 5:
                        for j in range(summa):
                            if [row + j, col] not in lines2:
                                lines2.append([row + j, col])
                        search = True
                    summa = 1
                    break
    # поиск по диагонали
    summa = 1
    lines3 = []
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == "N":
                summa = 1
                continue
            for i in range(1, 9 - max(row, col)):
                if matrix[row][col] == matrix[row + i][col + i] and ((col + i) == 8 or (row + i) == 8):
                    summa += 1
                    for j in range(summa):
                        if [row + j, col + j] not in lines3:
                            lines3.append([row + j, col + j])
                    search = True
                    summa = 1
                elif matrix[row][col] == matrix[row + i][col + i]:
                    summa += 1
                else:
                    if summa >= 5:
                        for j in range(summa):
                            if [row + j, col + j] not in lines3:
                                lines3.append([row + j, col + j])
                        search = True
                    summa = 1
                    break
    # поиск по диагонали
    summa = 1
    lines4 = []
    for row in range(4, 9):
        for col in range(0, 5):
            if matrix[row][col] == "N":
                summa = 1
                continue
            for i in range(1, 9 - max(col, 5 - row)):
                if matrix[row][col] == matrix[row - i][col + i] and ((col + i) == 8 or (row - i) == 0):
                    summa += 1
                    for j in range(summa):
                        if [row - j, col + j] not in lines4:
                            lines4.append([row - j, col + j])
                    search = True
                    summa = 1
                elif matrix[row][col] == matrix[row - i][col + i]:
                    summa += 1
                else:
                    if summa >= 5:
                        for j in range(summa):
                            if [row - j, col + j] not in lines4:
                                lines4.append([row - j, col + j])
                        search = True
                    summa = 1
                    break
    return (search, lines1 + lines2 + lines3 + lines4)


"""Начало программы"""

win = pygame.display.set_mode((576, 676))
pygame.display.set_caption("Игра Шарики")
pole = pygame.image.load("image/Pole3.png").convert()
about = pygame.image.load("image/About2.png").convert_alpha()
newgame1 = pygame.image.load("image/NewGame1.png").convert_alpha()
newgame2 = pygame.image.load("image/NewGame2.png").convert_alpha()
F1 = pygame.image.load("image/F2.png").convert()
ico = pygame.image.load("image/icon.png").convert_alpha()
pygame.display.set_icon(ico)
gr_balls = pygame.sprite.Group()
font1 = pygame.font.SysFont("arial", 30)
font2 = pygame.font.SysFont("arial", 40)
font3 = pygame.font.SysFont("arial", 80)
font4 = pygame.font.SysFont("arial", 16)
text_Value = font1.render("очки:", 0, (230, 230, 230))
text_Rec = font1.render("рекорд:", 0, (230, 230, 230))
file_txt = open("data/record.txt", "r")
rec = file_txt.read()
about_flag = False
matrix, free_pole, Ball.value, Ball.shot, Ball.level = begin()
text_shot = font3.render(str(Ball.shot), 0, (230, 230, 230))
xy_mouse = (1, 1)
ring_activ = False
level = 0

while 1:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            if Ball.value > int(rec):
                file_txt = open("data/record.txt", "w")
                file_txt.write(str(Ball.value))
                file_txt.close()
            data = {1: matrix, 2: free_pole, 3: Ball.value, 4: Ball.shot, 5: Ball.level}
            file = open("data/save.dat", "wb")
            pickle.dump(data, file)
            file.close()

            pygame.quit()
            sys.exit()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_F1:
                about_flag = True
        if ev.type == pygame.KEYUP:
            if ev.key == pygame.K_F1:
                about_flag = False
        if ev.type == pygame.MOUSEMOTION:
            xy_mouse = pygame.mouse.get_pos()

        if ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == pygame.BUTTON_RIGHT:
                if Ball.shot > 0:
                    row_coor = pygame.mouse.get_pos()[1] // 64  # читаю координаты курсора и перевожу в клетки
                    column_coor = pygame.mouse.get_pos()[0] // 64
                    if [row_coor, column_coor] not in free_pole:  # если полученных координат нет в свободных полях
                        for sp_pusto in gr_balls:  # находим шарик который находится на этом поле
                            if tuple(sp_pusto.coor) == (row_coor, column_coor):
                                sp_pusto.kill()
                        free_pole.append([row_coor, column_coor])
                        matrix[row_coor][column_coor] = "N"
                        Ball.shot -= 1

            if ev.button == pygame.BUTTON_LEFT:
                if pygame.mouse.get_pos()[1] < 576:
                    if len(free_pole) == 0:
                        if Ball.value > int(rec):
                            file_txt = open("data/record.txt", "w")
                            file_txt.write(str(Ball.value))
                            file_txt.close()
                            file_txt = open("data/record.txt", "r")
                            rec = file_txt.read()
                        matrix, free_pole, value, Ball.shot, Ball.level = new_balls()
                    row_coor = pygame.mouse.get_pos()[1] // 64  # читаю координаты курсора и перевожу в клетки
                    column_coor = pygame.mouse.get_pos()[0] // 64
                    if [row_coor, column_coor] not in free_pole:  # если полученных координат нет в свободных полях
                        ring = Ring(pygame.image.load("image/RingMlt1.png").convert_alpha(), row_coor, column_coor)
                        ring_activ = True
                        for sp_pusto in gr_balls:  # находим шарик который находится на этом поле
                            if tuple(sp_pusto.coor) == (row_coor, column_coor):
                                sp_pusto.push = True  # его атрибуту присваиваем True
                            else:
                                sp_pusto.push = False  # а остальным шарикам присваиваю push=False
                        Ball.vibor = True  # указываю, что один из шариков выбран
                        begin = [row_coor, column_coor]  # сохраняю координаты выбранного шарика - это начало пути
                    else:  # если не попал по шарику
                        if Ball.vibor == True:  # но один из шариков уже был выбран
                            end = [row_coor, column_coor]  # запоминаю координаты этой клетки - это конец пути
                            coor_put = put(matrix, begin, end)  # вызываю фун. для поиска пути в матрице и сохраняю
                            if coor_put != None:  # если путь есть меняю местами значения элементом начала и конца пути в матрице
                                matrix[coor_put[0][0]][coor_put[0][1]], matrix[coor_put[-1][0]][coor_put[-1][1]] = \
                                    matrix[coor_put[-1][0]][coor_put[-1][1]], matrix[coor_put[0][0]][coor_put[0][1]]
                                free_pole.append(
                                    coor_put[0])  # добавляю освободившуюся клетку (begin) в список свободных клеток
                                free_pole.remove(coor_put[-1])  # удаляю занятую клетку (end) из списка свободных
                                for i in gr_balls:
                                    if i.push:  # для шарика который выбран
                                        i.vector = i.coding(
                                            coor_put)  # преобразовываю список пути (coor_put) в списак направлений
                                        # и записываю в атрибут vector
                                        i.push = False  # нажатие передвинутого шарика сбросить
                            # если свободного пути НЕТ
                            Ball.vibor = False  # выбранных шариков нет
                            for sp_pusto in gr_balls:
                                sp_pusto.push = False  # нажатие всех шариков сбросить

                if 576 < pygame.mouse.get_pos()[1] < 660 and 448 < pygame.mouse.get_pos()[
                    0] < 566:  # если кликнул НОВАЯ ИГРА
                    if Ball.value > int(rec):
                        file_txt = open("data/record.txt", "w")
                        file_txt.write(str(Ball.value))
                        file_txt.close()
                        file_txt = open("data/record.txt", "r")
                        rec = file_txt.read()
                    matrix, free_pole, value, Ball.shot, Ball.level = new_balls()  # создать 3 шарика, расположить в матрице, создать список пустых полей
    modify_value = str(Ball.value).zfill(6)
    modify_rec = str(rec).zfill(6)
    text_Digit = font2.render(modify_value, 0, (230, 230, 230))
    text_RecValue = font2.render(modify_rec, 0, (230, 230, 230))
    text_free_pole = font2.render(str(len(free_pole)), 0, (230, 230, 230))
    text_shot = font3.render(str(Ball.shot), 0, (230, 230, 230))
    text_ball_level = font4.render(str(RANG_LEVEL - Ball.level), 0, (230, 230, 230))
    win.blit(pole, (0, 0))
    win.blit(text_Value, (35, 580))
    win.blit(text_Rec, (170, 580))
    win.blit(text_Digit, (10, 620))
    win.blit(text_free_pole, (320, 580))
    win.blit(text_RecValue, (155, 620))
    win.blit(text_ball_level, (430, 645))
    win.blit(F1, (310, 640))
    win.blit(text_shot, (390, 580))
    gr_balls.update()
    gr_balls.draw(win)

    if ring_activ:
        win.blit(ring.image, ring.rect)
        ring.update()
    if 448 < xy_mouse[0] < 566 and 576 < xy_mouse[1] < 660:
        win.blit(newgame2, (450, 580))
    else:
        win.blit(newgame1, (450, 580))
    if about_flag:
        win.blit(about, (96, 100))

    pygame.display.update()
    clock.tick(50)