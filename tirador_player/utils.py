# utils.py
import pygame
from .settings import WHITE, WIDTH

# Mostrar el puntaje del jugador
def show_scores(screen, score1):
    font = pygame.font.Font(None, 36)
    text1 = font.render(f"Puntaje Jugador: {score1}", True, WHITE)
    
    # Mostrar el puntaje en la parte superior
    screen.blit(text1, (10, 10))  # A la izquierda

# Mostrar las vidas del jugador
def show_lives(screen, lives):
    font = pygame.font.Font(None, 36)
    lives_text = font.render(f"Vidas Jugador: {lives}", True, WHITE)
    
    # Mostrar las vidas en la parte superior
    screen.blit(lives_text, (10, 50))  # A la izquierda

# Mostrar mensaje de "Has perdido" y el botón "Jugar de nuevo"
def show_game_over(screen, score):
    font = pygame.font.Font(None, 74)
    game_over_text = font.render("¡Has perdido!", True, WHITE)
    score_text = font.render(f"Puntaje: {score}", True, WHITE)

    # Posicionar el texto en el centro de la pantalla
    screen.blit(game_over_text, (screen.get_width() // 2 - game_over_text.get_width() // 2, screen.get_height() // 2 - 100))
    screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, screen.get_height() // 2 - 50))

    # Crear el botón "Jugar de nuevo"
    button_font = pygame.font.Font(None, 50)
    button_text = button_font.render("Jugar de nuevo", True, WHITE)
    button_rect = button_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))
    
    # Dibujar el botón en la pantalla
    pygame.draw.rect(screen, (0, 0, 0), button_rect.inflate(20, 20))  # Fondo del botón
    screen.blit(button_text, button_rect)  # Texto del botón
    
    return button_rect  # Retorna la posición y tamaño del botón para detectar clics
