"""
Dual Blasters – 2-Player Top-Down Shooter
With Clickable RESTART Button
"""

import pygame
import math
from dataclasses import dataclass
from typing import List, Tuple

pygame.init()

# ====================== CONFIG ======================
@dataclass
class Config:
    SCREEN_WIDTH: int = 800
    SCREEN_HEIGHT: int = 600
    FPS: int = 60
    TITLE: str = "Dual Blasters"

    PLAYER_SIZE: int = 25
    PLAYER_SPEED: float = 5.0
    BULLET_SPEED: float = 10.0
    BULLET_RADIUS: int = 5
    BULLET_LIFETIME: int = 40
    SHOOT_COOLDOWN: int = 15

    P1_COLOR: Tuple[int, int, int] = (255, 50, 50)
    P2_COLOR: Tuple[int, int, int] = (50, 50, 255)
    BULLET_P1_COLOR: Tuple[int, int, int] = (255, 100, 100)
    BULLET_P2_COLOR: Tuple[int, int, int] = (100, 100, 255)
    WALL_COLOR: Tuple[int, int, int] = (100, 100, 100)
    BG_COLOR: Tuple[int, int, int] = (30, 30, 30)

    START_LIVES: int = 3

config = Config()

# ====================== BUTTON CLASS ======================
class Button:
    def __init__(self, x, y, width, height, text, font, color, hover_color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.hovered = False

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, screen):
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 3, border_radius=12)

        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def click(self):
        if self.hovered:
            self.action()

# ====================== VECTOR HELPERS ======================
def angle_to_vector(angle):
    rad = math.radians(angle)
    return math.cos(rad), math.sin(rad)

# ====================== PLAYER CLASS ======================
class Player:
    def __init__(self, x, y, color, controls):
        self.rect = pygame.Rect(x, y, config.PLAYER_SIZE, config.PLAYER_SIZE)
        self.color = color
        self.controls = controls
        self.angle = 0
        self.lives = config.START_LIVES
        self.shoot_cooldown = 0

    def handle_input(self, keys):
        dx = dy = 0
        if keys[self.controls['up']]: dy -= config.PLAYER_SPEED
        if keys[self.controls['down']]: dy += config.PLAYER_SPEED
        if keys[self.controls['left']]: dx -= config.PLAYER_SPEED
        if keys[self.controls['right']]: dx += config.PLAYER_SPEED

        self.rect.x += dx
        self.rect.y += dy

        self.rect.x = max(50, min(config.SCREEN_WIDTH - 50 - self.rect.width, self.rect.x))
        self.rect.y = max(50, min(config.SCREEN_HEIGHT - 50 - self.rect.height, self.rect.y))

        self.shoot_cooldown = max(0, self.shoot_cooldown - 1)
        if keys[self.controls['shoot']] and self.shoot_cooldown == 0:
            self.shoot_cooldown = config.SHOOT_COOLDOWN
            return True
        return False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        cx, cy = self.rect.center
        dx, dy = angle_to_vector(self.angle)
        end_x = cx + dx * 30
        end_y = cy + dy * 30
        pygame.draw.line(screen, (255, 255, 255), (cx, cy), (end_x, end_y), 4)

        for i in range(self.lives):
            pygame.draw.circle(screen, self.color,
                               (50 + i * 20, 50 if self.color == config.P1_COLOR else config.SCREEN_HEIGHT - 50), 8)

# ====================== BULLET CLASS ======================
class Bullet:
    def __init__(self, x, y, angle, color):
        self.x = x
        self.y = y
        self.angle = angle
        self.color = color
        self.lifetime = config.BULLET_LIFETIME
        dx, dy = angle_to_vector(angle)
        self.vx = dx * config.BULLET_SPEED
        self.vy = dy * config.BULLET_SPEED

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        return (self.x < 0 or self.x > config.SCREEN_WIDTH or
                self.y < 0 or self.y > config.SCREEN_HEIGHT or
                self.lifetime <= 0)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), config.BULLET_RADIUS)

    def collides_with(self, player: Player):
        dx = self.x - player.rect.centerx
        dy = self.y - player.rect.centery
        return math.hypot(dx, dy) < config.PLAYER_SIZE

