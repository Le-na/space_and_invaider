import pygame
import settings
import sys
from pygame.sprite import Sprite
from random import choice, randint, uniform
import time

COLORS = (
    (255,0,0), # red
    (0,255,0), # green
    (0,0,255), # blue
)

class Stars(Sprite):
    """Класс в котором рисуется 1 звезда"""
    def __init__(self, ai_game):
        super(Stars, self).__init__()
        """ Инициализирует звезду и задает ее изначальную позицию"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = None
        self.size = randint(1, 3)
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.color = choice(COLORS)
        self.rect.x = randint(0, self.settings.screen_width)
        self.rect.y = randint(0, self.settings.screen_height)
        self.last_update = time.time()
        self.update_time_diff = uniform(0, 0.2)
        self.last_flap_time = time.time()
        self.flap_time_diff = uniform(0.4, 5)
        self.shine = True
    def update(self):
        """ Переммещает звезду вних по экрану"""
        # Обновление позиции прямоугольника
        if time.time() - self.last_update > self.update_time_diff:
            self.rect.y += self.settings.stars_speed
            if self.rect.y == self.settings.screen_height:
                self.rect.y = 0
            self.last_update = time.time()
    def draw(self, screen):
        """ Вывод снарряда на экран"""
        if time.time() - self.last_flap_time > self.flap_time_diff:
            self.shine = not self.shine
            self.last_flap_time = time.time()
        if self.shine:
            pygame.draw.rect(self.screen, self.color, self.rect)







