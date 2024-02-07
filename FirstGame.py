import pygame

if __name__ == '__main__':
    pygame.init()
    size = widht, height = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass