import pygame
import random
import math

pygame.init()
pygame.mixer.init()

#----------------БЛОК ПЕРЕМЕННЫХ---------------------------
#ЗВУКИ
bang = pygame.mixer.Sound("bang.mp3")
quacking = pygame.mixer.Sound("quacking.mp3")
pain = pygame.mixer.Sound("pain.mp3")
intro = pygame.mixer.Sound("intro.mp3")
win = pygame.mixer.Sound("win.mp3")
lose = pygame.mixer.Sound("lose.mp3")
pygame.mixer.music.load("sound.mp3")

#ПАРАМЕТРЫ НАЧАЛЬНОГО ЭКРАНА
WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("НеФото-Охота")

#ПЕРЕМЕННАЯ ОТСЧЁТА ВРЕМЕНИ
clock = pygame.time.Clock()

#ШРИФТЫ
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 72)
rule_font = pygame.font.Font(None, 32)

#КАРТИНКИ 
duck1 = pygame.image.load("duck1.png")
duck2 = pygame.image.load("duck2.png")
duck3 = pygame.image.load("duck3.png")
duck4 = pygame.image.load("duck4.png")
duck_images = [duck1, duck2, duck3, duck4]
for i in range(len(duck_images)):
    duck_images[i] = pygame.transform.scale(duck_images[i], (160, 120))

bush1 = pygame.image.load("bush1.png")
bush2 = pygame.image.load("bush2.png")
bush_images = [bush1, bush2]
for i in range(len(bush_images)):
    bush_images[i] = pygame.transform.scale(bush_images[i], (160, 200))

dog_image = pygame.image.load("dog.png")
dog_image = pygame.transform.scale(dog_image, (160, 240))

cloud1 = pygame.image.load("cloud1.png")
cloud2 = pygame.image.load("cloud2.png")
cloud3 = pygame.image.load("cloud3.png")
cloud_images = [cloud1, cloud2, cloud3]
for i in range(len(cloud_images)):
    cloud_images[i] = pygame.transform.scale(cloud_images[i], (300, 200))

sky_image = pygame.image.load("sky.png")
grass_image = pygame.image.load("grass.png")

#ПОДГОН ФОНА ПОД ЭКРАН
sky_image = pygame.transform.scale(sky_image, (WIDTH, HEIGHT - 150))
grass_image = pygame.transform.scale(grass_image, (grass_image.get_width(), 250))

#ИГРОК И ФИЗИКА
player_screen_x = WIDTH // 2 - 80
player_screen_y = HEIGHT - 400
player_width = 160
player_height = 100
player_world_x = 0
player_speed = 8
is_jumping = False
jump_velocity = 0
jump_power = 20
gravity = 0.8
on_ground = True

mouse_pressed = False
drag_start_x, drag_start_y = 0, 0
max_pull_distance = 150

#СТАТЫ
score = 0
health = 5
ducks_hit = 0

obstacles = []
ducks = []
bullets = []

#РАНДОМАЙЗЕР ОБЛАКОВ
clouds = []
for i in range(6):
    clouds.append([
        random.randint(-1000, 2000), 
        random.randint(50, 200),      
        random.randint(0, len(cloud_images)-1)
    ])

duck_timer = 0
obstacle_timer = 0
last_player_move_time = 0

#----------------БЛОК САМОЙ ИГРЫ-----------------

game_state = "intro"
music_started = False

