import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scorebord
from button import Button
from ship import Ship
from boom import Boom
from bullet import Bullet
from pygame.sprite import Group
from alien import Alien
from stars import Stars
from random import Random



class AlienInvasion:
    """Класс для управления ресурсами и поведением игры"""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы"""

        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, vsync=1)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Создание экземпляра для хранения игровой статистики
        # и панели резльтатов
        self.stats = GameStats(self)
        self.sb = Scorebord(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()

        self._create_fleet()
        self._create_stars(200)

        #Создание кнопки Play
        self.play_button = Button(self, "Play")

#       self.screen = pygame.display.set_mode((1200, 800))
#       pygame.display.set_caption("Alien Invasion")
#       # Назначение цвета фона
#       self.bg_color = (97, 153, 059)

    def run_game(self):
        """Запуск основного цикла игры"""
        while True:
            self._check_events()  # При каждом проходе цикла перерысовывается экран

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self.stars.update()
                if not self.aliens:
                    self.settings.increase_speed()
                    # Увеличение уровня
                    self.stats.level += 1
                    self.sb.prep_level()
                    self._create_fleet()
            self._update_screen()

    def _check_events(self):
        # Обрабатывает нажатия клавиш и слбытия мыши
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        """ Запускает новую игру при нажатии кнопки Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Сброс игровых настроек
            self.settings.initialize_dynamic_settings()
            # Указатель мыши скрывается
            pygame.mouse.set_visible(False)
            # Сброс игровой статистики
            self.stats.reset_stats()
            self.stats.game_active = True
            # Очистка списков пришшельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()
            # Создание нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()
            self.sb.prep_score()    # Метод prep_score() вызывается при сбросе игровой статистики в начале новой игры. Счет, выводимый на экран, обнуляется.
            self.sb.prep_level()
            self.sb.prep_ships()


    def _check_keydown_events(self, event):
        """Регирует на нажатие клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_forward = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_backward = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Реагирует на отпускание  клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_forward = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_backward = False

    def _fire_bullet(self):
        """ Создание нового снаряда и вклюючение его в группу bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """ Обновляет позиции снарядов и унчтожает старые снаряды"""
        # Обновление позиции снарядов
        self.bullets.update()
        # Удалениее снарядов, вышедших за край экрана
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()
    def _check_bullet_alien_collisions(self):
        """ Обработкаа коллизий снарядов с пришельцами """
        # Проверка попаданий в пришельцев
        # При обнаружении попадания удалиить снаряд и пришельца
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )
        if collisions:  #При попадании снаряда в пришельца Pygame возвращает словарь collisions
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

    # В этом методе создается один экземпляр Alien, который затем добавляется в
    #группу для хранения флота.
    def _create_fleet(self):
        """Создание флота вторжения"""
        # Создание пришельца
        # Создание ппришельца и вычисление количества пришельцев в ряду
        #Интервал между соседними пришельцами равен ширине пришельца
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x = available_space_x // (2 * alien_width)

        """Определяет количество рядовб помещающихся на экране"""
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Создание флота вторжения
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                # Создание пришельца и размещение его в ряду
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """ Реагирует на достижение пишельцем края экрана"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _check_aliens_bottom(self):
        """ Проверяет, добрались ли пришельцы до нижнего края экрана"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Происходит то же, что при столкновении с кораблем
                self._ship_hit()
                break


    def _change_fleet_direction(self):
        """ Опускает весь флот и меняет направление флота"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """ Обрабатывает столкновение корабля с пришельцем"""
        if self.stats.ships_left > 0:
            # Уменьшение ship_left и обновление панели счета
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # Очистка списков пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()
            # Создание нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()
            # Пауза
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_aliens(self):
        """ Обновляет позиции всех пришельцев во флоте"""
        self._check_fleet_edges()
        self.aliens.update()    # Мы используем метод update() для группы aliens, что приводит к автоматическому вызову метода update() каждого пришельца.
        # Проверка коллизий "пришелец - корабль"
        if pygame.sprite.spritecollideany(self.ship, self.aliens):  # Функция spritecollideany() получает два аргумента: спрайт и грппу
            self._ship_hit()
        # Проверить, добрались ли пришельцы до нижнего края экрана
        self._check_aliens_bottom()


    def _create_stars(self, star_number):
        for star in range(star_number):
            star = Stars(self)
            self.stars.add(star)



    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран"""
        # При каждом проходе цикла перерисовывается экран
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Вывод информациии о счете
        self.sb.show_score()

        # Кнопка Play отображается в том случае, если  игра неактивна
        if not self.stats.game_active:
            self.play_button.draw_button()
        for star in self.stars:
            star.draw(self.screen)
        # Отслеживание последнего прорисованного экрана
        pygame.display.flip()

if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()