import pygame
import math
import random

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Asteroids")

# Spaceship
class Ship:
    def __init__(self):
        self.x, self.y = width//2, height//2
        self.angle = 0
        self.speed = 0
        self.dx, self.dy = 0, 0

    def move(self):
        self.x += self.dx
        self.y += self.dy
        if self.x < 0: self.x += width
        if self.x > width: self.x -= width
        if self.y < 0: self.y += height
        if self.y > height: self.y -= height

    def draw(self):
        points = [
            (self.x + 20 * math.cos(math.radians(self.angle)), self.y - 20 * math.sin(math.radians(self.angle))),
            (self.x - 10 * math.cos(math.radians(self.angle + 120)), self.y + 10 * math.sin(math.radians(self.angle + 120))),
            (self.x - 10 * math.cos(math.radians(self.angle - 120)), self.y + 10 * math.sin(math.radians(self.angle - 120)))
        ]
        pygame.draw.polygon(screen, (255, 255, 255), points)

# Asteroid
class Asteroid:
    def __init__(self):
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)
        self.dx = random.uniform(-2, 2)
        self.dy = random.uniform(-2, 2)
        self.size = 30

    def move(self):
        self.x += self.dx
        self.y += self.dy
        if self.x < 0: self.x += width
        if self.x > width: self.x -= width
        if self.y < 0: self.y += height
        if self.y > height: self.y -= height

    def draw(self):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.size)

ship = Ship()
asteroids = [Asteroid() for _ in range(5)]
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ship.angle += 5
    if keys[pygame.K_RIGHT]:
        ship.angle -= 5
    if keys[pygame.K_UP]:
        ship.speed = 5
        ship.dx = ship.speed * math.cos(math.radians(ship.angle))
        ship.dy = -ship.speed * math.sin(math.radians(ship.angle))
    else:
        ship.speed = 0
        ship.dx = ship.dy = 0

    # Update
    ship.move()
    for asteroid in asteroids:
        asteroid.move()

    # Draw
    screen.fill((0, 0, 0))
    ship.draw()
    for asteroid in asteroids:
        asteroid.draw()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
