import pygame

if __name__ == "__main__":
    n = input()
    if n.isdigit():
        n = int(n)
        # инициализация Pygame:
        pygame.init()
        # размеры окна:
        size = width, height = 300, 300
        # screen — холст, на котором нужно рисовать:
        screen = pygame.display.set_mode(size)
        # команды рисования на холсте
        screen.fill((0, 0, 0))
        # горизонтальные эллипсы
        l = 0
        w = 300
        for t in range(0, 150, 150 // n):
            h = (150 - t) * 2
            pygame.draw.ellipse(screen, (255, 255, 255), (l, t, w, h), width=1)
        # вертикальные эллипсы
        t = 0
        h = 300
        for l in range(0, 150, 150 // n):
            w = (150 - l) * 2
            pygame.draw.ellipse(screen, (255, 255, 255), (l, t, w, h), width=1)

        pygame.display.flip()
        # ожидание закрытия окна:
        while pygame.event.wait().type != pygame.QUIT:
            pass
        # завершение работы:
        pygame.quit()
    else:
        print("Неправильный формат ввода")
