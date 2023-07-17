import pygame
import settings
from pygame.sprite import Sprite


class Alien(Sprite):
    """ Класс, представляющий одного пришельца"""
    def __init__(self, ai_game):
        """ Иициализирует пришельца и задает его начальную позицию"""
        super(Alien, self).__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Загрузка изображения пришельца и назначение атрибута rect
        self.scale = (120, 60)
        self.image = pygame.transform.scale(
            pygame.image.load(f"images/ai.png"),
            self.scale,
        )

        self.rect = self.image.get_rect()

        # Каждый новый пришелец повляется в левом верхнем углу экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранени точной горизонтальной позиции пришельца
        self.x = float(self.rect.x)

    def check_edges(self):
        """ Возвращает True, если пришелец находится у края экрана """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
    def update(self):
        """ Перемещает пришельца влево или вправо"""
        self.x += (self.settings.alien_speed_facctor * self.settings.fleet_direction)
        # print(self.image.get_rect())
        self.rect.x = self.x

