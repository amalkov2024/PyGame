import pygame
import sys
import os


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5
        )


def load_image(name, color_key=None):
    fullname = os.path.join("data", name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print("Cannot load image:", name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def terminate():  # завершение игры
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = [
        "ЗАСТАВКА",
        "",
        "Правила игры",
        "Если в правилах несколько строк,",
        "приходится выводить их построчно",
    ]

    fon = pygame.transform.scale(load_image("fon.jpg"), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color("black"))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event_game in pygame.event.get():
            if event_game.type == pygame.QUIT:
                terminate()
            elif event_game.type == pygame.KEYDOWN or event_game.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    try:
        # читаем уровень, убирая символы перевода строки
        with open(filename, "r") as mapFile:
            level_map = [line.strip() for line in mapFile]
            # и подсчитываем максимальную длину
        max_width = max(map(len, level_map))

        # дополняем каждую строку пустыми клетками ('.')
        # return list(map(lambda x: x.ljust(max_width, "."), level_map))
        return [ [x for x in y] for y in list(map(lambda x: x.ljust(max_width, "."), level_map))]
    except FileNotFoundError:
        print("Файл не найден:", filename)
        print("Программа завершена")
        terminate()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == ".":
                Tile("empty", x, y)
            elif level[y][x] == "#":
                Tile("wall", x, y)
            elif level[y][x] == "@":
                Tile("empty", x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


# Проверяем возможность хода игрока. Если ход возможен то меняем место положение игрока на карте
def step_player(player_game,karta, step_x=0, step_y=0):
    coord_x = (player_game.rect[0] - 15) // 50
    coord_y = (player_game.rect[1] - 5) // 50
    flag = False
    if step_x!=0 and 0 <= coord_x+step_x < len(karta[0]) and karta[coord_y][coord_x+step_x] != '#': # возможен ход по оси Х
        karta[coord_y][coord_x + step_x] ='@'
        karta[coord_y][coord_x] = '.'
        flag = True
    if step_y!=0 and 0 <= coord_y + step_y < len(karta) and karta[coord_y + step_y][coord_x] != '#':  # возможен ход по оси Y
        karta[coord_y + step_y][coord_x] = '@'
        karta[coord_y][coord_x] = '.'
        flag = True
    return (flag, karta)

# работа с камерой начало
class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)

# работа с камерой окончание




# Отображение имен файлов с уровнями игры для предварительного просмотра и выбора нужного
list_file = [
    file for file in os.listdir("data") if file[-4:] == ".txt" and file[:5] == "level"
]
if list_file:
    print(
        "Имена файлов с доступными для загрузки уровнями:"
    )  # для отображения файлы с уровнями игры должны именоваться level*.txt
    for f in list_file:
        print(f)
# Ввод уровня
level_start = input("Введите название файла в котором расположена карта уровня: ")
# карта уровня
map_level = load_level(level_start)

pygame.init()
pygame.key.set_repeat(200, 70)
FPS = 50
width = 550
height = 550
step = 50

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
# основной персонаж
# player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

# Запуск игры
tile_images = {"wall": load_image("box.png"), "empty": load_image("grass.png")}
player_image = load_image("mario.png", -1)

tile_width = tile_height = 50

start_screen()
# Создаем камеру
camera = Camera()
# положение игрока и размер карты
player, level_x, level_y = generate_level(map_level)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                flag_step, map_level = step_player(player, map_level, -1, 0)
                if flag_step:
                    player.rect.x -= step
            if event.key == pygame.K_RIGHT:
                flag_step, map_level = step_player(player, map_level, 1, 0)
                if flag_step:
                    player.rect.x += step
            if event.key == pygame.K_UP:
                flag_step, map_level = step_player(player, map_level, 0, -1)
                if flag_step:
                    player.rect.y -= step
            if event.key == pygame.K_DOWN:
                flag_step, map_level = step_player(player, map_level, 0, 1)
                if flag_step:
                    player.rect.y += step
    # изменяем ракурс камеры
    camera.update(player)
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)

    screen.fill(pygame.Color(0, 0, 0))
    tiles_group.draw(screen)
    player_group.draw(screen)

    pygame.display.flip()

    clock.tick(FPS)

terminate()
