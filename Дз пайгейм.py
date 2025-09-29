import pygame
pygame.init()

screen = pygame.display.set_mode((1152, 768))
pygame.display.set_caption("Пейзаж")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((153,228,238))
    pygame.draw.circle(screen, (255, 240, 0), (576, 200), 70)
    pygame.draw.polygon(screen, (250, 160, 50), [
        (0, 400), (200, 200), (400, 350), (600, 250),
        (800, 380), (1152, 300), (1152, 400), (0, 400)
    ])

   

    
    mx, my = pygame.mouse.get_pos()
    text = font.render(f"x: {mx}, y: {my}", True, (0, 0, 0))
    screen.blit(text, (10, 10))
    pygame.draw.rect(screen, (170, 70, 50), (0, 400, 1152, 500))
    pygame.draw.rect(screen, (170, 120, 130), (0, 500, 1152, 268))

    pygame.display.flip()
    

pygame.quit()