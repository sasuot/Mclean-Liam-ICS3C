import pygame

pygame.init()

# Create the game window
screen = pygame.display.set_mode((1440, 800))
pygame.display.set_caption("Moving Square")

# Set up our colours
SKY_BLUE = (135, 206, 235)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
# Store the player's and enemenys starting position
player_x = 700
player_y = 700
enemy_x = 700
enemy_y = 400

bullet_x = player_y
bullet_y = player_x
bullet_speed = 5  # Increased speed so it doesn't move at a crawl
bullet_active = False

# Control how many pixels the square moves each frame
speed = 3
enemy_speed = 0.5

# Keep the game running
running = True

# Add a clock to regulate frame rate (prevents the game from running too fast)
clock = pygame.time.Clock()

while running:

    # Check for events, including closing the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check which keyboard keys are being pressed
    keys = pygame.key.get_pressed()

    # Move left by decreasing the X position
    if keys[pygame.K_LEFT]:
        player_x = player_x - speed

    # Move right by increasing the X position
    if keys[pygame.K_RIGHT]:
        player_x = player_x + speed

    # Move the enemy toward the player
    if enemy_x < player_x:
        enemy_x += enemy_speed
    elif enemy_x > player_x:
        enemy_x -= enemy_speed
    if enemy_y < player_y:
        enemy_y += enemy_speed
    elif enemy_y > player_y:
        enemy_y -= enemy_speed

    # 1. HANDLE INPUT (Only handles the initial trigger)
    if keys[pygame.K_SPACE]:         
        if not bullet_active:
            # Reset bullet position to the player's position when fired
            bullet_x = player_x  # Adjust as needed to center it
            bullet_y = player_y
            bullet_active = True

    # 2. UPDATE BULLET POSITION
    if bullet_active:
        bullet_y -= bullet_speed 

        # Check boundaries (If it goes off-screen, deactivate it)
        if bullet_x >= 1440 or bullet_y >= 800 or bullet_y <= 0 or bullet_x <= 0:                      
            bullet_active = False

    # ================= DRAWING SECTION =================
    # Paint the background first to clear the previous frame
    screen.fill(BLACK)

    # Now draw the bullet if it's active
    if bullet_active:
        pygame.draw.rect(screen, BLUE, (bullet_x, bullet_y, 15, 15)) # Made bullet smaller (15x15) so it looks like a bullet!

    # 1. Create rectangle objects for both the player and the enemy
    player_rect = pygame.Rect(player_x, player_y, 50, 50)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, 30, 30)
    bullet_rect = pygame.Rect(bullet_x,bullet_y,15,15)
    
    # 2. Check if the rectangles overlap (collision)
    if player_rect.colliderect(enemy_rect):
        running = False  # Ends the game loop
    if bullet_rect.colliderect(enemy_rect):
        enemy_x = 0
        enemy_y = 0
    # Draw the player and enemy on top of the background
    pygame.draw.rect(screen, BLUE, (player_x, player_y, 50, 50))
    pygame.draw.rect(screen, RED, (enemy_x, enemy_y, 30, 30))
    
    # Show the updated screen
    pygame.display.flip()
    
    # Cap the game at 60 frames per second
    clock.tick(60)

pygame.quit()