import pygame
from Screen import Screen
from Player import Player

pygame.init()

# create game window, background, and clock
screen_width = 1024
screen_height = 389
window = Screen(screen_width, screen_height)
window = window.create_screen()
background = pygame.image.load("assets/background/cathedral.jpg")

clock = pygame.time.Clock()

# load in character sprite images
left_list = [pygame.image.load("assets/character/walk/L1.png"), pygame.image.load("assets/character/walk/L2.png"),\
             pygame.image.load("assets/character/walk/L3.png"), pygame.image.load("assets/character/walk/L4.png"),\
             pygame.image.load("assets/character/walk/L5.png"), pygame.image.load("assets/character/walk/L6.png")]

right_list = [pygame.image.load("assets/character/walk/R1.png"), pygame.image.load("assets/character/walk/R2.png"),\
              pygame.image.load("assets/character/walk/R3.png"), pygame.image.load("assets/character/walk/R4.png"),\
              pygame.image.load("assets/character/walk/R5.png"), pygame.image.load("assets/character/walk/R6.png")]

character = pygame.image.load("assets/character/standing/standing_1.png")

# create player
player = Player(100, 250, 64, 64)

# main event loop
running = True
while running:

    clock.tick(18)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
        
    if keys[pygame.K_LEFT] and player.x > player.speed:
        player.x -= player.speed
        player.walk_left = True
        player.walk_right = False
        player.standing = False

    elif keys[pygame.K_RIGHT] and player.x + player.speed + player.width < screen_width:
        player.x += player.speed
        player.walk_left = False
        player.walk_right = True
        player.standing = False

    else:
        player.standing = True
        player.steps = 0

    if not(player.is_jumping):
        if keys[pygame.K_SPACE]:
            player.is_jumping = True
            player.walk_left = False
            player.walk_right = False
            player.steps = 0
    else:
        if player.jump_length >= -8:
            multiplier = 1
            if player.jump_length < 0:
                multiplier = -1
            player.y -= (player.jump_length ** 2) * 0.5 * multiplier
            player.jump_length -= 1
        else:
            player.is_jumping = False
            player.jump_length = 8


    window.blit(background, (0,0))
    player.draw(window, left_list, right_list)
    pygame.display.update()

pygame.quit()