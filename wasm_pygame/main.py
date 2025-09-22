import pygame
import random
import sys
import asyncio

# Config
WINDOW_SIZE = 400
CELL_SIZE = 20
FPS = 10

# Couleurs
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

async def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36) # Police par défaut, taille 36

    snake = [(100, 100)]
    snake_dir = (CELL_SIZE, 0)
    food = (random.randrange(0, WINDOW_SIZE, CELL_SIZE),
            random.randrange(0, WINDOW_SIZE, CELL_SIZE))
    
    score = 0
    running = True
    while running:
        clock.tick(FPS)
        await asyncio.sleep(0) # Nécessaire pour Pygbag
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_dir != (0, CELL_SIZE):
                    snake_dir = (0, -CELL_SIZE)
                if event.key == pygame.K_DOWN and snake_dir != (0, -CELL_SIZE):
                    snake_dir = (0, CELL_SIZE)
                if event.key == pygame.K_LEFT and snake_dir != (CELL_SIZE, 0):
                    snake_dir = (-CELL_SIZE, 0)
                if event.key == pygame.K_RIGHT and snake_dir != (-CELL_SIZE, 0):
                    snake_dir = (CELL_SIZE, 0)

        # Déplacement du serpent
        new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
        snake.insert(0, new_head)

        # Collision avec nourriture
        if snake[0] == food:
            score += 1
            food = (random.randrange(0, WINDOW_SIZE, CELL_SIZE),
                    random.randrange(0, WINDOW_SIZE, CELL_SIZE))
        else:
            snake.pop()
        
        # Collision avec murs ou soi-même
        if (snake[0][0] < 0 or snake[0][0] >= WINDOW_SIZE or
            snake[0][1] < 0 or snake[0][1] >= WINDOW_SIZE or
            snake[0] in snake[1:]):
            running = False

        # Affichage
        screen.fill(BLACK)
        for pos in snake:
            pygame.draw.rect(screen, GREEN, (pos[0], pos[1], CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))

        # Affichage du score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

    # Affiche le score final
    screen.fill(BLACK)
    msg = font.render(f"Game Over ! Final Score: {score}", True, WHITE)
    screen.blit(msg, (WINDOW_SIZE // 2 - msg.get_width() // 2,
                      WINDOW_SIZE // 2 - msg.get_height() // 2))
    pygame.display.flip()
    await asyncio.sleep(2) # Laisse le message affiché 2 secondes

    pygame.quit()
    sys.exit()

asyncio.run(main())