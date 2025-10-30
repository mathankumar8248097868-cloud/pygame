import pygame
import random

pygame.init()
width, height = 300, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tetris")

# Grid
grid = [[0] * 10 for _ in range(20)]
block_size = 30

# Tetromino shapes
shapes = [
    [[1, 1, 1, 1]], # I
    [[1, 1], [1, 1]], # O
    [[1, 1, 1], [0, 1, 0]] # T
]

class Tetromino:
    def __init__(self):
        self.shape = random.choice(shapes)
        self.x = 3
        self.y = 0

    def move_down(self):
        self.y += 1
        if self.check_collision():
            self.y -= 1
            return False
        return True

    def move_left(self):
        self.x -= 1
        if self.check_collision():
            self.x += 1

    def move_right(self):
        self.x += 1
        if self.check_collision():
            self.x -= 1

    def check_collision(self):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[0])):
                if self.shape[i][j]:
                    if (self.y + i >= 20 or
                        self.x + j < 0 or
                        self.x + j >= 10 or
                        grid[self.y + i][self.x + j]):
                        return True
        return False

    def draw(self):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[0])):
                if self.shape[i][j]:
                    pygame.draw.rect(screen, (255, 255, 255),
                                    (self.x * block_size + j * block_size,
                                     self.y * block_size + i * block_size,
                                     block_size, block_size))

# Game loop
current_piece = Tetromino()
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_piece.move_left()
            if event.key == pygame.K_RIGHT:
                current_piece.move_right()

    # Move piece down
    if not current_piece.move_down():
        for i in range(len(current_piece.shape)):
            for j in range(len(current_piece.shape[0])):
                if current_piece.shape[i][j]:
                    grid[current_piece.y + i][current_piece.x + j] = 1
        current_piece = Tetromino()

    # Draw
    screen.fill((0, 0, 0))
    for i in range(20):
        for j in range(10):
            if grid[i][j]:
                pygame.draw.rect(screen, (255, 255, 255),
                                (j * block_size, i * block_size, block_size, block_size))
    current_piece.draw()
    pygame.display.flip()
    clock.tick(5)

pygame.quit()
