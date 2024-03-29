import os
import sys
import random
import pygame


# Изображение не получится загрузить
# без предварительной инициализации pygame
pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join("data", name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Bomb(pygame.sprite.Sprite):
    image = load_image("bomb.png")
    image_boom = load_image("boom.png")

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Bomb.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - self.rect[2] - 20) + self.rect[2] // 2
        self.rect.y = random.randrange(height - self.rect[3] - 20) + self.rect[3] // 2

    def update(self, *args):
        if (
            args
            and args[0].type == pygame.MOUSEBUTTONDOWN
            and self.rect.collidepoint(args[0].pos)
        ):
            self.image_boom = pygame.transform.scale(
                self.image_boom, (self.rect[2] + 5, self.rect[3] + 5)
            )
            self.image = self.image_boom


# создадим группу, содержащую все спрайты
all_sprites = pygame.sprite.Group()
for _ in range(20):
    Bomb(all_sprites)


if __name__ == "__main__":
    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                all_sprites.update(event)
        all_sprites.draw(screen)
        pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    # завершение работы:
    pygame.quit()
