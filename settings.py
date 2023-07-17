class Settings():
    """Класс для хранения всех настроек игры Alien Invasion"""
    def __init__(self):
        """Инициализирует настройки игры"""
        #Параметры экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)     #(107, 107, 127)
        # Настройки корабля
        self.ship_speed = 4   # смещение корабля на 1,5 пикселя вместо 1
        self.ship_limit = 3
        # Параметры снаряда
        self.bullet_speed = 7
        self.bullet_widht = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3    # Ограничение количества снарядов до 3х одновременно
        # Настройка пришельца (Настройка используется в реализации update():)
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet_direction = 1 обозначает движение вправо; а -1 - влево
        self.fleet_direction = 1
        # Настройка зввезды
        self.stars_speed = 1
        # Темп ускорения игры
        self.speedup_scale = 1.1
        # Темп роста стоимости пришельцев
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """ Инициализирует настройки. изменяющиеся в ходе игры"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3.0
        self.alien_speed_facctor = 1.0
        #fleet_direction = 1 обозначает движение вправо; а -1 - влевво
        self.fleet_direction = 1
        # Подсчет очков
        self.alien_points = 50

    def increase_speed(self):
        """ Увеличивает настройки скорости и стоимости пришельцев"""
        self.ship_speed_factor += self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_facctor *= self.speedup_scale
        # print(self.alien_points)
        self.alien_points = int(self.alien_points * self.score_scale)

