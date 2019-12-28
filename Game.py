import pygame
from Screen import Screen
from Player import Player
from Treasure import Treasure

pygame.init()

# create game window and clock
screen_width = 1000
screen_height = 739
window = Screen(screen_width, screen_height)
window = window.create_screen()

# load in background and its properties
background = pygame.image.load("assets/background/background.jpg")
background_flipped = pygame.image.load("assets/background/background_flipped.jpg")
background_x1 = 0
background_x2 = background.get_width()
background_speed = 10

# load in game object images
ground = pygame.image.load("assets/background/ground.png")
character = pygame.image.load("assets/character/standing/standing_1.png")

clock = pygame.time.Clock()

# load in character sprite images
left_list = [pygame.image.load("assets/character/walk/L1.png"), pygame.image.load("assets/character/walk/L2.png"),\
             pygame.image.load("assets/character/walk/L3.png"), pygame.image.load("assets/character/walk/L4.png"),\
             pygame.image.load("assets/character/walk/L5.png"), pygame.image.load("assets/character/walk/L6.png")]

right_list = [pygame.image.load("assets/character/walk/R1.png"), pygame.image.load("assets/character/walk/R2.png"),\
              pygame.image.load("assets/character/walk/R3.png"), pygame.image.load("assets/character/walk/R4.png"),\
              pygame.image.load("assets/character/walk/R5.png"), pygame.image.load("assets/character/walk/R6.png")]

# create player
player = Player(100, 550, 64, 64)
treasure = Treasure(850, 590, 80, 72)

# draws all objects to window
def draw_objects(window, player):

    # draw background and background objects
    window.blit(background, (background_x1, 0))
    window.blit(background_flipped, (background_x2, 0))
    window.blit(ground, (0, 639))

    # draw game objects and update
    player.draw(window, left_list, right_list)
    treasure.draw(window)
    pygame.display.update()


# main event loop
running = True
while running:

    clock.tick(18)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
        
    # player movement
    if keys[pygame.K_LEFT] and player.x > player.speed:
        player.x -= player.speed
        player.walk_left = True
        player.walk_right = False
        player.standing = False

        background_x1 += background_speed
        if background_x1 > background.get_width():
            background_x1 = background.get_width() * -1

        background_x2 += background_speed
        if background_x2 > background.get_width():
            background_x2 = background.get_width() * -1

    elif keys[pygame.K_RIGHT]:

        if player.x < 300:
            player.x += player.speed
        player.walk_left = False
        player.walk_right = True
        player.standing = False

        # background scrolling with player
        background_x1 -= background_speed
        if background_x1 < background.get_width() * -1:
            background_x1 = background.get_width()

        background_x2 -= background_speed
        if background_x2 < background.get_width() * -1:
            background_x2 = background.get_width()

    else:
        player.standing = True
        player.steps = 0

    # quadratic jumping functionality
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

    draw_objects(window, player)

pygame.quit()