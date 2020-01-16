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

        super().__init__(200, 500, self.right_standing_list[0])
        self.speed = 5
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
        self.knockback = 50
        self.y_speed = 0
    

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


    def move_left(self):

        self.rect.x -= self.speed/2
        self.walk_left = True
        self.walk_right = False
        self.standing = False
        self.facing_right = False
    
    
    def move_right(self):

        self.walk_left = False
        self.walk_right = True
        self.standing = False
        self.facing_right = True


    def jump(self, jump_key1, jump_key2):

        if not(self.is_jumping):
            self.on_ground = True
            if jump_key1 or jump_key2:
                self.is_jumping = True
                self.walk_left = False
                self.walk_right = False
                self.steps = 0
                self.on_ground = False
                self.y_speed = 30
        else:
            if self.on_ground:
                self.is_jumping = False
                self.y_speed = 0
            else:
                self.y_speed -= self.gravity * (1/60)
                self.rect.y -= self.y_speed
                if self.y_speed < 20:
                    self.falling = True


    def lose_health(self):

        self.health -= 10
        self.rect.x -= self.knockback


    def player_platform_collision_handling(self, collisions):

        highest_y = 0
        for platform in collisions:
            if platform.rect.top > highest_y:
                highest_y = platform.rect.top
        if (self.falling or self.on_ground) and self.rect.y < highest_y:
            self.rect.bottom = highest_y + 12
            self.on_ground = True
            self.falling = False
            self.is_jumping = False
        elif not(self.on_ground) and self.y_speed < 15:
            falling = True