#ФУНКЦИЯ ОТРИСОВКИ ПРАВИЛ
def draw_intro():
    screen.fill((255, 255, 255)) 
    
    title = title_font.render("ПРАВИЛА ИГРЫ", True, (0, 0, 0))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 40))
    
    rules = [
        "УПРАВЛЕНИЕ:",
        "A/D - двигаться влево/вправо",
        "ПРОБЕЛ - прыгать",
        "ЛКМ на персонаже - натянуть рогатку и выстрелить",
        "",
        "ЦЕЛЬ ИГРЫ:",
        "Подстрелить 3 уток",
        "",
        "КАК ИГРАТЬ:",
        "1. Двигайся (A/D) найти уток ",
        "2. Нажми ЛКМ на персонаже, потяни и отпусти для выстрела",
        "",
        "ОПАСНОСТИ:",
        "• Не дай утке атаковать (коснуться тебя)",
        "• Кусты преграждают путь, прыгай",
        "",
        "НАЖМИ ПРОБЕЛ ДЛЯ НАЧАЛА ИГРЫ"
    ]

    for i, rule in enumerate(rules):
        text = rule_font.render(rule, True, (50, 50, 50))
        screen.blit(text, (WIDTH//2 - text.get_width()//2, 120 + i * 35))


running = True
while running:
    dt = clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            player_screen_x = WIDTH // 2 - player_width // 2
            
            #ПОДГОН РАЗМЕРА ПОД ЭКРАН
            sky_image = pygame.transform.scale(pygame.image.load("sky.png"), (WIDTH, HEIGHT - 150))

            grass = pygame.image.load("grass.png")
            grass_image = pygame.transform.scale(grass, (grass.get_width(), 250))
        
        #ПРОБЕЛ,ДЛЯ ПЕРЕХОДА ИЗ ИНТРО В ИГРУ
        if event.type == pygame.KEYDOWN and game_state == "intro":
            if event.key == pygame.K_SPACE:
                intro.play()
                game_state = "playing"
                #ВКЛЮЧИТЬ МУЗЫКУ
                if not music_started:
                    pygame.mixer.music.play(-1)
                    music_started = True
        
        elif game_state == "playing":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    click_padding = 30
                    if (mouse_x > player_screen_x - click_padding and 
                        mouse_x < player_screen_x + player_width + click_padding and
                        mouse_y > player_screen_y - click_padding and 
                        mouse_y < player_screen_y + player_height + click_padding):
                        mouse_pressed = True
                        drag_start_x, drag_start_y = mouse_x, mouse_y
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and mouse_pressed:
                    mouse_pressed = False
                    mouse_x, mouse_y = event.pos
                    dx = drag_start_x - mouse_x
                    dy = drag_start_y - mouse_y
                    
                    distance = math.sqrt(dx**2 + dy**2)
                    if distance > max_pull_distance:
                        dx = dx * max_pull_distance / distance
                        dy = dy * max_pull_distance / distance
                    
                    if len(ducks) > 0:
                        bullets.append([
                            player_world_x,
                            player_screen_y + player_height//2,
                            dx * 0.25,
                            dy * 0.25
                        ])
                        bang.play()
    
    #ИНТРО
    if game_state == "intro":
        draw_intro()
        pygame.display.flip()
        continue
    
    current_mouse_pos = pygame.mouse.get_pos()
    screen.fill((0, 0, 0))  
    
    #ПРОЦЕСС ИГРЫ
    if game_state == "playing":
        keys = pygame.key.get_pressed()
        player_moved = False
        
        old_player_world_x = player_world_x #это обновление по иксу
        
        #БЕГ ВЛЕВО
        if keys[pygame.K_a]:
            player_world_x -= player_speed
            player_moved = True
            last_player_move_time = pygame.time.get_ticks()
        
        #БЕГ ВПРАВО
        if keys[pygame.K_d]:
            player_world_x += player_speed
            player_moved = True
            last_player_move_time = pygame.time.get_ticks()
        
        #ПРЫЖОК
        if keys[pygame.K_SPACE] and on_ground:
            is_jumping = True
            on_ground = False
            jump_velocity = jump_power
        
        #МЕХАНИКА ПРЫЖКА
        if is_jumping:
            player_screen_y -= jump_velocity
            jump_velocity -= gravity
            if player_screen_y >= HEIGHT - 300 - player_height:
                player_screen_y = HEIGHT - 300 - player_height
                on_ground = True
                is_jumping = False
        
       #ТАЙМЕР ПРЕПЯТСТВИЙ
        obstacle_timer += 1
        if obstacle_timer > 120:
            spawn_distance = 800
            num_obstacles = random.randint(1, 2)
            for i in range(num_obstacles):
                obs_height = 200
                obs_width = 160
                spacing = random.randint(200, 350)
                bush_index = random.randint(0, len(bush_images)-1)
                
                obstacles.append([
                    player_world_x + spawn_distance + spacing,
                    HEIGHT - 300 - obs_height, 
                    obs_width,
                    obs_height,
                    bush_index
                ])
            
            obstacle_timer = 0
        
        duck_timer += 1
        current_time = pygame.time.get_ticks()
        
        #УТИНЫЙ ТАЙМЕР
        if (player_moved and 
            duck_timer > 180 and
            current_time - last_player_move_time < 3000):
            
            start_world_x = player_world_x + random.randint(-300, 300)
            start_y = -30
            
            dx_to_player = (player_world_x + player_screen_x) - start_world_x
            dy_to_player = (player_screen_y + player_height//2) - start_y
            
            distance = math.sqrt(dx_to_player**2 + dy_to_player**2)
            speed = 3
            
            duck_index = random.randint(0, len(duck_images)-1)
            ducks.append([
                start_world_x,
                start_y,
                (dx_to_player / distance) * speed,
                (dy_to_player / distance) * speed,
                30,
                duck_index
            ])
            duck_timer = 0
        
        player_rect = pygame.Rect(player_screen_x, player_screen_y, player_width, player_height)
        collision_happened = False
        
        for obs in obstacles[:]:
            obs_screen_x = obs[0] - player_world_x + player_screen_x
            obs_rect = pygame.Rect(obs_screen_x, obs[1], obs[2], obs[3])
            
            # ПРОВЕРКА ПЕРЕСЕЧЕНИЯ ПРЯМОУГОЛЬНИКОВ ИГРОКА И КУСТА
            if player_rect.colliderect(obs_rect) and on_ground and not is_jumping:
                collision_happened = True
            
            if obs[0] < player_world_x - 1500:
                obstacles.remove(obs)
        
        if collision_happened and on_ground:
            player_world_x = old_player_world_x
        
        for duck in ducks[:]:
            duck[0] += duck[2]
            duck[1] += duck[3]
            
            duck_screen_x = duck[0] - player_world_x + player_screen_x
            
            if (duck_screen_x < -150 or duck_screen_x > WIDTH + 150 or 
                duck[1] > HEIGHT + 150):
                ducks.remove(duck)
                continue
            
            #УТИНЫЙ ПРЯМОУГОЛЬНИК
            duck_rect = pygame.Rect(duck_screen_x - duck[4], duck[1] - duck[4], 
                                   duck[4]*2, duck[4]*2)
            #СНИМАЕМ ЗДОРОВЬЕ, ЕСЛИ СТОЛКНУЛИСЬ С УТКОЙ
            if duck_rect.colliderect(player_rect):
                ducks.remove(duck)
                health -= 1
                pain.play()
        
        #ОБНОВЛЕНИЕ ПУЛИ ПО КООРДИНАТАМ
        for bullet in bullets[:]:
            bullet[0] += bullet[2]
            bullet[1] += bullet[3]
            bullet[3] += 0.2
            
            bullet_screen_x = bullet[0] - player_world_x + player_screen_x
            
            for duck in ducks[:]:
                duck_screen_x = duck[0] - player_world_x + player_screen_x
                duck_rect = pygame.Rect(duck_screen_x - duck[4], duck[1] - duck[4], 
                                       duck[4]*2, duck[4]*2)
                bullet_rect = pygame.Rect(bullet_screen_x - 5, bullet[1] - 5, 10, 10)
                
                if duck_rect.colliderect(bullet_rect):
                    ducks.remove(duck)
                    bullets.remove(bullet)
                    score += 10
                    ducks_hit += 1
                    quacking.play()
                    break #КИК УТКИ 
            
            if (bullet_screen_x < -50 or bullet_screen_x > WIDTH + 50 or 
                bullet[1] > HEIGHT + 50):
                bullets.remove(bullet)
        
        if health <= 0:
            game_state = "lose"
            lose.play()
        if ducks_hit >= 3:
            game_state = "win"
            win.play()
    
#------------------ОТРИСОВКА------------------------------
    screen.blit(sky_image, (0, 0))

    for cloud in clouds:
        cloud_x, cloud_y, cloud_img_index = cloud
        cloud_screen_x = cloud_x - player_world_x * 0.15
        
        if cloud_screen_x < -400:
            cloud[0] = player_world_x * 0.3 + WIDTH + random.randint(400, 800)
            cloud[1] = random.randint(50, 200)
            cloud[2] = random.randint(0, len(cloud_images)-1)
        elif cloud_screen_x > WIDTH + 400:
            cloud[0] = player_world_x * 0.3 - random.randint(400, 800)
            cloud[1] = random.randint(50, 200)
            cloud[2] = random.randint(0, len(cloud_images)-1)
        
        cloud_screen_x = cloud[0] - player_world_x * 0.3
        if cloud_screen_x > -250 and cloud_screen_x < WIDTH + 250:
            cloud_img = cloud_images[cloud_img_index]
            screen.blit(cloud_img, (cloud_screen_x, cloud_y))
    
    ground_y = HEIGHT - 270
    grass_scroll = -player_world_x % grass_image.get_width()

    grass_width = grass_image.get_width()
    start_x = grass_scroll - grass_width
    end_x = WIDTH + grass_width
    
    x = start_x
    while x < end_x:
        screen.blit(grass_image, (x, ground_y))
        x += grass_width
    
    for obs in obstacles:
        obs_screen_x = obs[0] - player_world_x + player_screen_x
        if obs_screen_x > -obs[2] and obs_screen_x < WIDTH + obs[2]:
            bush_img = bush_images[obs[4]]
            screen.blit(bush_img, (obs_screen_x, obs[1] + 120))
    
    screen.blit(dog_image, (player_screen_x, player_screen_y))
    
    for duck in ducks:
        duck_screen_x = duck[0] - player_world_x + player_screen_x
        duck_img = duck_images[duck[5]]
        screen.blit(duck_img, (duck_screen_x - 80, duck[1] - 60))
    
    for bullet in bullets:
        bullet_screen_x = bullet[0] - player_world_x + player_screen_x
        pygame.draw.circle(screen, (255, 0, 0), 
                          (int(bullet_screen_x), int(bullet[1])), 12)
    
    if mouse_pressed:
        mouse_x, mouse_y = current_mouse_pos
        dx = drag_start_x - mouse_x
        dy = drag_start_y - mouse_y
        
        distance = math.sqrt(dx**2 + dy**2)
        if distance > max_pull_distance:
            dx = dx * max_pull_distance / distance
            dy = dy * max_pull_distance / distance
        
        temp_vx = dx * 0.25
        temp_vy = dy * 0.25
        temp_x = player_screen_x + player_width//2 - 10
        temp_y = player_screen_y + player_height//2 + 100
        
        points = []
        for i in range(60):
            temp_vy += 0.2
            temp_x += temp_vx
            temp_y += temp_vy
            if temp_x < -50 or temp_x > WIDTH + 50 or temp_y > HEIGHT + 50:
                break
            points.append((int(temp_x), int(temp_y)))
        
        if len(points) > 1:
            if len(ducks) > 0:
                pygame.draw.lines(screen, (255, 255, 0), False, points, 3)
            else:
                pygame.draw.lines(screen, (150, 150, 150), False, points, 2)
        
        pygame.draw.line(screen, (200, 200, 200), 
                        (player_screen_x + player_width//2 - 10, player_screen_y + player_height//2 + 100),
                        (mouse_x, mouse_y), 3)
    

    for i in range(5):
        color = (255, 0, 0) if i < health else (100, 0, 0)
        pygame.draw.rect(screen, color, (10 + i * 35, 10, 30, 30))
    
    score_text = font.render(f"Очки: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 50))
    
    ducks_text = font.render(f"Утки: {ducks_hit}/3", True, (255, 255, 255))
    screen.blit(ducks_text, (10, 90))
    
    if not player_moved and (pygame.time.get_ticks() - last_player_move_time > 2000):
        move_text = font.render("Двигайтесь, чтобы найти утку!", True, (255, 255, 0))
        screen.blit(move_text, (WIDTH//2 - 150, 30))
    
    controls = font.render("A/D - двигаться, ПРОБЕЛ - прыгать, ЛКМ - рогатка", 
                          True, (200, 200, 200))
    screen.blit(controls, (WIDTH//2 - 250, HEIGHT - 30))
    
    # КОНЕЦ ИГРЫ
    if game_state == "win":
        pygame.draw.rect(screen, (0, 100, 0, 180), (0, 0, WIDTH, HEIGHT))
        win_text = font.render("ПОБЕДА! Вы поймали 3 уток! :)", True, (255, 255, 255))
        screen.blit(win_text, (WIDTH//2 - 200, HEIGHT//2 - 50))
    
    elif game_state == "lose":
        pygame.draw.rect(screen, (100, 0, 0, 180), (0, 0, WIDTH, HEIGHT))
        lose_text = font.render("ПОРАЖЕНИЕ! Вас избили утки :(", True, (255, 255, 255))
        screen.blit(lose_text, (WIDTH//2 - 220, HEIGHT//2 - 50))
    
    pygame.display.flip()

pygame.quit()