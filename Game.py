import pygame
import random as rand
import time
from Screen import Screen
from Player import Player
from Treasure import Treasure
from Projectile import Projectile
from Enemy import Enemy
from Platform import Platform
from Upgrades import Heart, JumpBoost

pygame.init()
score = 0
win_score = 10
fps = 60

# create game window and clock
screen_width = 1000
screen_height = 739
window = Screen(screen_width, screen_height)
window = window.create_screen()
clock = pygame.time.Clock()

# load in background and its properties
background = pygame.image.load("assets/background/background.jpg")
background_flipped = pygame.image.load("assets/background/background_flipped.jpg")
background_x1 = 0
background_x2 = background.get_width()
treasure_image = pygame.image.load("assets/misc/treasure.png")

# load in music and sound effects
pygame.mixer.music.load('assets/sound/theme.mp3')
treasure_sound = pygame.mixer.Sound('assets/sound/treasure.wav')
explosion_sound = pygame.mixer.Sound('assets/sound/explosion.wav')
fireball_sound = pygame.mixer.Sound('assets/sound/fireball.wav')
upgrade_sound = pygame.mixer.Sound('assets/sound/health.wav')
damage_sound = pygame.mixer.Sound('assets/sound/damage.wav')
death_sound = pygame.mixer.Sound('assets/sound/death.wav')

# draws all game objects to window
def redraw_window(window, player):

    # draw background and background game objects
    window.blit(background, (background_x1, 0))
    window.blit(background_flipped, (background_x2, 0))

    # render the score
    window.blit(treasure_image, (30, 60))
    text = small_font.render("x" + str(score), 1, (0, 0, 0))
    window.blit(text, (110, 80))

    # draw health bar
    pygame.draw.rect(window, (200, 0, 0), (30, 10, 500, 40))
    pygame.draw.rect(window, (0, 180, 0), (30, 10, player.health * 5, 40))
    pygame.draw.rect(window, (0, 0, 0), (30, 10, 500, 40), 2)

    # draw the storm
    pygame.draw.rect(window, (240, 0, 0), (0, 0, 10, screen_height))

    # update sprite images
    player.set_image()
    for enemy in enemies:
        enemy.set_image()
    for projectile in projectiles:
        projectile.set_image()

    # draw sprites and refresh display
    sprites.draw(window)
    pygame.display.update()


def draw_game_over(window, starting, won, score):

    pygame.mixer.music.stop()
    window.fill((0, 220, 0))
    play_easy = medium_font.render("Press the E key to play EASY MODE", 1, (128, 0, 128))
    play_medium = medium_font.render("Press the M key to play MEDIUM MODE", 1, (128, 0, 128))
    play_hard = medium_font.render("Press the H key to play HARD MODE", 1, (128, 0, 128))
    window.blit(play_easy, (200, 400))
    window.blit(play_medium, (170, 500))
    window.blit(play_hard, (200, 600))

    if starting:
        title = large_font.render('DURSEEK', 1, (128, 0, 128))
        window.blit(title, (375, 100))

        controls = small_font.render('Use the arrow keys or WASD to move and jump, and space to shoot', 1, (128, 0, 128))
        instructions = small_font.render('Collect all 10 treasures to win, and keep ahead of the red storm behind you!', 1, (128, 0, 128))
        window.blit(controls, (120, 200))
        window.blit(instructions, (60, 300))
        pygame.display.update()
    else:
        if won:
            text = medium_font.render('You Win!', 1, (128, 0, 128))
            window.blit(text, (420, 200))
        else:
            text = medium_font.render('You Lose!', 1, (128, 0, 128))
            score_text = medium_font.render('Score: ' + str(score), 1, (128, 0, 128))
            window.blit(text, (420, 200))
            window.blit(score_text, (430, 300))
        
        pygame.display.update()
        time.sleep(2.5)
            
    waiting = True
    while waiting:
        clock.tick(fps)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            difficulty = "easy"
            waiting = False
        elif keys[pygame.K_m]:
            difficulty = "medium"
            waiting = False
        elif keys[pygame.K_h]:
            difficulty = "hard"
            waiting = False
    return difficulty


