import pygame
import random as rand
from Screen import Screen
from Player import Player
from Treasure import Treasure
from Enemy import Enemy

pygame.init()
score = 0
win_score = 5

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
clock = pygame.time.Clock()

# create player
player = Player(100, 550, 64, 106)

# draws all game_objects to window
def redraw_window(window, player):

    # draw background and background game_objects
    window.blit(background, (background_x1, 0))
    window.blit(background_flipped, (background_x2, 0))
    window.blit(ground, (0, 639))

    # render the score
    text = font.render('Score: ' + str(score), 1, (0, 0, 0))
    window.blit(text, (10, 60))

    # draw health bar
    pygame.draw.rect(window, (200, 0, 0), (10, 10, 500, 40))
    pygame.draw.rect(window, (0, 180, 0), (10, 10, player.health * 5, 40))
    pygame.draw.rect(window, (0, 0, 0), (10, 10, 500, 40), 2)

    # draw game objects and update
    player.draw(window)
    for game_object in game_objects:
        game_object.draw(window)
    pygame.display.update()


def draw_game_over(window, won):

    if won:
        text = font.render('You Win!', 1, (0, 0, 0))
    else:
        text = font.render('You Lose!', 1, (0, 0, 0))
    
    window.fill((255, 255, 255))
    window.blit(text, (450, 300))
    pygame.display.update()


# create game object list, object spawn timer, and font
game_objects = []
font = pygame.font.SysFont('comicsans', 30, True)
pygame.time.set_timer(pygame.USEREVENT+1, 3000)
game_over = False

# main event loop
running = True
while running:

    # clock speed and event detection
    clock.tick(36)

    if game_over:
        draw_game_over(window, won)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT+1:
            spawn_probability = rand.random()
            if spawn_probability > 0.7:
                game_objects.append(Treasure(1050, 590, 80, 72))
            elif spawn_probability > 0.3:
                game_objects.append(Enemy(1050, 600, 50, 50))

    # collision detection
    for game_object in game_objects:
        if player.y - player.height < game_object.hitbox[1] + game_object.hitbox[3] and player.y + player.height > game_object.hitbox[1]:
            if player.x - player.width < game_object.hitbox[0] + game_object.hitbox[2] and player.x + player.width > game_object.hitbox[0]:                
                game_object.hit(player, game_object, game_objects)
                if isinstance(game_object, Treasure):
                    score += 1

    # check score and health to see if game over
    if score >= win_score:
        game_over = True
        won = True
    elif player.health == 0:
        game_over = True
        won = False
   
    keys = pygame.key.get_pressed()
        
    # player movement
    if keys[pygame.K_LEFT] and player.x > player.speed:
        player.x -= player.speed
        player.walk_left = True
        player.walk_right = False
        player.standing = False

        # background scrolling with player
        background_x1 += background_speed
        if background_x1 > background.get_width():
            background_x1 = background.get_width() * -1

        background_x2 += background_speed
        if background_x2 > background.get_width():
            background_x2 = background.get_width() * -1

        # move game objects right
        for game_object in game_objects:
            game_object.x += background_speed

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

        # move game objects left
        for game_object in game_objects:
            game_object.x -= background_speed
            if game_object.x <= game_object.width * -1:
                game_objects.pop(game_objects.index(game_object))

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

    if not(game_over):
        redraw_window(window, player)

pygame.quit()
