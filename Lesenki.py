import pygame


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(vertical_borders)
        self.image = pygame.Surface((50, 10), pygame.SRCALPHA, 32)
        pygame.draw.rect(
            self.image,
            pygame.Color("gray"),
            (0, 0, 50, 10),
        )
        self.rect = pygame.Rect(x, y, 50, 10)


class Block_vert(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1):
        super().__init__(all_sprites)
        self.add(horizontal_borders)
        self.image = pygame.Surface([10, 50])
        self.image.fill((255, 0, 0))
        self.rect = pygame.Rect(x1, y1, 10, 50)


class Rect(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.x = x
        self.y = y
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA, 32)
        pygame.draw.rect(
            self.image,
            pygame.Color("blue"),
            (0, 0, 20, 20),
        )
        self.rect = pygame.Rect(x, y, 20, 20)
        self.vx = 0
        self.vy = 1

    def update(self):
        if not pygame.sprite.spritecollideany(self, vertical_borders) and not pygame.sprite.spritecollideany(self,
                                                                                                             horizontal_borders):
            self.rect = self.rect.move(0, 1)

    def remove_rect(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)

    def move_horizont(self, m):
        self.rect = self.rect.move(m, 0)

    def move_vertical(self, m):
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.rect = self.rect.move(0, m)


fps = 20
clock = pygame.time.Clock()
pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()

if __name__ == "__main__":
    vertical_borders = pygame.sprite.Group()
    horizontal_borders = pygame.sprite.Group()
    running = True
    flag = False
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # нажатие левой кнопки
                    if pygame.key.get_mods() & pygame.KMOD_LCTRL:
                        Block_vert(event.pos[0], event.pos[1])
                    else:
                        Block(event.pos[0], event.pos[1])
                if event.button == 3:
                    # правая кнопка мыши
                    if not flag:
                        kub = Rect(event.pos[0], event.pos[1])
                        flag = not flag
                    else:
                        kub.remove_rect(event.pos[0], event.pos[1])
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    kub.move_horizont(10)
                if event.key == pygame.K_LEFT:
                    kub.move_horizont(-10)
                if event.key == pygame.K_DOWN:
                    kub.move_vertical(10)
                if event.key == pygame.K_UP:
                    kub.move_vertical(-10)
        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(fps)
        pygame.display.flip()

    # завершение работы:
    pygame.quit()
