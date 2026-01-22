import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Don't Crash Game")
clock = pygame.time.Clock()

GAME_RUNNING = "running"
GAME_OVER = "game_over"

SCORE_INTERVAL = 500

# Font
font = pygame.font.Font(None, 72)
font_score = pygame.font.SysFont(None, 36)

button_rect = pygame.Rect(300, 420, 200, 60)

# Road
road = pygame.Rect(200, 0, 400, 800)
lines = []
last_line_spawn = 0
base_line_interval = 1000
min_line_interval = 150

# Car
car = pygame.Rect(300, 450, 50, 100)

# Boxes
boxes = []
box_speed = 5
last_box_spawn = 0
spawn_interval_box = 1500
last_speed_increase = 0
speed_increase_interval = 5000

# Score
score = 0
last_score_time = 0

game_state = GAME_RUNNING

first_lines = []


def reset_game():
    global score, boxes, lines, box_speed, last_score_time, game_state, first_lines
    score = 0
    boxes.clear()
    lines.clear()
    first_lines.clear()   # ✅ ADD THIS
    box_speed = 5
    last_score_time = pygame.time.get_ticks()
    car.x, car.y = 300, 450
    game_state = GAME_RUNNING

    first_lines.extend([
        pygame.Rect(380, 650, 20, 100),
        pygame.Rect(380, 400, 20, 100),
        pygame.Rect(380, 150, 20, 100),
    ])

def draw_game_over():
    text = font.render("GAME OVER", True, (0, 0, 0))
    screen.blit(text, text.get_rect(center=(400, 400)))

    pygame.draw.rect(screen, ("green"), button_rect)
    btn_text = font_score.render("Play Again", True, (0, 0, 0))
    screen.blit(btn_text, btn_text.get_rect(center=button_rect.center))
reset_game()

running = True
while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == GAME_OVER and button_rect.collidepoint(event.pos):
                reset_game()

    # Controls
    if game_state == GAME_RUNNING:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            car.x -= 5
        if keys[pygame.K_RIGHT]:
            car.x += 5
        if keys[pygame.K_UP]:
            car.y -= box_speed*0.5
        if keys[pygame.K_DOWN]:
            car.y += box_speed

        car.x = max(200, min(car.x, 600 - car.width))
        car.y = max(0, min(car.y, 800 - car.height))

    # Background
    screen.fill((0, 100, 0))
    pygame.draw.rect(screen, "gray", road)

    # Lines
    spawn_interval_roadline = max(min_line_interval, base_line_interval - box_speed * 50)

    if game_state == GAME_RUNNING and current_time - last_line_spawn > spawn_interval_roadline:
        lines.append(pygame.Rect(380, -100, 20, 100))
        last_line_spawn = current_time

    for line in lines:
        if game_state == GAME_RUNNING:
            line.y += box_speed
        pygame.draw.rect(screen, "white", line)

    # Spawn boxes
    if game_state == GAME_RUNNING and current_time - last_box_spawn > spawn_interval_box:
        boxes.append(pygame.Rect(random.randint(200, 500), -50, 100, 50))
        last_box_spawn = current_time

    # Increase speed
    if game_state == GAME_RUNNING and current_time - last_speed_increase >= speed_increase_interval:
        box_speed += 2
        last_speed_increase = current_time

    # Move boxes
    for box in boxes:
        if game_state == GAME_RUNNING:
            box.y += box_speed
        pygame.draw.rect(screen, (194, 155, 103), box)

    # Collision
    if game_state == GAME_RUNNING:
        for box in boxes:
            if car.colliderect(box):
                game_state = GAME_OVER
                break
    
    # First lines
    for line in first_lines:
        if game_state == GAME_RUNNING:
            line.y += box_speed
        pygame.draw.rect(screen, (255, 255, 255), line)

    pygame.draw.rect(screen, (255, 0, 0), car)
    
    # Score
    if game_state == GAME_RUNNING and current_time - last_score_time >= SCORE_INTERVAL:
        score += 1
        last_score_time = current_time

    score_text = font_score.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Game Over
    if game_state == GAME_OVER:
        draw_game_over()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
