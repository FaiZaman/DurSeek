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

        super().__init__(100, 550, self.right_standing_list[0])
        self.speed = 10
        self.steps = 0
        self.health = 100
        self.standing = True
        self.stand_count = 0
        self.walk_right = False
        self.walk_left = False
        self.is_jumping = False
        self.jump_length = 8

    
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

    
    def lose_health(self):

        self.health -= 10
        