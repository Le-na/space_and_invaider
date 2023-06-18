class Settings():
    """Класс для хранения всех настроек игры Alien Invasion"""
    def __init__(self):
        """Инициализирует настройки игры"""
        #Параметры экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (107, 107, 127)
        # Настройки корабля
        self.ship_speed = 1.5 # смещение корабля на 1,5 пикселя вместо 1
