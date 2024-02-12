import pygame

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("К щелчку")
    size = width, height = 501, 501
    screen = pygame.display.set_mode(size)
    x_pos = 250
    y_pos = 250
    x_y = (250, 250)
    fps = 80
    clock = pygame.time.Clock()

    flag = False
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_y = event.pos  # координаты нажатия мышки
                dx = x_y[0] - x_pos
                dy = x_y[1] - y_pos
        if x_pos != x_y[0]:
            x_pos += -1 * (dx < 0) + (dx > 0)
        if y_pos != x_y[1]:
            y_pos += -1 * (dy < 0) + (dy > 0)

        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, (255, 0, 0), (int(x_pos), int(y_pos)), 20)
        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()
