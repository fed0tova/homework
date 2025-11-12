import pygame
import random
import math

#==== блок данных, переменных и прочего ====================================== 

pygame.init()
screen_width = 700
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ну, яйца!")
font = pygame.font.SysFont(None, 30)

player_size = 50 
target_radius = 30
score = 0
missed_count = 0
max_missed = 5
win_score = 10  

win_sound = pygame.mixer.Sound("win_sound.mp3")
fail_sound = pygame.mixer.Sound("fail_sound.mp3")

full_win_sound = pygame.mixer.Sound("ура.mp3")
full_fail_sound = pygame.mixer.Sound("проигрыш.mp3")


background = pygame.image.load("coop.jpg")
background = pygame.transform.scale(background, (screen_width, screen_height))


basket = pygame.image.load("basket.png")
basket = pygame.transform.scale(basket, (60, 60))

egg = pygame.image.load("egg.jpg")
egg.set_colorkey((255, 255, 255))
egg = pygame.transform.scale(egg, (target_radius*3, target_radius*2))

#диапозон движения корзины
center_x = 350 
min_x = center_x - 100  
max_x = center_x + 100 - player_size  

player_x = center_x - player_size // 2
player_y = 400  

balls = []
spawn_interval = 1500
last_spawn_time = 0

running = True
game_over = False
game_win = False

#==== блок процесса игры ======================================

while running:
    current_time = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if not game_over and not game_win:
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        #ограничение движения корзины
        player_x = max(min_x, min(max_x, mouse_x - player_size // 2))
        

        if current_time - last_spawn_time > spawn_interval:
            if random.choice([True, False]):
                balls.append([50, 50, 'left'])
            else:
                balls.append([650, 50, 'right'])
            last_spawn_time = current_time
        
        balls_delete = []
        
        for ball in balls:
            x, y, ball_type = ball
            speed = 2
            
            #вертикальное падения яйца
            if ball_type == 'left' and x >= center_x - 80:
                ball[1] += speed
            elif ball_type == 'right' and x <= center_x + 80:
                ball[1] += speed
            else:
                #угловое падение
                if ball_type == 'left':
                    angle = 30
                    ball[0] += speed * math.cos(math.radians(angle))
                    ball[1] += speed * math.sin(math.radians(angle))
                else:
                    angle = 150
                    ball[0] += speed * math.cos(math.radians(angle))
                    ball[1] += speed * math.sin(math.radians(angle))
            
            #касание корзины
            if ((y + target_radius >= player_y) and (y - target_radius <= player_y + player_size) and (x + target_radius >= player_x) and (x - target_radius <= player_x + player_size)):
                score += 1
                win_sound.play()
                balls_delete.append(ball)
                
                #победа
                if score >= win_score:
                    game_win = True
            
            #поражение
            elif y > 500:
                fail_sound.play()
                missed_count += 1
                balls_delete.append(ball)
                
                if missed_count >= max_missed:
                    game_over = True
        
        #удалить шары
        for ball in balls_delete:
            if ball in balls:
                balls.remove(ball)
    
    screen.blit(background, (0, 0))  # фон
    
#==== блок отрисовки ======================================

    #спавн шаров, пока идёт игра
    if not game_over and not game_win:
        for ball in balls:
            x, y, ball_type = ball
            screen.blit(egg, (int(x - target_radius), int(y - target_radius)))
    
    screen.blit(basket, (player_x, player_y)) #корзина 
    
    #место для движения корзины
    pygame.draw.line(screen, (255, 255, 0), (min_x, player_y + 60), 
                    (max_x + player_size, player_y + 60), 2)
    
    #жерди для яиц
    pygame.draw.line(screen, (56, 24, 6), (0, 45), (245, 185), 15)
    pygame.draw.line(screen, (56, 24, 6), (485, 185), (700, 60), 15)
    
    #статы
    score_text = font.render(f"Счёт: {score}", True, (255, 255, 255))
    missed_text = font.render(f"Пропущено: {missed_count}/{max_missed}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(missed_text, (10, 40))
    
#==== блок конца игры  ======================================
    
    if game_over:
        text_width, text_height = font.size("БЛИНБ, ВЫ ПРОИГРАЛИ :(")
        rect_width = text_width + 40
        rect_x = (screen_width - rect_width) // 2
        pygame.draw.rect(screen, (255, 255, 255), (rect_x, 200, rect_width, 100))
        game_over_text = font.render("БЛИНБ, ВЫ ПРОИГРАЛИ :(", True, (133, 32, 9))
        screen.blit(game_over_text, (rect_x + 20, 240))
        full_fail_sound.play()
    
    if game_win:
        text_width, text_height = font.size("УРА, ПОБЕДА :)")
        rect_width = text_width + 40
        rect_x = (screen_width - rect_width) // 2
        pygame.draw.rect(screen, (255, 255, 255), (rect_x, 200, rect_width, 100))
        game_win_text = font.render("УРА, ПОБЕДА :)", True, (20, 133, 9))
        screen.blit(game_win_text, (rect_x + 20, 240))
        full_win_sound.play()

    pygame.display.flip()
    pygame.time.Clock().tick(60)


pygame.quit()
