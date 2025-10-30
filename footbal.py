import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2-Player Football Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 180, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Player settings
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_SPEED = 5
KICK_POWER = 12

# Ball settings
BALL_RADIUS = 15
ball_speed_x = 0
ball_speed_y = 0

# Goal settings
GOAL_WIDTH = 100
GOAL_HEIGHT = 200
GOAL_DEPTH = 40

# Fonts
font = pygame.font.SysFont("Arial", 48)

# Player 1 (Blue - Left Side)
player1_x = 100
player1_y = HEIGHT // 2 - PLAYER_HEIGHT // 2
player1_score = 0

# Player 2 (Red - Right Side)
player2_x = WIDTH - 100 - PLAYER_WIDTH
player2_y = HEIGHT // 2 - PLAYER_HEIGHT // 2
player2_score = 0

# Ball
ball_x = WIDTH // 2
ball_y = HEIGHT // 2

# Game states
game_active = True

# Reset ball function
def reset_ball():
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_speed_x = random.choice([-7, 7])
    ball_speed_y = random.choice([-7, 7])

# Initial ball kick
reset_ball()

# Main game loop
running = True
while running:
    screen.fill(GREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    if game_active:
        keys = pygame.key.get_pressed()

        # Player 1 Controls (WASD)
        if keys[pygame.K_w] and player1_y > 0:
            player1_y -= PLAYER_SPEED
        if keys[pygame.K_s] and player1_y < HEIGHT - PLAYER_HEIGHT:
            player1_y += PLAYER_SPEED
        if keys[pygame.K_a] and player1_x > 0:
            player1_x -= PLAYER_SPEED
        if keys[pygame.K_d] and player1_x < WIDTH // 2 - PLAYER_WIDTH:
            player1_x += PLAYER_SPEED

        # Player 2 Controls (Arrow Keys)
        if keys[pygame.K_UP] and player2_y > 0:
            player2_y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and player2_y < HEIGHT - PLAYER_HEIGHT:
            player2_y += PLAYER_SPEED
        if keys[pygame.K_LEFT] and player2_x > WIDTH // 2:
            player2_x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and player2_x < WIDTH - PLAYER_WIDTH:
            player2_x += PLAYER_SPEED

        # Ball movement
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Ball collision with top/bottom
        if ball_y <= BALL_RADIUS or ball_y >= HEIGHT - BALL_RADIUS:
            ball_speed_y *= -1

        # Ball collision with players
        # Player 1
        p1_rect = pygame.Rect(player1_x, player1_y, PLAYER_WIDTH, PLAYER_HEIGHT)
        ball_rect = pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
        if p1_rect.colliderect(ball_rect):
            # Kick logic
            dx = ball_x - (player1_x + PLAYER_WIDTH // 2)
            dy = ball_y - (player1_y + PLAYER_HEIGHT // 2)
            ball_speed_x = dx * 0.3
            ball_speed_y = dy * 0.3
            if abs(ball_speed_x) < 3:
                ball_speed_x = 3 if dx > 0 else -3
            if abs(ball_speed_y) < 3:
                ball_speed_y = 3 if dy > 0 else -3

        # Player 2
        p2_rect = pygame.Rect(player2_x, player2_y, PLAYER_WIDTH, PLAYER_HEIGHT)
        if p2_rect.colliderect(ball_rect):
            dx = ball_x - (player2_x + PLAYER_WIDTH // 2)
            dy = ball_y - (player2_y + PLAYER_HEIGHT // 2)
            ball_speed_x = dx * 0.3
            ball_speed_y = dy * 0.3
            if abs(ball_speed_x) < 3:
                ball_speed_x = 3 if dx > 0 else -3
            if abs(ball_speed_y) < 3:
                ball_speed_y = 3 if dy > 0 else -3

        # Goal detection (Left goal for Player 2)
        left_goal = pygame.Rect(0, HEIGHT//2 - GOAL_HEIGHT//2, GOAL_DEPTH, GOAL_HEIGHT)
        if left_goal.colliderect(ball_rect):
            player2_score += 1
            reset_ball()

        # Right goal for Player 1
        right_goal = pygame.Rect(WIDTH - GOAL_DEPTH, HEIGHT//2 - GOAL_HEIGHT//2, GOAL_DEPTH, GOAL_HEIGHT)
        if right_goal.colliderect(ball_rect):
            player1_score += 1
            reset_ball()

        # Ball out of bounds (side)
        if ball_x < -50:
            player2_score += 1
            reset_ball()
        if ball_x > WIDTH + 50:
            player1_score += 1
            reset_ball()

        # Draw field
        pygame.draw.line(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 3)
        pygame.draw.circle(screen, WHITE, (WIDTH//2, HEIGHT//2), 80, 3)

        # Draw goals
        pygame.draw.rect(screen, WHITE, left_goal, 3)
        pygame.draw.rect(screen, WHITE, right_goal, 3)

        # Draw players
        pygame.draw.rect(screen, BLUE, (player1_x, player1_y, PLAYER_WIDTH, PLAYER_HEIGHT))
        pygame.draw.rect(screen, RED, (player2_x, player2_y, PLAYER_WIDTH, PLAYER_HEIGHT))

        # Draw ball
        pygame.draw.circle(screen, YELLOW, (int(ball_x), int(ball_y)), BALL_RADIUS)

        # Draw score
        score_text = font.render(f"{player1_score} - {player2_score}", True, WHITE)
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))

        # Instructions
        small_font = pygame.font.SysFont("Arial", 24)
        p1_text = small_font.render("Player 1: WASD", True, WHITE)
        p2_text = small_font.render("Player 2: Arrows", True, WHITE)
        screen.blit(p1_text, (20, HEIGHT - 40))
        screen.blit(p2_text, (WIDTH - p2_text.get_width() - 20, HEIGHT - 40))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
