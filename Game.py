import pygame
import random as rand
from Screen import Screen
from Player import Player
from Treasure import Treasure
from Projectile import Projectile
from Enemy import Enemy
from Platform import Platform
from Upgrades import Heart

pygame.init()
score = 0
win_score = 10
fps = 40

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

# load in game object images
ground = pygame.image.load("assets/background/ground.png")
clock = pygame.time.Clock()

# load in music and sound effects
pygame.mixer.music.load('assets/sound/game_theme.mp3')
treasure_sound = pygame.mixer.Sound('assets/sound/treasure.wav')
explosion_sound = pygame.mixer.Sound('assets/sound/explosion.wav')
fireball_sound = pygame.mixer.Sound('assets/sound/fireball.wav')
health_sound = pygame.mixer.Sound('assets/sound/health.wav')
damage_sound = pygame.mixer.Sound('assets/sound/damage.wav')
death_sound = pygame.mixer.Sound('assets/sound/death.wav')

# draws all game objects to window
def redraw_window(window, player):

    # draw background and background game objects
    window.blit(background, (background_x1, 0))
    window.blit(background_flipped, (background_x2, 0))

    # render the score
    text = small_font.render('Score: ' + str(score), 1, (0, 0, 0))
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


def draw_game_over(window, starting, won):

    pygame.mixer.music.stop()
    window.fill((0, 220, 0))
    play = medium_font.render("Press any key to begin", 1, (128, 0, 128))
    again = medium_font.render("Press any key to play again", 1, (128, 0, 128))

    if starting:
        title = large_font.render('DURSEEK', 1, (128, 0, 128))
        window.blit(title, (375, 150))

        controls = small_font.render('Use the arrow keys to move and jump, and space to shoot', 1, (128, 0, 128))
        window.blit(controls, (200, 300))
        window.blit(play, (300, 400))
    else:
        if won:
            text = medium_font.render('You Win!', 1, (128, 0, 128))
            window.blit(text, (420, 200))
        else:
            text = medium_font.render('You Lose!', 1, (128, 0, 128))
            window.blit(text, (420, 200))
        window.blit(again, (300, 400))
        
    pygame.display.update()
    
    waiting = True
    while waiting:
        clock.tick(fps)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


def draw_ground(ground_coords, tx, ty):

    ground = Platform(0, 0)
    ground_coords, no_ground_list = ground.get_coords_list(ground_coords, tx, ty)

    for i in range(0, len(ground_coords)):
        ground = Platform(ground_coords[i], screen_height - ty)
        platforms.add(ground)
        game_objects.add(ground)
        sprites.add(ground)
    
    for j in range(0, len(no_ground_list)):
        draw_platform([no_ground_list[j]], rand.randrange(5), rand.randrange(500, 540), 128, 32)


def draw_platform(platform_coords, width, y_position, tx, ty):

    if platform_coords == []:
        for i in range(0, width):
            platform_coords.append(rand.randrange(1300, 1700))
    
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

# create game object list, object spawn timer, and font
small_font = pygame.font.SysFont('comicsans', 30, True)
medium_font = pygame.font.SysFont('comicsans', 45, True)
large_font = pygame.font.SysFont('comicsans', 75, True)
pygame.time.set_timer(pygame.USEREVENT+1, 10000)
pygame.time.set_timer(pygame.USEREVENT+2, 2000)
pygame.time.set_timer(pygame.USEREVENT+3, 3500)
shootLoop = 0
game_over = True
first_game = True
starting = True
won = False

