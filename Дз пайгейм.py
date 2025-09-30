import pygame
import math
pygame.init()
font = pygame.font.SysFont(None, 24)

screen = pygame.display.set_mode((1152, 768))
pygame.display.set_caption("Пейзаж")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((153,228,238))
    pygame.draw.rect(screen, (14,147,37), (0, 380, 1152, 500)) #трава
    pygame.draw.rect(screen, (147,107,14), (200, 300, 280, 200)) #стена домика
    pygame.draw.rect(screen, (0,0,0), (200, 300, 280, 200),2) #обводка стены 
    pygame.draw.rect(screen, (14,147,145), (295, 355, 100, 90)) #окно
    pygame.draw.rect(screen, (181,98,24), (295, 355, 100, 90),3) #обводка окна
    pygame.draw.polygon(screen, (235,47,68), [(200,300,),(340,160),(480,300)]) #крыша
    pygame.draw.polygon(screen, (0,0,0), [(200,300,),(340,160),(480,300)],2) #обводка крыши
    pygame.draw.rect(screen, (0,0,0), (820, 330, 30, 130)) #ствол дерева

    pygame.draw.circle(screen, (15,83,14), (835,180), 50)#листва
    pygame.draw.circle(screen, (0,0,0), (835,180), 50, 2)#листва обводка

    pygame.draw.circle(screen, (15,83,14), (780,235), 50)#листва
    pygame.draw.circle(screen, (0,0,0), (780,235), 50, 2)#листва обводка

    pygame.draw.circle(screen, (15,83,14), (890,225), 50)#листва
    pygame.draw.circle(screen, (0,0,0), (890,225), 50, 2)#листва обводка

    pygame.draw.circle(screen, (15,83,14), (835,270), 50)#листва
    pygame.draw.circle(screen, (0,0,0), (835,270), 50, 2)#листва обводка

    pygame.draw.circle(screen, (15,83,14), (800,300), 50)#листва
    pygame.draw.circle(screen, (0,0,0), (800,300), 50, 2)#листва обводка

    pygame.draw.circle(screen, (15,83,14), (875,300), 50)#листва
    pygame.draw.circle(screen, (0,0,0), (875,300), 50, 2)#листва обводка


    #лучики солнца
    points = []
    for i in range(40): 
        ugol = math.pi * 2 * i / 40
    
        if i % 2 == 0:
            r = 60 
        else:
            r = 50  
    
        x = 1030 + r * math.cos(ugol)
        y = 90 + r * math.sin(ugol)
        points.append((x, y))

    pygame.draw.polygon(screen, (249,194,194), points)
    pygame.draw.polygon(screen, (0,0,0), points,1)

    pygame.draw.circle(screen, (254,249,249), (520,130), 50)#облака
    pygame.draw.circle(screen, (0,0,0), (520,130), 50, 2)#облака обводка

    pygame.draw.circle(screen, (254,249,249), (570,130), 50)#облака
    pygame.draw.circle(screen, (0,0,0), (570,130), 50, 2)#облака обводка

    pygame.draw.circle(screen, (254,249,249), (620,130), 50)#облака
    pygame.draw.circle(screen, (0,0,0), (620,130), 50, 2)#облака обводка

    pygame.draw.circle(screen, (254,249,249), (670,130), 50)#облака
    pygame.draw.circle(screen, (0,0,0), (670,130), 50, 2)#облака обводка

    pygame.draw.circle(screen, (254,249,249), (630,100), 50)#облака
    pygame.draw.circle(screen, (0,0,0), (630,100), 50, 2)#облака обводка

    pygame.draw.circle(screen, (254,249,249), (570,100), 50)#облака
    pygame.draw.circle(screen, (0,0,0), (570,100), 50, 2)#облака обводка
    
    mx, my = pygame.mouse.get_pos()
    text = font.render(f"x: {mx}, y: {my}", True, (0, 0, 0))
    screen.blit(text, (10, 10))



    pygame.display.flip()
    

pygame.quit()