# enemy.py
import pygame
import random
from .settings import WIDTH, HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_IMAGE

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        # Cargar la imagen, escalarla y asignarla a self.image
        self.image = pygame.transform.scale(pygame.image.load(ENEMY_IMAGE).convert_alpha(), (ENEMY_WIDTH//3, ENEMY_HEIGHT//3))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:  # Cuando el enemigo pasa el borde inferior
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
