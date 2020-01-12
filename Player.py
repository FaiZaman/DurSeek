import pygame
from Entity import Entity

class Player(Entity):

    # load in character sprite images
    left_list = [pygame.image.load("assets/character/walk/L1.png"), pygame.image.load("assets/character/walk/L2.png"),\
                pygame.image.load("assets/character/walk/L3.png"), pygame.image.load("assets/character/walk/L4.png"),\
                pygame.image.load("assets/character/walk/L5.png"), pygame.image.load("assets/character/walk/L6.png")]

    right_list = [pygame.image.load("assets/character/walk/R1.png"), pygame.image.load("assets/character/walk/R2.png"),\
                pygame.image.load("assets/character/walk/R3.png"), pygame.image.load("assets/character/walk/R4.png"),\
                pygame.image.load("assets/character/walk/R5.png"), pygame.image.load("assets/character/walk/R6.png")]

    left_standing_list = [pygame.image.load("assets/character/standing/standing_L1.png"), pygame.image.load("assets/character/standing/standing_L2.png")]

    right_standing_list = [pygame.image.load("assets/character/standing/standing_R1.png"), pygame.image.load("assets/character/standing/standing_R2.png")]

    def __init__(self):

        super().__init__(100, 500, self.right_standing_list[0])
        self.speed = 10
        self.steps = 0
        self.health = 100
        self.standing = True
        self.stand_count = 0
        self.walk_right = False
        self.walk_left = False
        self.is_jumping = False
        self.jump_length = 12
        self.falling = False
        self.on_ground = True
        self.facing_right = True
        self.cooldown = 0
        self.tinted = False
        self.tint_scale = 0.5
        self.knockback = 50
    

    def set_image(self):

        if self.steps + 1 > 18:
            self.steps = 0

        if not(self.standing):
            self.stand_count = 0
            if self.walk_left:
                self.image = self.left_list[self.steps//3]
            elif self.walk_right:
                self.image = self.right_list[self.steps//3]
            self.steps += 1
        else:
            if self.walk_left:
                self.image = self.left_standing_list[self.stand_count % 2]
            else:
                self.image = self.right_standing_list[self.stand_count % 2]
            self.stand_count += 1
        
        if self.tinted:
            self.tint()
            self.tinted = False


    def move_left(self):

        if self.rect.x >= 400:
            self.rect.x -= self.speed
        self.walk_left = True
        self.walk_right = False
        self.standing = False
        self.facing_right = False
    
    
    def move_right(self):

        if self.rect.x < 400:
            self.rect.x += self.speed
        self.walk_left = False
        self.walk_right = True
        self.standing = False
        self.facing_right = True


    def jump(self, jump_key):

        # quadratic jumping functionality
        if not(self.is_jumping):
            self.falling = False
            self.on_ground = True
            if jump_key:
                self.is_jumping = True
                self.walk_left = False
                self.walk_right = False
                self.steps = 0
                self.on_ground = False
        else:
            if self.jump_length >= -12:
                multiplier = 1
                if self.jump_length < 0:
                    self.falling = True
                    multiplier = -1
                self.rect.bottom -= (self.jump_length ** 2) * 0.5 * multiplier
                self.jump_length -= 1
            else:
                self.is_jumping = False
                self.jump_length = 12
        

    def lose_health(self):

        if self.cooldown > 0:
            self.cooldown -= 1
        else:
            self.cooldown = 10
            self.health -= 10
            if self.facing_right:
                self.rect.x -= self.knockback
            else:
                self.rect.x += self.knockback
            self.tinted = True


    def tint(self):

        GB = min(255, max(0, round(255 * (1 - self.tint_scale))))
        self.image.fill((255, GB, GB), special_flags = pygame.BLEND_MULT)


    def player_platform_collision_handling(self, collisions):

        if collisions:
            highest_y = 0
            for platform in collisions:
                if platform.rect.top > highest_y:
                    highest_y = platform.rect.top
            if (self.rect.y < highest_y and self.falling) or (self.rect.y < highest_y and self.on_ground):
                self.rect.bottom = highest_y + 12
