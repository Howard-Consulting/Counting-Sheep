# counting_sheep.py
import pygame
import random
import sys

# Initialize PyGame
pygame.init()

# Screen dimensions
screen_width = 400
screen_height = 600

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Sheep")

# Load images
sheep_image = pygame.image.load('assets/sheep.png')
sheep_image = pygame.transform.scale(sheep_image, (44, 34))
fence_image = pygame.image.load('assets/fence.png')
background_image = pygame.image.load('assets/background.png')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Clock
clock = pygame.time.Clock()

# Bird settings
bird_x = screen_width // 4
bird_y = screen_height // 2
bird_width = 44
bird_height = 34
bird_y_change = 0
gravity = 0.5
jump = -10

# Pipe settings
pipe_width = 80
pipe_gap = 200
pipe_x_change = -3
pipes = []

def create_pipe():
    height = random.randint(150, 450)
    top_pipe = pygame.Rect(screen_width, height - pipe_gap // 2 - 600, pipe_width, 600)
    bottom_pipe = pygame.Rect(screen_width, height + pipe_gap // 2, pipe_width, 600)
    return top_pipe, bottom_pipe

def draw_pipes(pipes):
    for pipe in pipes:
        pipe_rect = pygame.Rect(pipe.x, pipe.y, pipe_width, pipe.height)
        fence_stretched = pygame.transform.scale(fence_image, (pipe_width, pipe.height))
        screen.blit(fence_stretched, pipe_rect.topleft)

def check_collision(pipes, bird):
    for pipe in pipes:
        if bird.colliderect(pipe):
            return True
    if bird.top <= 0 or bird.bottom >= screen_height:
        return True
    return False

def draw_bird(bird):
    screen.blit(sheep_image, (bird.x, bird.y))

def game_over():
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, (0, 0, 0))
    screen.blit(text, (screen_width // 4, screen_height // 2))
    pygame.display.flip()
    pygame.time.wait(2000)

def reset_game():
    global bird, bird_y_change, pipes, score, high_score
    if score > high_score:
        high_score = score
    bird.y = screen_height // 2
    bird_y_change = 0
    pipes = []
    pipes.extend(create_pipe())
    score = 0

# Initialize high score
high_score = 0

# Main loop
running = True
score = 0
bird = pygame.Rect(bird_x, bird_y, bird_width, bird_height)
pipes.extend(create_pipe())
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_y_change = jump

    bird_y_change += gravity
    bird.y += bird_y_change

    if pipes[0].right < 0:
        pipes = pipes[2:]
        pipes.extend(create_pipe())
        score += 1

    for pipe in pipes:
        pipe.x += pipe_x_change

    screen.blit(background_image, (0, 0))
    draw_bird(bird)
    draw_pipes(pipes)

    if check_collision(pipes, bird):
        game_over()
        reset_game()

    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

    high_score_text = font.render(f"High Score: {high_score}", True, (0, 0, 0))
    screen.blit(high_score_text, (10, 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()