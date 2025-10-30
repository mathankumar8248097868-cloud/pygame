import pygame

pygame.init()
width, height = 700, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong")

# Paddles and ball
paddle_a = pygame.Rect(50, height//2 - 70, 10, 140)
paddle_b = pygame.Rect(width - 60, height//2 - 70, 10, 140)
ball = pygame.Rect(width//2 - 15, height//2 - 15, 30, 30)
ball_speed_x, ball_speed_y = 7, 7

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move paddles
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle_a.top > 0:
        paddle_a.y -= 5
    if keys[pygame.K_s] and paddle_a.bottom < height:
        paddle_a.y += 5
    if keys[pygame.K_UP] and paddle_b.top > 0:
        paddle_b.y -= 5
    if keys[pygame.K_DOWN] and paddle_b.bottom < height:
        paddle_b.y += 5

    # Move ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collisions
    if ball.top <= 0 or ball.bottom >= height:
        ball_speed_y *= -1
    if ball.colliderect(paddle_a) or ball.colliderect(paddle_b):
        ball_speed_x *= -1

    # Reset ball if out of bounds
    if ball.left <= 0 or ball.right >= width:
        ball.center = (width//2, height//2)
        ball_speed_x *= -1

    # Draw
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), paddle_a)
    pygame.draw.rect(screen, (255, 255, 255), paddle_b)
    pygame.draw.ellipse(screen, (255, 255, 255), ball)
    pygame.draw.aaline(screen, (255, 255, 255), (width//2, 0), (width//2, height))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
