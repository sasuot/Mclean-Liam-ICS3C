import pygame
import random

pygame.init()

# WINDOW
screen = pygame.display.set_mode((1440, 800))
pygame.display.set_caption("Space Shooter")

clock = pygame.time.Clock()

# COLOURS
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0,255,0)
# PLAYER
player_x = 700
player_y = 700
player_speed = 12

player2_x = 700
player2_y = 800


# BULLETS
bullet_x = [0, 0, 0, 0, 0]
bullet_y = [0, 0, 0, 0, 0]
bullet_active = [False, False, False, False, False]
bullet_speed = 13

# ENEMIES
enemy_x = [250, 375, 500, 625, 750, 875, 1000, 1125]
enemy_y = [80, 80, 80, 80, 80, 80, 80, 80]

enemy_speed = 1
enemy_direction = 1

end_screen = 0

# STARS
stars = []

for i in range(50):
    stars = stars + [[random.randint(0, 1440),
                      random.randint(0, 800)]]

running = True
game_over = False

shoot_timer = 0

while running:

    clock.tick(60)

    # EVENTS
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    if not game_over:

        keys = pygame.key.get_pressed()

        # PLAYER MOVEMENT
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
            player2_x -= player_speed
            
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
            player2_x += player_speed

        if player_x < 0:
            player_x = 0

        if player_x > 1390:
            player_x = 1390

        if player2_x < 0:
            player2_x = 0
            
        if player2_x > 1390:
            player2_x = 1390

        player_rect = pygame.Rect(player_x, player_y, 50, 50)

        player2_rect = pygame.Rect(player2_x, player2_y, 30, 30)

        
        # MOVE ENEMIES
        hit_edge = False

        for i in range(8):

            if enemy_y[i] != 1000:

                enemy_x[i] += enemy_speed * enemy_direction
                enemy_y[i] += 1.5

                if enemy_x[i] <= 0 or enemy_x[i] >= 1405:
                    hit_edge = True

        if hit_edge:
            enemy_direction = enemy_direction * -1

        # SHOOT BULLETS
        shoot_timer += 1

        if keys[pygame.K_SPACE] and shoot_timer >= 12:

            for i in range(5):

                if bullet_active[i] == False:

                    bullet_x[i] = player_x + 21
                    bullet_y[i] = player_y
                    bullet_active[i] = True

                    shoot_timer = 0
                    break

        # MOVE BULLETS
        for i in range(5):

            if bullet_active[i]:

                bullet_y[i] -= bullet_speed

                if bullet_y[i] < 0:
                    bullet_active[i] = False

        # BULLET COLLISION
        for i in range(5):

            if bullet_active[i]:

                bullet_rect = pygame.Rect(
                    bullet_x[i], bullet_y[i], 8, 20
                )

                for j in range(8):

                    if enemy_y[j] != 1000:

                        enemy_rect = pygame.Rect(
                            enemy_x[j], enemy_y[j], 35, 35
                        )

                        if bullet_rect.colliderect(enemy_rect):

                            bullet_active[i] = False
                            enemy_y[j] = 1000
                            break

        # PLAYER COLLISION
        for i in range(6):

            if enemy_y[i] != 1000:

                enemy_rect = pygame.Rect(
                    enemy_x[i], enemy_y[i], 35, 35
                )

                if player_rect.colliderect(enemy_rect):
                    game_over = True

                if enemy_y[i] >= 760:
                    game_over = True

        # NEW WAVE
        enemies_left = 0


        for i in range(6):

            if enemy_y[i] != 1000:
                enemies_left += 1

        if enemies_left == 0:

            for i in range(6):

                enemy_x[i] = 250 + i * 125
                enemy_y[i] = 80

            for i in range(5):
                bullet_active[i] = False

            enemy_speed += 1
        if enemies_left == 0:
            end_screen += 1
        
        
    # BACKGROUND
    screen.fill(BLACK)

    # DRAW STARS
    for i in range(50):

        pygame.draw.rect(
            screen, WHITE,
            (stars[i][0], stars[i][1], 4, 4)
        )

    # DRAW PLAYER
    pygame.draw.rect(screen, BLUE,(player_x, player_y, 50, 50))

    if player_x == 800:
            player2_rect = pygame.draw.rect(screen, GREEN,(player_x, player_y, 25, 25))
                
    # DRAW ENEMIES
    for i in range(6):

        if enemy_y[i] != 1000:

            pygame.draw.rect(screen, RED,(enemy_x[i], enemy_y[i], 35, 35))

    # DRAW BULLETS
    for i in range(5):

        if bullet_active[i]:

            pygame.draw.rect(
                screen, BLUE,
                (bullet_x[i], bullet_y[i], 20, 20)
            )
    if end_screen>2:
        font = pygame.font.SysFont(None, 60)
        
        text = font.render("YOU WIN", True, GREEN)
        
        screen.blit(text, (620, 300))

        game_over = True

    # GAME OVER
    if game_over:

        font = pygame.font.SysFont(None, 60)

        text = font.render(
            "GAME OVER", True, RED
        )
        pygame.draw.rect(screen, WHITE,(player2_x, player2_y, 30, 30))
        screen.blit(text, (620, 380))

        

    pygame.display.flip()

pygame.quit()