# ====================== GAME CLASS ======================
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption(config.TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 40, bold=True)
        self.small_font = pygame.font.SysFont("arial", 28, bold=True)
        self.button_font = pygame.font.SysFont("arial", 32, bold=True)
        self.reset()

        # Create Restart Button
        btn_w, btn_h = 200, 60
        btn_x = config.SCREEN_WIDTH // 2 - btn_w // 2
        btn_y = config.SCREEN_HEIGHT // 2 + 50
        self.restart_button = Button(
            btn_x, btn_y, btn_w, btn_h,
            "RESTART",
            self.button_font,
            (70, 130, 180),
            (100, 180, 255),
            self.reset
        )

    def reset(self):
        self.p1 = Player(100, config.SCREEN_HEIGHT // 2, config.P1_COLOR, {
            'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a,
            'right': pygame.K_d, 'shoot': pygame.K_f
        })
        self.p2 = Player(config.SCREEN_WIDTH - 150, config.SCREEN_HEIGHT // 2, config.P2_COLOR, {
            'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT, 'shoot': pygame.K_RETURN
        })
        self.bullets: List[Bullet] = []
        self.winner = None

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and self.winner:
                if event.button == 1:  # Left click
                    self.restart_button.click()
        return True

    def update(self):
        if self.winner:
            self.restart_button.update(pygame.mouse.get_pos())
            return

        keys = pygame.key.get_pressed()

        # Player 1
        if self.p1.handle_input(keys):
            cx, cy = self.p1.rect.center
            dx = self.p2.rect.centerx - cx
            dy = self.p2.rect.centery - cy
            self.p1.angle = math.degrees(math.atan2(dy, dx))
            self.bullets.append(Bullet(cx, cy, self.p1.angle, config.BULLET_P1_COLOR))

        # Player 2
        if self.p2.handle_input(keys):
            cx, cy = self.p2.rect.center
            dx = self.p1.rect.centerx - cx
            dy = self.p1.rect.centery - cy
            self.p2.angle = math.degrees(math.atan2(dy, dx))
            self.bullets.append(Bullet(cx, cy, self.p2.angle, config.BULLET_P2_COLOR))

        # Bullets
        for bullet in self.bullets[:]:
            if bullet.update():
                self.bullets.remove(bullet)
                continue
            if bullet.color == config.BULLET_P1_COLOR and bullet.collides_with(self.p2):
                self.p2.lives -= 1
                self.bullets.remove(bullet)
            elif bullet.color == config.BULLET_P2_COLOR and bullet.collides_with(self.p1):
                self.p1.lives -= 1
                self.bullets.remove(bullet)

        # Win
        if self.p1.lives <= 0:
            self.winner = "Player 2 (Blue)"
        elif self.p2.lives <= 0:
            self.winner = "Player 1 (Red)"

    def draw(self):
        self.screen.fill(config.BG_COLOR)

        # Walls
        wall = 20
        walls = [(0,0,config.SCREEN_WIDTH,wall),
                 (0,config.SCREEN_HEIGHT-wall,config.SCREEN_WIDTH,wall),
                 (0,0,wall,config.SCREEN_HEIGHT),
                 (config.SCREEN_WIDTH-wall,0,wall,config.SCREEN_HEIGHT)]
        for w in walls:
            pygame.draw.rect(self.screen, config.WALL_COLOR, w)

        # Players & Bullets
        self.p1.draw(self.screen)
        self.p2.draw(self.screen)
        for b in self.bullets:
            b.draw(self.screen)

        # HUD
        p1_text = self.small_font.render("P1", True, config.P1_COLOR)
        p2_text = self.small_font.render("P2", True, config.P2_COLOR)
        self.screen.blit(p1_text, (60, 20))
        self.screen.blit(p2_text, (config.SCREEN_WIDTH - 100, 20))

        # Game Over + Button
        if self.winner:
            win_text = self.font.render(f"{self.winner} WINS!", True, (255, 215, 0))
            self.screen.blit(win_text, win_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 50)))
            self.restart_button.draw(self.screen)

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
    game = Game()
    game.run()
