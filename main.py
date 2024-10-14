# main.py
import pygame
from tirador_player.player import Player
from tirador_player.bullet import Bullet
from tirador_player.enemy import Enemy
from tirador_player.utils import show_scores, show_lives, show_game_over
from tirador_player.settings import WIDTH, HEIGHT, FPS, WHITE, LEVELS
import cv2  # Importa la biblioteca OpenCV para procesamiento de video.
from gesture_detector.main import GestureDetector  # Importa la clase GestureDetector desde el módulo gesture_detector.main.

# Inicializar Pygame
pygame.init()

def run_game():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Juego de Tirador")
    clock = pygame.time.Clock()

    # Cargar imágenes de fondo
    backgrounds = {
        1: pygame.image.load(LEVELS[1]["background"]),
        2: pygame.image.load(LEVELS[2]["background"]),
        3: pygame.image.load(LEVELS[3]["background"])
    }
    current_background = backgrounds[1]  # Fondo inicial

    # Grupos de sprites
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    # Jugador 1 (Blanco, controla con gestos)
    player1 = Player(x=WIDTH // 2, y=HEIGHT - 50, move_left=pygame.K_LEFT, move_right=pygame.K_RIGHT, shoot_key=pygame.K_RETURN, color=WHITE)
    all_sprites.add(player1)

    # Crear enemigos iniciales
    enemy_speed = LEVELS[1]["enemy_speed"]  # Velocidad de los enemigos al iniciar
    for i in range(5):
        enemy = Enemy(speed=enemy_speed)  # Iniciar enemigos con la velocidad del nivel 1
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Inicializa el detector de gestos
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    hand_gesture = GestureDetector()

    # Variables del juego
    score1 = 0  # Puntaje del jugador 1
    running = True
    game_over = False
    current_level = 1  # Nivel inicial

    # Bucle principal del juego
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and not game_over:
                # Jugador 1 dispara con Enter
                if event.key == player1.shoot_key:
                    bullet = Bullet(player1.rect.centerx, player1.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)

        # Procesamiento del frame para detectar gestos
        ret, frame = cap.read()
        if ret:
            command, draw_frame = hand_gesture.gesture_interpretation(frame)
            cv2.imshow('Car gesture control', draw_frame)

            # Interpretar el comando del gesto para mover al jugador
            if command == 'I':
                player1.m_move_left()  # Mover a la izquierda
            elif command == 'D':
                player1.m_move_right()  # Mover a la derecha
            elif command == 'A':
                bullet = Bullet(player1.rect.centerx, player1.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
            elif command == 'P':
                player1.fire()  # Disparar

            # Si la tecla Esc (código 27) es presionada, romper el bucle
            if cv2.waitKey(5) == 27:
                running = False

        if not game_over:
            # Actualizar sprites
            all_sprites.update()

            # Colisiones entre balas y enemigos
            hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
            for hit in hits:
                score1 += 1  # Aumentar el puntaje del jugador 1
                # Crear nuevo enemigo con la velocidad actual
                enemy = Enemy(speed=enemy_speed)
                all_sprites.add(enemy)
                enemies.add(enemy)

            # Colisiones entre el jugador y los enemigos
            player1_hits = pygame.sprite.spritecollide(player1, enemies, False)

            if player1_hits:
                player1.lose_life()
                if player1.lives == 0:
                    game_over = True  # Jugador ha perdido todas sus vidas

            # Verificar si el puntaje alcanza el siguiente nivel
            if score1 >= LEVELS[current_level]["score_threshold"]:
                current_level += 1
                if current_level <= len(LEVELS):
                    current_background = backgrounds[current_level]  # Cambiar el fondo
                    enemy_speed = LEVELS[current_level]["enemy_speed"]  # Cambiar la velocidad de los enemigos

        # Dibujar en pantalla el fondo y sprites
        screen.blit(current_background, (0, 0))
        all_sprites.draw(screen)
        show_scores(screen, score1)  # Mostrar el puntaje del jugador 1
        show_lives(screen, player1.lives)  # Mostrar las vidas restantes

        # Si el jugador ha perdido, mostrar el mensaje de "Has perdido"
        if game_over:
            button_rect = show_game_over(screen, score1)  # Mostrar mensaje y botón

        # Actualizar la pantalla
        pygame.display.flip()

        # Controlar la velocidad del juego
        clock.tick(FPS)

    cap.release()  # Liberar recursos de la cámara
    cv2.destroyAllWindows()  # Cerrar ventanas de OpenCV
    pygame.quit()

# Iniciar el juego
run_game()