import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    # Класс для управления кораблем
    def __init__(self, ai_game):
        """ Инициализиует корабль и задает его начальнную позицию"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load("images/4.bmp")
        self.rect = self.image.get_rect()

        # Каждый новый корабль появляется у нижнего края экрана
        self.rect.midbottom = self.screen_rect.midbottom

        # Сохранение вещественной координаты центра корабля
        self.x = float(self.rect.x)
        self.y = self.rect.y
        # Флаг перемещения
        self.moving_right = False
        self.moving_left = False
        self.moving_forward = False
        self.moving_backward = False

    def update(self):
        """Обновляет позицию корабля с учетом флагов"""
        # Обновляется атрибут x объекта ship, а не rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        if self.moving_forward and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_backward and self.rect.bottom < self.settings.screen_height:
            self.y += self.settings.ship_speed
        # Обновление атрибута rect на основании self.x
        self.rect.x = self.x
        self.rect.y = self.y
    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """ Размещает корабль в центре нижней стороны"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.x)





