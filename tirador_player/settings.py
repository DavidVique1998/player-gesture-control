# settings.py

# Dimensiones de la pantalla
WIDTH = 800
HEIGHT = 600

# Dimensiones enemigo
ENEMY_WIDTH = 377
ENEMY_HEIGHT = 216


# Dimensiones jugador
PLAYER_WIDTH = 197
PLAYER_HEIGHT = 249

# dmensiones bala
BULLET_WIDTH =  80
BULLET_HEIGHT = 85


# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Velocidad de la bala
BULLET_SPEED = -10  # Velocidad negativa para que la bala se mueva hacia arriba

# Niveles y fondos
LEVELS = {
    1: {"score_threshold": 10, "background": "background1.jpeg", "enemy_speed": 3},
    2: {"score_threshold": 20, "background": "background2.jpeg", "enemy_speed": 5},
    3: {"score_threshold": 30, "background": "background3.jpeg", "enemy_speed": 7}
}

# Enemy image
ENEMY_IMAGE = "enemy.png"

# Player image
PLAYER_IMAGE = "player.png"

# Bullet image
BULLET_IMAGE = "bullet.png"

# Frames por segundo
FPS = 60
