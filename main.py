import pygame
import random
import time

pygame.init()
win = pygame.display.set_mode((1440, 900))
pygame.display.set_caption("Aim Trainer")
black = (0, 0, 0)
white = (255, 255, 255)

# Initialize variables
width = 20
height = 20
hit_counter = 0

# Initialize positions for three stationary targets at random locations
targets = [(random.randint(50, 1390), random.randint(50, 850)) for _ in range(3)]

# Initialize the timer
start_time = time.time()
timer_duration = 100  # 100 seconds
game_over = False
show_play_again_button = False  # Initially, do not show the "Play Again" button

def enemies():
    # Draw three stationary targets at their positions
    for pos in targets:
        pygame.draw.ellipse(win, (255, 0, 0), (pos[0], pos[1], width, height))

def draw_crosshair(x, y):
    pygame.draw.line(win, white, (x - 15, y), (x + 15, y), 2)
    pygame.draw.line(win, white, (x, y - 15), (x, y + 15), 2)

def display_final_score(score):
    font = pygame.font.Font(None, 72)
    text = font.render("Final Score: " + str(score), True, white)
    text_rect = text.get_rect(center=(720, 450))
    win.blit(text, text_rect)

def display_play_again_button():
    font = pygame.font.Font(None, 36)
    button_text = font.render("Play Again", True, black)
    button_rect = pygame.Rect(600, 500, 200, 50)
    pygame.draw.rect(win, white, button_rect)
    win.blit(button_text, (650, 515))
    return button_rect

pygame.mouse.set_visible(False)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    x, y = pygame.mouse.get_pos()
    pygame.time.delay(10)

    win.fill(black)
    enemies()
    draw_crosshair(x, y)

    for i, pos in enumerate(targets):
        if not game_over:  # Only check collisions when the game is not over
            target_rect = pygame.Rect(pos[0], pos[1], width, height)
            crosshair_rect = pygame.Rect(x - 15, y - 15, 30, 30)
            
            if crosshair_rect.colliderect(target_rect):
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # Increase the hit counter
                        hit_counter += 1
                        print("Your Score Is:", str(hit_counter))
                        # Remove the hit target and replace it with a new target at a random position
                        targets[i] = (random.randint(50, 1390), random.randint(50, 850))

    # Display the remaining time and score on the screen
    font = pygame.font.Font(None, 36)
    text_time = font.render("Time Remaining: {:.1f} seconds".format(max(timer_duration - (time.time() - start_time), 0)), True, white)
    text_score = font.render("Targets Hit: " + str(hit_counter), True, white)
    win.blit(text_time, (10, 10))
    win.blit(text_score, (10, 50))

    if not game_over and time.time() - start_time >= timer_duration:
        game_over = True
        show_play_again_button = True

    if game_over and show_play_again_button:
        display_final_score(hit_counter)
        play_again_button_rect = display_play_again_button()

    pygame.display.update()

    if show_play_again_button:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and play_again_button_rect.collidepoint(event.pos):
                # Reset the game and variables
                hit_counter = 0
                targets = [(random.randint(50, 1390), random.randint(50, 850)) for _ in range(3)]
                start_time = time.time()
                game_over = False
                show_play_again_button = False
