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

character = pygame.image.load("assets/character/standing/standing_000.png")

# create player
player = Player(100, 300, 64, 64)

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
    elif keys[pygame.K_RIGHT] and player.x + player.speed + player.width < screen_width:
        player.x += player.speed


    window.blit(background, (0,0))
    pygame.display.update()

pygame.quit()