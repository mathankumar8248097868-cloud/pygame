import pygame
import math
import random
from dataclasses import dataclass
from typing import Tuple

pygame.init()

# ====================== CONFIG ======================
@dataclass
class Config:
    SCREEN_WIDTH: int = 900
    SCREEN_HEIGHT: int = 500
    FPS: int = 60
    TITLE: str = "TAPLE TEENI"

    # Table
    TABLE_COLOR: Tuple = (0, 100, 0)      # Dark green
    LINE_COLOR: Tuple = (255, 255, 255)   # White lines
    NET_HEIGHT: int = 80
    NET_WIDTH: int = 6

    # Paddles
    PADDLE_WIDTH: int = 15
    PADDLE_HEIGHT: int = 100
    PADDLE_SPEED: float = 7.0
    P1_COLOR: Tuple = (255, 50, 50)        # Red
    P2_COLOR: Tuple = (50, 50, 255)        # Blue

    # Ball
    BALL_RADIUS: int = 10
    BALL_COLOR: Tuple = (255, 255, 255)
    BALL_SPEED_X: float = 6.0
    BALL_SPEED_Y_MAX: float = 8.0

    # Scoring
    WIN_SCORE: int = 11
    FONT_NAME: str = "consolas"

    # AI Difficulty (0.0 to 1.0, where 1.0 is perfect tracking)
    AI_DIFFICULTY: float = 0.85  # New: Added AI difficulty parameter

config = Config()

# ====================== BUTTON CLASS ======================
class Button:
    def __init__(self, x, y, w, h, text, action):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.action = action
        self.hovered = False
        self.font = pygame.font.SysFont(config.FONT_NAME, 32, bold=True)

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, screen):
        color = (100, 200, 100) if self.hovered else (70, 150, 70)
        pygame.draw.rect(screen, color, self.rect, border_radius=15)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 4, border_radius=15)
        txt = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    def click(self):
        if self.hovered:
            self.action()

