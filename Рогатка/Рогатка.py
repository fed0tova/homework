import pygame
import math
pygame.init()

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Попади в корзинку")

background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (600, 400))

wolf = pygame.image.load("wolf.png")
wolf = pygame.transform.scale(wolf, (150, 200))

full_win_sound = pygame.mixer.Sound("ура.mp3")
fly_sound = pygame.mixer.Sound("fly.mp3")
bum_sound = pygame.mixer.Sound("bum.mp3")

pygame.mixer.music.load("soundtrack.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

#яйцо
start_x, start_y = 150, 310
x, y = start_x, start_y
radius = 60

egg = pygame.image.load("egg.jpg")
egg.set_colorkey((255, 255, 255))
egg = pygame.transform.scale(egg, (radius*1.5, radius))

#физика
vx, vy = 0, 0
gravity = 0.7
bounce_loss = 0.6
on_ground = True

#корзина
basket_width, basket_height = 60, 60
basket_x, basket_y = 500, 200
basket_speed = 1.5
basket_direction = 1

basket_img = pygame.image.load("basket.png")
basket_img = pygame.transform.scale(basket_img, (basket_width, basket_height))

#текст
font = pygame.font.Font(None, 24)
big_font = pygame.font.Font(None, 48)

#флажки игры и счёт
scored_flag = False
score = 0
win_score = 5 
game_won = False

#переменные рогатки
mouse_pressed = False
drag_start_x, drag_start_y = 0, 0
max_pull_distance = 100

#=========блок самой игры=================
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not game_won:
                mouse_x, mouse_y = event.pos

                if math.sqrt((mouse_x - x)**2 + (mouse_y - y)**2) <= radius and on_ground:
                    mouse_pressed = True
                    drag_start_x, drag_start_y = mouse_x, mouse_y
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and mouse_pressed and not game_won:
                mouse_pressed = False
                if on_ground:
                    mouse_x, mouse_y = event.pos
                    dx = drag_start_x - mouse_x
                    dy = drag_start_y - mouse_y
                    
                    distance = math.sqrt(dx**2 + dy**2)
                    if distance > max_pull_distance:
                        dx = dx * max_pull_distance / distance
                        dy = dy * max_pull_distance / distance
                    
                    vx = dx * 0.2
                    vy = dy * 0.2
                    on_ground = False
                    fly_sound.play() 

    current_mouse_pos = pygame.mouse.get_pos()
    
    #движение корзины
    if not game_won:
        basket_x += basket_speed * basket_direction
        
        #границы корзины
        if basket_x + basket_width >= 600:
            basket_x = 600 - basket_width
            basket_direction = -1
        elif basket_x <= 150:
            basket_x = 150
            basket_direction = 1

        if not on_ground:
            vy += gravity
            x += vx
            y += vy

        #столновение с землёй
        if y + radius >= 400:
            y = 400 - radius
            vy = -vy * bounce_loss
            vx *= bounce_loss
            if abs(vy) < 1 and abs(vx) < 1:
                x, y = start_x, start_y
                vx, vy = 0, 0
                on_ground = True
                scored_flag = False
            else:
                bum_sound.play()

        #соприксновение с верхом корзины
        basket_rect = pygame.Rect(basket_x, basket_y, basket_width, 15)
        ball_rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)

        if ball_rect.colliderect(basket_rect) and not scored_flag and not on_ground:
            scored_flag = True
            score += 1
            
            x, y = start_x, start_y
            vx, vy = 0, 0
            on_ground = True
            
            #проверка победы
            if score >= win_score:
                game_won = True

#==================отрисовка=========================================
    screen.blit(background, (0, 0))
    screen.blit(wolf, (30, 190))

    if mouse_pressed and on_ground and not game_won:

        mouse_x, mouse_y = current_mouse_pos
        dx = drag_start_x - mouse_x
        dy = drag_start_y - mouse_y
        
        distance = math.sqrt(dx**2 + dy**2)
        if distance > max_pull_distance:
            dx = dx * max_pull_distance / distance
            dy = dy * max_pull_distance / distance
            distance = max_pull_distance
        
        temp_vx = dx * 0.2
        temp_vy = dy * 0.2
        temp_x, temp_y = start_x, start_y
        
        trajectory_points = []
        for i in range(100):
            temp_vy += gravity
            temp_x += temp_vx
            temp_y += temp_vy
            if temp_x < -50 or temp_x > 650 or temp_y > 400:
                break
            trajectory_points.append((int(temp_x), int(temp_y)))
        
        #траектория полёта
        if len(trajectory_points) > 1:
            pygame.draw.lines(screen, (150, 150, 150), False, trajectory_points, 2)
       

    #корзина
    screen.blit(basket_img, (basket_x, basket_y))

    #яйцо
    egg_rect = egg.get_rect()
    egg_rect.center = (int(x), int(y))
    screen.blit(egg, egg_rect)

    #тексты
    text_score = font.render(f"Счёт: {score}/{win_score}", True, (0, 0, 0))
    text_help = font.render("Зажмите ЛКМ на мяче и тяните, чтобы бросить в корзину", True, (0, 0, 0))
    screen.blit(text_score, (10, 10))
    screen.blit(text_help, (10, 35))

    if scored_flag and not game_won:
        hit_text = font.render("Молодец! Попал!", True, (47,137,47))
        screen.blit(hit_text, (250, 100))
        pygame.display.flip()  
        pygame.time.delay(1000)  #задержка в секунду (чтобы был виден текст)
        scored_flag = False  

    
#==== блок конца игры  ======================================
    if game_won:
        s = pygame.Surface((600, 400), pygame.SRCALPHA)
        s.fill((255, 255, 255, 200))
        screen.blit(s, (0, 0))
        
        win_text = big_font.render("УРА! ПОБЕДА! :)", True, (128, 0, 128))
        screen.blit(win_text, (220, 150))
        full_win_sound.play()

    pygame.display.flip()
    pygame.time.delay(10)

pygame.quit()