def draw_ground(difficulty):

    platform_y = [490, 520, 550]
    prev_generated = False

    if difficulty == "easy":
        spawn_rate = 0.2
    elif difficulty == "medium":
        spawn_rate = 0.3
    elif difficulty == "hard":
        spawn_rate = 0.5

    for i in range(0, 65000, 128):
        if (rand.random() > spawn_rate or i <= 512):
            ground = Platform(i, screen_height - 128)
            platforms.add(ground)
            game_objects.add(ground)
            sprites.add(ground)
            prev_generated = True
        else:
            if not(prev_generated):
                draw_platform(rand.choice([i, i - 128]), rand.randrange(1, 2), rand.choice(platform_y))
            prev_generated = False
    return spawn_rate


def draw_platform(x, width, y_position):
    
    for w in range(0, width):
        platform = Platform(x + 128*w, y_position)
        platform.image = platform.platform
        platforms.add(platform)
        game_objects.add(platform)
        sprites.add(platform)


def create_heart():

    heart = Heart(rand.randrange(1500, 2500), rand.randrange(0, 300))
    hearts.add(heart)
    gravitons.add(heart)
    game_objects.add(heart)
    sprites.add(heart)


def create_jump_boost():

    jump_boost = JumpBoost(rand.randrange(3000, 3500), rand.randrange(0, 300))
    jump_boosts.add(jump_boost)
    gravitons.add(jump_boost)
    game_objects.add(jump_boost)
    sprites.add(jump_boost)


def treasure_collected(score, background_speed, player, difficulty):

    treasure_sound.play()
    score += 1
    background_speed += 1
    player.speed += 1
    player.jump_limit -= 2

    if difficulty == "easy":
        if score == 8:
            pygame.time.set_timer(pygame.USEREVENT+2, 1200)
            create_heart()
            if player.gravity > 18:
                create_jump_boost()
        elif score == 6:
            background_speed -= 1
            player.speed -= 1
            pygame.time.set_timer(pygame.USEREVENT+2, 1400)
            create_heart()
            if player.gravity > 18:
                create_jump_boost()
        elif score == 4:
            background_speed -= 1
            player.speed -= 1
            create_heart()
            pygame.time.set_timer(pygame.USEREVENT+2, 1600)
            if player.gravity > 18:
                create_jump_boost()
        elif score == 2:
            background_speed -= 1
            player.speed -= 1
            pygame.time.set_timer(pygame.USEREVENT+2, 1800)
            create_heart()

    elif difficulty == "medium":
        if score == 8:
            pygame.time.set_timer(pygame.USEREVENT+2, 700)
            if player.gravity > 18:
                create_jump_boost()
            create_heart()
        elif score == 6:
            background_speed -= 1
            player.speed -= 1
            pygame.time.set_timer(pygame.USEREVENT+2, 1000)
            create_heart()
            if player.gravity > 18:
                create_jump_boost()
        elif score == 4:
            pygame.time.set_timer(pygame.USEREVENT+2, 1300)
        elif score == 2:
            pygame.time.set_timer(pygame.USEREVENT+2, 1600)
            create_heart()
    
    elif difficulty == "hard":
        if score == 8:
            pygame.time.set_timer(pygame.USEREVENT+2, 400)
            create_heart()
        elif score == 6:
            pygame.time.set_timer(pygame.USEREVENT+2, 800)
            if player.gravity > 18:
                create_jump_boost()
        elif score == 4:
            create_heart()
            pygame.time.set_timer(pygame.USEREVENT+2, 1200)
        elif score == 2:
            pygame.time.set_timer(pygame.USEREVENT+2, 1500)

    return score, background_speed


# create game object list, object spawn timer, and font
small_font = pygame.font.SysFont('comicsans', 30, True)
medium_font = pygame.font.SysFont('comicsans', 45, True)
large_font = pygame.font.SysFont('comicsans', 75, True)
pygame.time.set_timer(pygame.USEREVENT+1, 6000)    # treasure
pygame.time.set_timer(pygame.USEREVENT+2, 2000)     # enemies
pygame.time.set_timer(pygame.USEREVENT+3, 5000)     # platforms
game_over = True
first_game = True
starting = True
won = False
high_platform_y = [300, 330, 370, 400, 430, 460, 490]
jump_loop = 0

