import time
import pygame

class Boom(pygame.sprite.Sprite):
    def __init__(self, game, sprite):
        super(Boom, self).__init__()
        self.game = game.screen
        self.screen = game.screen

        self.scale = (max(sprite.rect.size), max(sprite.rect.size))
        self.sprites = [
            pygame.transform.scale(
                pygame.image.load(f"images/boom_{i}.png"),
                self.scale
            )
            for i in range(1, 6)
        ]
        self.image = self.sprites[0]
        self.rect = self.sprites[0].get_rect()

        self.last_sprite = 0
        self.last_sprite_changed = time.time()

        self.rect.midbottom = sprite.rect.midbottom

        self.sound_boom = pygame.mixer.Sound("./sounds/boom1.wav")
        pygame.mixer.Sound.play(self.sound_boom)
        self.evict = False

    def next_sprite(self):
        if self.last_sprite >= len(self.sprites):
            self.evict = True
            pygame.mixer.music.stop()
        elif time.time() - self.last_sprite_changed > 0.1:
            self.last_sprite += 1
            self.last_sprite_changed = time.time()
        self.image = self.sprites[self.last_sprite -1]

    def blitme(self):
        if self.evict:
            self.kill()
        self.next_sprite()
        self.screen.blit(self.image, self.rect)