# ====================== BALL CLASS ======================
class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = config.SCREEN_WIDTH // 2
        self.y = config.SCREEN_HEIGHT // 2
        angle = random.uniform(-45, 45)
        if random.random() > 0.5:
            angle += 180
        rad = math.radians(angle)
        self.vx = config.BALL_SPEED_X * math.copysign(1, math.cos(rad))
        self.vy = config.BALL_SPEED_Y_MAX * math.sin(rad) * 0.8

    def update(self, p1, p2):
        self.x += self.vx
        self.y += self.vy

        # Top/Bottom bounce
        if self.y - config.BALL_RADIUS <= 80 or self.y + config.BALL_RADIUS >= config.SCREEN_HEIGHT - 50:
            self.vy = -self.vy
            self.y = max(80 + config.BALL_RADIUS, min(config.SCREEN_HEIGHT - 50 - config.BALL_RADIUS, self.y))

        # Paddle collision
        if self.x - config.BALL_RADIUS <= p1.x + config.PADDLE_WIDTH and \
           p1.y - config.PADDLE_HEIGHT//2 <= self.y <= p1.y + config.PADDLE_HEIGHT//2:
            if self.vx < 0:
                self.vx = -self.vx * 1.05
                rel_y = (self.y - p1.y) / (config.PADDLE_HEIGHT // 2)
                self.vy = rel_y * config.BALL_SPEED_Y_MAX
                self.x = p1.x + config.PADDLE_WIDTH + config.BALL_RADIUS

        if self.x + config.BALL_RADIUS >= p2.x and \
           p2.y - config.PADDLE_HEIGHT//2 <= self.y <= p2.y + config.PADDLE_HEIGHT//2:
            if self.vx > 0:
                self.vx = -self.vx * 1.05
                rel_y = (self.y - p2.y) / (config.PADDLE_HEIGHT // 2)
                self.vy = rel_y * config.BALL_SPEED_Y_MAX
                self.x = p2.x - config.BALL_RADIUS

        # Score
        if self.x < 0:
            return "p2"
        if self.x > config.SCREEN_WIDTH:
            return "p1"
        return None

    def draw(self, screen):
        pygame.draw.circle(screen, config.BALL_COLOR, (int(self.x), int(self.y)), config.BALL_RADIUS)
        # Glow
        pygame.draw.circle(screen, (*config.BALL_COLOR, 80), (int(self.x), int(self.y)), config.BALL_RADIUS + 8, 2)

# ====================== PADDLE CLASS ======================
class Paddle:
    def __init__(self, x, color, is_ai=False):  # Modified: Added is_ai parameter
        self.x = x
        self.y = config.SCREEN_HEIGHT // 2
        self.color = color
        self.is_ai = is_ai  # New: Flag to indicate AI control

    def update(self, up_key=None, down_key=None, ball=None):  # Modified: Added ball parameter
        if self.is_ai:
            # AI logic: Move toward the ball's y position when the ball is coming toward the paddle
            if ball and ball.vx < 0:  # Only move if ball is moving toward P1
                target_y = ball.y
                # Introduce some randomness to make AI less perfect
                target_y += random.uniform(-20, 20) * (1 - config.AI_DIFFICULTY)
                # Smoothly move toward the target y position
                if self.y < target_y and self.y < config.SCREEN_HEIGHT - 50 - config.PADDLE_HEIGHT // 2:
                    self.y += config.PADDLE_SPEED * config.AI_DIFFICULTY
                elif self.y > target_y and self.y > 80 + config.PADDLE_HEIGHT // 2:
                    self.y -= config.PADDLE_SPEED * config.AI_DIFFICULTY
        else:
            # Human control
            keys = pygame.key.get_pressed()
            if keys[up_key] and self.y > 80 + config.PADDLE_HEIGHT // 2:
                self.y -= config.PADDLE_SPEED
            if keys[down_key] and self.y < config.SCREEN_HEIGHT - 50 - config.PADDLE_HEIGHT // 2:
                self.y += config.PADDLE_SPEED

    def draw(self, screen):
        rect = pygame.Rect(
            self.x - config.PADDLE_WIDTH // 2,
            self.y - config.PADDLE_HEIGHT // 2,
            config.PADDLE_WIDTH,
            config.PADDLE_HEIGHT
        )
        pygame.draw.rect(screen, self.color, rect, border_radius=8)
        pygame.draw.rect(screen, (255, 255, 255), rect, 3, border_radius=8)

# ====================== GAME CLASS ======================
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption(config.TITLE)
        self.clock = pygame.time.Clock()
        self.font_big = pygame.font.SysFont(config.FONT_NAME, 72, bold=True)
        self.font_small = pygame.font.SysFont(config.FONT_NAME, 36)
        self.reset()

        # Restart Button
        btn_w, btn_h = 220, 70
        self.restart_btn = Button(
            config.SCREEN_WIDTH // 2 - btn_w // 2,
            config.SCREEN_HEIGHT // 2 + 60,
            btn_w, btn_h,
            "RESTART",
            self.reset
        )

    def reset(self):
        self.p1 = Paddle(100, config.P1_COLOR, is_ai=True)  # Modified: P1 is AI
        self.p2 = Paddle(config.SCREEN_WIDTH - 100, config.P2_COLOR, is_ai=False)  # Modified: P2 is human
        self.ball = Ball()
        self.score_p1 = 0
        self.score_p2 = 0
        self.winner = None

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and self.winner:
                if event.button == 1:
                    self.restart_btn.click()
        self.restart_btn.update(mouse_pos)
        return True

    def update(self):
        if self.winner:
            return

        self.p1.update(ball=self.ball)  # Modified: Pass ball to P1 for AI control
        self.p2.update(pygame.K_UP, pygame.K_DOWN)  # Modified: P2 uses keyboard controls

        result = self.ball.update(self.p1, self.p2)
        if result == "p1":
            self.score_p1 += 1
            self.ball.reset()
        elif result == "p2":
            self.score_p2 += 1
            self.ball.reset()

        if self.score_p1 >= config.WIN_SCORE:
            self.winner = "AI Player"  # Modified: Reflect AI as P1
        elif self.score_p2 >= config.WIN_SCORE:
            self.winner = "Player 2"

    def draw_table(self):
        # Background
        self.screen.fill((20, 50, 20))

        # Table
        table_rect = pygame.Rect(50, 80, config.SCREEN_WIDTH - 100, config.SCREEN_HEIGHT - 130)
        pygame.draw.rect(self.screen, config.TABLE_COLOR, table_rect)
        pygame.draw.rect(self.screen, config.LINE_COLOR, table_rect, 5)

        # Center line
        center_x = config.SCREEN_WIDTH // 2
        pygame.draw.line(self.screen, config.LINE_COLOR, (center_x, 80), (center_x, config.SCREEN_HEIGHT - 50), 3)

        # Net
        net_y = config.SCREEN_HEIGHT // 2 - config.NET_HEIGHT // 2
        pygame.draw.rect(self.screen, (200, 200, 200),
                         (center_x - config.NET_WIDTH // 2, net_y, config.NET_WIDTH, config.NET_HEIGHT))

    def draw(self):
        self.draw_table()

        self.p1.draw(self.screen)
        self.p2.draw(self.screen)
        self.ball.draw(self.screen)

        # Score
        s1 = self.font_big.render(str(self.score_p1), True, config.P1_COLOR)
        s2 = self.font_big.render(str(self.score_p2), True, config.P2_COLOR)
        self.screen.blit(s1, (config.SCREEN_WIDTH // 4, 20))
        self.screen.blit(s2, (3 * config.SCREEN_WIDTH // 4 - s2.get_width(), 20))

        # Player labels
        p1_label = self.font_small.render("AI", True, config.P1_COLOR)  # Modified: Label P1 as AI
        p2_label = self.font_small.render("P2", True, config.P2_COLOR)
        self.screen.blit(p1_label, (config.SCREEN_WIDTH // 4, 80))
        self.screen.blit(p2_label, (3 * config.SCREEN_WIDTH // 4 - 50, 80))

        # Win screen
        if self.winner:
            win_text = self.font_big.render(f"{self.winner} WINS!", True, (255, 215, 0))
            self.screen.blit(win_text, win_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 50)))
            self.restart_btn.draw(self.screen)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(config.FPS)
        pygame.quit()

# ====================== RUN ======================
if __name__ == "__main__":
    Game().run()
