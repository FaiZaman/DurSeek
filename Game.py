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
background_speed = 5

# load in game object images
ground = pygame.image.load("assets/background/ground.png")
clock = pygame.time.Clock()

# create player and sprite groups
sprites = pygame.sprite.Group()
game_objects = pygame.sprite.Group() # everything but player
treasures = pygame.sprite.Group()
enemies = pygame.sprite.Group()

player = Player()
sprites.add(player)

# draws all game objects to window
def redraw_window(window, player):

    # draw background and background game objects
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

    # update sprite images
    player.set_image()
    for enemy in enemies:
        enemy.set_image()

    # draw sprites and refresh display
    sprites.draw(window)
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
                treasure = Treasure()
                treasures.add(treasure)
                game_objects.add(treasure)
                sprites.add(treasure)
            elif spawn_probability > 0.3:
                enemy = Enemy()
                enemies.add(enemy)
                game_objects.add(enemy)
                sprites.add(enemy)

    # collision detection
    enemy_collisions = pygame.sprite.spritecollide(player, enemies, False)
    if enemy_collisions:
        player.lose_health()

    treasure_collisions = pygame.sprite.spritecollide(player, treasures, True)
    if treasure_collisions:
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
    if keys[pygame.K_LEFT] and player.rect.x > player.speed:

        player.move_left()

        # background scrolling with player
        background_x1 += background_speed
        if background_x1 > background.get_width():
            background_x1 = background.get_width() * -1

        background_x2 += background_speed
        if background_x2 > background.get_width():
            background_x2 = background.get_width() * -1

        # move game objects right
        for game_object in game_objects:
            game_object.rect.x += background_speed

    elif keys[pygame.K_RIGHT]:

        player.move_right()

        # background scrolling with player
        background_x1 -= background_speed
        if background_x1 < background.get_width() * -1:
            background_x1 = background.get_width()

        background_x2 -= background_speed
        if background_x2 < background.get_width() * -1:
            background_x2 = background.get_width()

        # move game objects left
        for game_object in game_objects:
            game_object.rect.x -= background_speed
            if game_object.rect.x <= game_object.rect.width * -1:
                game_object.kill()

    else:
        player.standing = True
        player.steps = 0

    player.jump(keys[pygame.K_UP])

    if not(game_over):
        redraw_window(window, player)

pygame.quit()
