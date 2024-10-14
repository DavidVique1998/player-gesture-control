# player.py
import pygame
from .bullet import Bullet
from .settings import WHITE, WIDTH, HEIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, move_left, move_right, shoot_key, color=WHITE):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.move_left = move_left
        self.move_right = move_right
        self.shoot_key = shoot_key
        self.lives = 3  # Inicializamos con 3 vidas

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[self.move_left]:
            self.rect.x -= 5
        if keys[self.move_right]:
            self.rect.x += 5

    # Método para mover a la izquierda
    def m_move_left(self):
        self.rect.x -= 5

    # Método para mover a la derecha
    def m_move_right(self):
        self.rect.x += 5
    
    def fire(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        return bullet

    def lose_life(self):
        self.lives -= 1  # Reducir una vida
        if self.lives < 0:
            self.lives = 0  # Evitar que las vidas sean negativas