import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong vs IA - Velocidad Progresiva")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Configuración de paletas
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
PADDLE_SPEED = 7

# Configuración de pelota
BALL_SIZE = 15
INITIAL_BALL_SPEED = 5  # Velocidad inicial
MAX_BALL_SPEED = 15     # Velocidad máxima
SPEED_INCREASE = 0.5    # Incremento de velocidad por colisión

# Crear objetos del juego
player = pygame.Rect(50, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ai_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

# Variables del juego
player_score = 0
ai_score = 0
font = pygame.font.Font(None, 36)

# Dificultad de la IA
AI_DIFFICULTY = 0.8  # 0 (fácil) a 1 (difícil)

# Variables de velocidad
ball_speed_x = INITIAL_BALL_SPEED * random.choice([-1, 1])
ball_speed_y = INITIAL_BALL_SPEED * random.choice([-1, 1])
current_ball_speed = INITIAL_BALL_SPEED

# Función para reiniciar la pelota
def reset_ball():
    """Reinicia la pelota al centro con dirección aleatoria y velocidad inicial"""
    ball.center = (WIDTH//2, HEIGHT//2)
    global current_ball_speed, ball_speed_x, ball_speed_y
    current_ball_speed = INITIAL_BALL_SPEED
    ball_speed_x = INITIAL_BALL_SPEED * random.choice([-1, 1])
    ball_speed_y = INITIAL_BALL_SPEED * random.choice([-1, 1])
    return ball_speed_x, ball_speed_y

# Función para la IA
def ai_movement():
    """Controla el movimiento de la paleta de la IA"""
    # La IA sigue la pelota con cierta imperfección
    target_y = ball.centery - PADDLE_HEIGHT//2
    
    # Suavizar el movimiento de la IA
    if ai_paddle.centery < ball.centery and random.random() < AI_DIFFICULTY:
        ai_paddle.y += min(PADDLE_SPEED, ball.centery - ai_paddle.centery)
    elif ai_paddle.centery > ball.centery and random.random() < AI_DIFFICULTY:
        ai_paddle.y -= min(PADDLE_SPEED, ai_paddle.centery - ball.centery)
    
    # Mantener dentro de los límites
    ai_paddle.top = max(0, ai_paddle.top)
    ai_paddle.bottom = min(HEIGHT, ai_paddle.bottom)

# Bucle principal
clock = pygame.time.Clock()
running = True

while running:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Control del jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player.top > 0:
        player.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
        player.y += PADDLE_SPEED
    
    # Movimiento de la IA
    ai_movement()
    
    # Movimiento de la pelota (con velocidad actual)
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    
    # Rebotes en bordes
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1
    
    # Colisiones con paletas
    if ball.colliderect(player) or ball.colliderect(ai_paddle):
        # Aumentar velocidad (sin superar el máximo)
        if current_ball_speed < MAX_BALL_SPEED:
            current_ball_speed += SPEED_INCREASE
        
        # Calcular nueva velocidad manteniendo la dirección
        ratio = current_ball_speed / (abs(ball_speed_x) + abs(ball_speed_y))
        ball_speed_x *= ratio * -1  # Invertir dirección horizontal
        
        # Añadir efecto de ángulo según donde golpee la paleta
        if ball.colliderect(player):
            ball_speed_y += (ball.centery - player.centery) * 0.05
        else:
            ball_speed_y += (ball.centery - ai_paddle.centery) * 0.05
    
    # Puntuación
    if ball.left <= 0:  # Punto para IA
        ai_score += 1
        ball_speed_x, ball_speed_y = reset_ball()
    elif ball.right >= WIDTH:  # Punto para jugador
        player_score += 1
        ball_speed_x, ball_speed_y = reset_ball()
    
    # Dibujado
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player)
    pygame.draw.rect(screen, WHITE, ai_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
    
    # Mostrar marcador y velocidad
    score_text = font.render(f"{player_score} - {ai_score}", True, WHITE)
    speed_text = font.render(f"Velocidad: {current_ball_speed:.1f}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))
    screen.blit(speed_text, (WIDTH//2 - speed_text.get_width()//2, 60))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()