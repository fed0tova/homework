import pygame
import math

pygame.init()

WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Солнечная система")

font = pygame.font.SysFont('Arial', 32)

explosion = pygame.mixer.Sound("Explosion.wav")
pygame.mixer.music.load("space.mp3")
pygame.mixer.music.set_volume(0.5)

intro = True
explosion_radius = 0

cx = WIDTH // 2
cy = HEIGHT // 2   
FPS = 60
clock = pygame.time.Clock()

class Planet:
    def __init__(self, screen, image, orbit_radius, speed=0, angle=0):
        self.screen = screen
        self.image = image
        self.orbit_radius = orbit_radius
        self.speed = speed
        self.angle = angle

    def update(self, dt):
        self.angle += self.speed * dt
        self.x = cx + self.orbit_radius * math.cos(self.angle)
        self.y = cy + self.orbit_radius * math.sin(self.angle)

    def draw(self):
        image_rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        self.screen.blit(self.image, image_rect)

class Asteroid:
    def __init__(self, screen, image, radius, rotation_speed=0.5):
        self.screen = screen
        self.image = image
        self.radius = radius
        self.rotation_speed = rotation_speed
        self.angle = 0

    def update(self, dt):
        self.angle += self.rotation_speed * dt

    def draw(self):
        rotate = pygame.transform.rotate(self.image, math.degrees(self.angle))
        rect = rotate.get_rect(center=(cx, cy))
        self.screen.blit(rotate, rect)

sun = pygame.image.load("sun.png").convert_alpha()
sun = pygame.transform.scale(sun, (120, 120))

earth = pygame.image.load("earth.png").convert_alpha()
earth = pygame.transform.scale(earth, (45, 45))

mars = pygame.image.load("mars.png").convert_alpha()
mars = pygame.transform.scale(mars, (80, 35))

jupiter = pygame.image.load("jupiter.png").convert_alpha()
jupiter = pygame.transform.scale(jupiter, (90, 90))

moon = pygame.image.load("moon.png").convert_alpha()
moon = pygame.transform.scale(moon, (20, 20))

asteroid = pygame.image.load("asteroid.png").convert_alpha()
asteroid = pygame.transform.scale(asteroid, (600, 600))


earth = Planet(screen, earth, 100, 0.5, 0)
mars = Planet(screen, mars, 150, 0.5, 1)
jupiter = Planet(screen, jupiter, 320, 0.5, 2)
moon = Planet(screen, moon, 30, 2, 0)


asteroid_ring = Asteroid(screen, asteroid, 320, 0.5)

running = True
while running:
    dt = clock.tick(FPS) / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            cx = WIDTH // 2
            cy = HEIGHT // 2
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and intro:
            intro = False
            explosion_radius = 0
            explosion.play()
    
    if intro:
        screen.fill((0, 0, 0))
        text = font.render("Нажмите на SPACE для создания вселенной", True, (255, 255, 255))
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 50))
        pygame.draw.circle(screen, (255, 255, 255), (WIDTH//2, HEIGHT//2 + 50), 3)
    
    elif explosion_radius < 500:
        screen.fill((0, 0, 0))
        explosion_radius += 8
        pygame.draw.circle(screen, (255, 255, 255), (WIDTH//2, HEIGHT//2), explosion_radius)
        
        if explosion_radius >= 500:
            pygame.mixer.music.play(-1) 
    
    else:
        earth.update(dt)
        mars.update(dt)
        jupiter.update(dt)
        asteroid_ring.update(dt)
        
        moon.angle += moon.speed * dt
        moon.x = earth.x + moon.orbit_radius * math.cos(moon.angle)
        moon.y = earth.y + moon.orbit_radius * math.sin(moon.angle)
        
        screen.fill((0, 0, 20))
        
        asteroid_ring.draw()
        
        sun_rect = sun.get_rect(center=(cx, cy))
        screen.blit(sun, sun_rect)
        
        jupiter.draw()
        mars.draw()
        earth.draw()
        moon.draw()

    pygame.display.flip()

pygame.quit()