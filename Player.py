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
        self.jump_length = 8
        self.facing_right = True

    
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

        self.rect.x -= self.speed
        self.walk_left = True
        self.walk_right = False
        self.standing = False
        self.facing_right = False
    
    
    def move_right(self):

        if self.rect.x < 300:
            self.rect.x += self.speed
        self.walk_left = False
        self.walk_right = True
        self.standing = False
        self.facing_right = True


    def jump(self, jump_key):

        # quadratic jumping functionality
        if not(self.is_jumping):
            if jump_key:
                self.is_jumping = True
                self.walk_left = False
                self.walk_right = False
                self.steps = 0
        else:
            if self.jump_length >= -8:
                multiplier = 1
                if self.jump_length < 0:
                    multiplier = -1
                self.rect.bottom -= (self.jump_length ** 2) * 0.5 * multiplier
                self.jump_length -= 1
            else:
                self.is_jumping = False
                self.jump_length = 8
    

    def apply_gravity(self):

        self.rect.y += self.gravity
        

    def lose_health(self):

        self.health -= 10
