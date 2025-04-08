import pygame
import random

SCORE_OF_SUN = 100
MIN_Y_SPEED = 1
MAX_Y_SPEED = 4

class Sun:
    def __init__(self, screen_ref: pygame.Surface):
        self.screen_ref = screen_ref
        self.speed = random.randint(MIN_Y_SPEED, MAX_Y_SPEED)
        self.image = pygame.transform.scale(pygame.image.load(r"C:\Users\Sadovnik\.vscode\.venv\Python-files\Calmer_Game\Sun.jpg"), (100, 100))
        self.score = SCORE_OF_SUN + SCORE_OF_SUN * 0.1 * self.speed

        self.sun_rect = self.image.get_rect()
        self.sun_rect.x = random.randint(self.sun_rect.width, screen_ref.get_width() - self.sun_rect.width)
        self.sun_rect.y = -100
    def move_sun_down(self):
        self.sun_rect.y += self.speed
        if(self.sun_rect.y > self.screen_ref.get_height() // 2):
            self.score = SCORE_OF_SUN // 2
    