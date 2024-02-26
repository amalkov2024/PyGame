import os
import sys
import random
import pygame

'''
class Bomb(pygame.sprite.Sprite):
    image = load_image("data/bomb.png")
    image_boom = load_image("data/boom.png")

    def __init__(self, group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__(group)
        self.image = Bomb.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width)
        self.rect.y = random.randrange(height)

    def update(self, *args):
        self.rect = self.rect.move(random.randrange(3) - 1,
                                   random.randrange(3) - 1)
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image = self.image_boom
'''

# создадим группу, содержащую все спрайты
all_sprites = pygame.sprite.Group()

# создадим спрайт
sprite = pygame.sprite.Sprite()
# определим его вид
sprite.image = pygame.image.load("data/bomb.png")

# и размеры
sprite.rect = sprite.image.get_rect()
print(sprite.rect)
# добавим спрайт в группу
all_sprites.add(sprite)
sprite.rect.x = 5
sprite.rect.y = 20

# изображение должно лежать в папке data
bomb_image = pygame.image.load("data/bomb.png")

for i in range(50):
    # можно сразу создавать спрайты с указанием группы
    bomb = pygame.sprite.Sprite(all_sprites)
    bomb.image = bomb_image
    bomb.rect = bomb.image.get_rect()

    # задаём случайное местоположение бомбочке
    bomb.rect.x = random.randrange(480-bomb.rect[2])+bomb.rect[2]//2
    bomb.rect.y = random.randrange(480-bomb.rect[3])+bomb.rect[3]//2


if __name__ == "__main__":
    # инициализация Pygame:
    #bomb = Bomb()
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)

    running = True
    screen.fill((0, 0, 0))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
        # в главном игровом цикле
        all_sprites.draw(screen)
        pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    # завершение работы:
    pygame.quit()
