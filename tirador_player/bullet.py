# bullet.py
import pygame
from .settings import GREEN, BULLET_SPEED, BULLET_IMAGE, BULLET_WIDTH, BULLET_HEIGHT

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Cargar la imagen y escalarla usando las dimensiones BULLET_WIDTH y BULLET_HEIGHT
        self.image = pygame.transform.scale(pygame.image.load(BULLET_IMAGE).convert_alpha(), (BULLET_WIDTH//3, BULLET_HEIGHT//3))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self):
        self.rect.y += BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()