# main event loop
running = True
while running:

    if game_over:
        draw_game_over(window, starting, won)
        game_over = False
        starting = False
        
        # create player and sprite groups
        sprites = pygame.sprite.Group()
        game_objects = pygame.sprite.Group() # everything but player
        gravitons = pygame.sprite.Group() # everything gravity is applied to except for player
        treasures = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        projectiles = pygame.sprite.Group()
        platforms = pygame.sprite.Group()
        hearts = pygame.sprite.Group()
        if not first_game:
            ground_coords = []
        draw_ground(ground_coords, tx, ty)

        player = Player()
        sprites.add(player)

        player.health = 100
        score = 0
        background_speed = 4

        pygame.mixer.music.play(-1)

    # clock speed and event detection
    clock.tick(fps)
    
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

        projectile_enemy_collisions = pygame.sprite.spritecollide(projectile, enemies, False)
        if projectile_enemy_collisions:
            projectile.kill()
            for enemy in projectile_enemy_collisions:
                explosion_sound.play()
                enemy.exploding = True
                enemy.rect.x -= 50
                enemy.rect.y -= 50

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if keys[pygame.K_RIGHT]:
            spawn_probability = rand.random()
            if event.type == pygame.USEREVENT+1:
                if spawn_probability > 0.5:
                    treasure = Treasure(1500, rand.randrange(0, 200))
                    treasures.add(treasure)
                    gravitons.add(treasure)
                    game_objects.add(treasure)
                    sprites.add(treasure)
            if event.type == pygame.USEREVENT+2:
                    enemy = Enemy(1500, rand.randrange(0, 200))
                    enemies.add(enemy)
                    gravitons.add(enemy)
                    game_objects.add(enemy)
                    sprites.add(enemy)
            if event.type == pygame.USEREVENT+3:
                width = rand.randrange(15)
                y_position = rand.randrange(300, 550)
                draw_platform([], width, y_position, 128, 32)

    # collision detection
    player_enemy_collisions = pygame.sprite.spritecollide(player, enemies, False)
    if player_enemy_collisions:
        for enemy in player_enemy_collisions:
            if not(enemy.exploding):
                player.lose_health()
                damage_sound.play()

    player_heart_collisions = pygame.sprite.spritecollide(player, hearts, True)
    if player_heart_collisions:
        health_sound.play()
        player.health += 50
        if player.health > 100:
            player.health = 100

    treasure_collisions = pygame.sprite.spritecollide(player, treasures, True)
    if treasure_collisions:
        treasure_sound.play()
        score += 1
        background_speed += 2
        if score >= 8:
            pygame.time.set_timer(pygame.USEREVENT+2, 400)
        elif score >= 6:
            pygame.time.set_timer(pygame.USEREVENT+2, 800)
        elif score >= 4:
            pygame.time.set_timer(pygame.USEREVENT+2, 1200)
        elif score >= 2:
            pygame.time.set_timer(pygame.USEREVENT+2, 1500)
            heart = Heart(1500, rand.randrange(0, 300))
            heart.rect.y -= 50
            hearts.add(heart)
            gravitons.add(heart)
            game_objects.add(heart)
            sprites.add(heart)
  
    # check score and health to see if game over
    if score >= win_score:
        game_over = True
        won = True
        first_game = False
    elif player.health == 0:
        game_over = True
        won = False
        first_game = False
        death_sound.play()
           
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
            if game_object.rect.x <= game_object.rect.width * -1 and isinstance(game_object, Projectile):
                game_object.kill()
    
    else:
        player.standing = True
        player.steps = 0

    # shoot projectiles
    if keys[pygame.K_SPACE] and shootLoop == 0:

        shootLoop = 1

        # create and orient projectile
        fireball = Projectile(player.rect.left - 70, player.rect.centery - 30)
        fireball_sound.play()
        if len(projectiles) < 3:
            if player.facing_right:
                fireball.shot_right = True
            else:
                fireball.shot_right = False

            projectiles.add(fireball)
            game_objects.add(fireball)
            sprites.add(fireball)

    player.jump(keys[pygame.K_UP])

    # endgame if player fell off screen
    player.apply_gravity()
    if player.rect.y > screen_height:
        game_over = True
        won = False
        first_game = False
        death_sound.play()

    player_platform_collisions = pygame.sprite.spritecollide(player, platforms, False)
    player.player_platform_collision_handling(player_platform_collisions)

    for graviton in gravitons:
        graviton.apply_gravity()
        graviton_platform_collisions = pygame.sprite.spritecollide(graviton, platforms, False)
        graviton.platform_collision_handling(graviton_platform_collisions)

    if not(game_over):
        redraw_window(window, player)

pygame.quit()