# main event loop
running = True
while running:

    if game_over:
        difficulty = draw_game_over(window, starting, won, score)
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
        jump_boosts = pygame.sprite.Group()
        spawn_rate = draw_ground(difficulty)

        player = Player()
        sprites.add(player)

        player.health = 100
        score = 0
        background_speed = 4
        if difficulty == "hard":
            background_speed += 1
            player.speed += 1

        pygame.mixer.music.play(-1)

    # clock speed and event detection
    clock.tick(fps)

    if difficulty == "easy":
        if player.health < 100 and rand.random() > 0.9995:
            create_heart()
    elif difficulty == "medium":
        if player.health <= 70 and rand.random() > 0.9997:
            create_heart()
    elif difficulty == "hard":
        if player.health <= 40 and rand.random() > 0.9999:
            create_heart()

    if player.jump_loop > 0:
        player.jump_loop += 1
    if player.jump_loop > player.jump_limit:
        player.jump_loop = 0

     # background scrolling with player
    background_x1 -= 1
    if background_x1 < background.get_width() * -1:
        background_x1 = background.get_width()

    background_x2 -= 1
    if background_x2 < background.get_width() * -1:
        background_x2 = background.get_width()

    # move game objects left
    for sprite in sprites:
        sprite.rect.x -= background_speed
        if sprite.rect.x <= sprite.rect.width * -1:
            if isinstance(sprite, Player):
                player.health = 0
            else:
                sprite.kill()

    # projectile movement
    for projectile in projectiles:
        projectile.move()
        if projectile.rect.x <= projectile.rect.width * -1:
            projectile.kill()
        elif projectile.rect.left >= screen_width:
            projectile.kill()

        projectile_enemy_collisions = pygame.sprite.spritecollide(projectile, enemies, False)
        if projectile_enemy_collisions:
            if not(enemy.exploding):
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
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            spawn_probability = rand.random()
            if event.type == pygame.USEREVENT+1:
                if spawn_probability > spawn_rate:
                    treasure = Treasure(rand.randrange(1500, 2000), rand.randrange(0, 200))
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
                draw_platform(1500, rand.randrange(5, 10), rand.choice(high_platform_y))

    # collision detection
    player_enemy_collisions = pygame.sprite.spritecollide(player, enemies, False)
    if player_enemy_collisions:
        for enemy in player_enemy_collisions:
            if not(enemy.exploding):
                player.lose_health()
                damage_sound.play()

    player_heart_collisions = pygame.sprite.spritecollide(player, hearts, True)
    if player_heart_collisions:
        upgrade_sound.play()
        player.health += 30
        if player.health > 100:
            player.health = 100

    player_boost_collisions = pygame.sprite.spritecollide(player, jump_boosts, True)
    if player_boost_collisions:
        upgrade_sound.play()
        player.gravity -= 2

    treasure_collisions = pygame.sprite.spritecollide(player, treasures, True)
    if treasure_collisions:
        score, background_speed = treasure_collected(score, background_speed, player, difficulty)
  
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
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        if player.rect.x > player.speed:
            player.move_left()

    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:

        if player.rect.x < 400:
            player.rect.x += player.speed
        else:
            player.rect.x += background_speed
        player.move_right()
    
    else:
        player.standing = True
        player.steps = 0

    # shoot projectiles
    if keys[pygame.K_SPACE]:

        # create and orient projectile
        fireball = Projectile(player.rect.left - 70, player.rect.centery - 30)
        fireball_sound.play()
        if len(projectiles) == 0:
            if player.facing_right:
                fireball.shot_right = True
            else:
                fireball.shot_right = False

            projectiles.add(fireball)
            game_objects.add(fireball)
            sprites.add(fireball)

    player.jump(keys[pygame.K_UP], keys[pygame.K_w])

    # end game if player fell off screen
    if player.is_jumping:
        player.apply_gravity()
    else:
        player.apply_falling_gravity()

    if player.rect.y > screen_height:
        game_over = True
        won = False
        first_game = False
        death_sound.play()

    player_platform_collisions = pygame.sprite.spritecollide(player, platforms, False)
    if player_platform_collisions:
        player.player_platform_collision_handling(player_platform_collisions)

    for graviton in gravitons:
        graviton.apply_gravity()
        graviton_platform_collisions = pygame.sprite.spritecollide(graviton, platforms, False)
        graviton.platform_collision_handling(graviton_platform_collisions)

    if not(game_over):
        redraw_window(window, player)

pygame.quit()
