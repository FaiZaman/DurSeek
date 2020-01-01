import pygame
import random as rand
from Screen import Screen
from Player import Player
from Treasure import Treasure
from Projectile import Projectile
from Enemy import Enemy
from Platform import Platform

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

# create player and sprite groups
sprites = pygame.sprite.Group()
game_objects = pygame.sprite.Group() # everything but player
treasures = pygame.sprite.Group()
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
platforms = pygame.sprite.Group()

player = Player()
sprites.add(player)

# draws all game objects to window
def redraw_window(window, player):

    # draw background and background game objects
    window.blit(background, (background_x1, 0))
    window.blit(background_flipped, (background_x2, 0))

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
    for projectile in projectiles:
        projectile.set_image()

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


def draw_ground(ground_coords, tx, ty):
    
    i = 0
    while i <= (screen_width/tx) + tx:
        ground_coords.append(i*tx)
        i += 1

    i = 0
    while i < len(ground_coords):
        ground = Platform(ground_coords[i], screen_height - ty)
        platforms.add(ground)
        game_objects.add(ground)
        sprites.add(ground)
        i += 1


def draw_platform(platform_coords, width, y_position, tx, ty):

    for i in range(0, width):
        platform_coords.append(rand.randrange(1000, 1500))
    
    for j in range(0, len(platform_coords)):
        platform = Platform(platform_coords[j], y_position)
        platform.image = platform.platform
        platforms.add(platform)
        game_objects.add(platform)
        sprites.add(platform)


# create ground throughout
ground_coords = []
tx = 128
ty = 128
draw_ground(ground_coords, tx, ty)

# create game object list, object spawn timer, and font
font = pygame.font.SysFont('comicsans', 30, True)
pygame.time.set_timer(pygame.USEREVENT+1, 3000)
pygame.time.set_timer(pygame.USEREVENT+2, 3500)
shootLoop = 0
game_over = False

# main event loop
running = True
while running:

    # clock speed and event detection
    clock.tick(36)

    if game_over:
        draw_game_over(window, won)
    
    # projectile cooldown
    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 10:
        shootLoop = 0

    # projectile movement
    for projectile in projectiles:
        projectile.move()
        if projectile.rect.x <= projectile.rect.width * -1:
            projectile.kill()
        elif projectile.rect.left >= screen_width:
            projectile.kill()

        projectile_enemy_collisions = pygame.sprite.spritecollide(projectile, enemies, True)
        if projectile_enemy_collisions:
            projectile.kill()

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
        if event.type == pygame.USEREVENT+2:
            width = rand.randrange(10)
            y_position = rand.randrange(300, 500)
            draw_platform([], width, y_position, tx, ty)

    # collision detection
    player_enemy_collisions = pygame.sprite.spritecollide(player, enemies, False)
    if player_enemy_collisions:
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

    # shoot projectiles
    if keys[pygame.K_SPACE] and shootLoop == 0:

        shootLoop = 1

        # create and orient projectile
        bullet = Projectile(player.rect.x, player.rect.centery)
        if len(projectiles) < 5:
            if player.facing_right:
                bullet.shot_right = True
            else:
                bullet.shot_right = False

            projectiles.add(bullet)
            game_objects.add(bullet)
            sprites.add(bullet)

    player.jump(keys[pygame.K_UP])

    # apply gravity to creatures and place them onto platforms
    player.apply_gravity()
    if player.rect.y > screen_height:
        game_over = True
        won = False

    player_platform_collisions = pygame.sprite.spritecollide(player, platforms, False)
    if player_platform_collisions:
        player.rect.bottom = player_platform_collisions[0].rect.top + 12
    
    for enemy in enemies:
        enemy.apply_gravity()
        enemy_platform_collisions = pygame.sprite.spritecollide(enemy, platforms, False)
        if enemy_platform_collisions:
            enemy.rect.bottom = enemy_platform_collisions[0].rect.top + 12

    if not(game_over):
        redraw_window(window, player)

pygame.quit()
