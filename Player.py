import pygame

class Player(object):

    # load in character sprite images
    left_list = [pygame.image.load("assets/character/walk/L1.png"), pygame.image.load("assets/character/walk/L2.png"),\
                pygame.image.load("assets/character/walk/L3.png"), pygame.image.load("assets/character/walk/L4.png"),\
                pygame.image.load("assets/character/walk/L5.png"), pygame.image.load("assets/character/walk/L6.png")]

    right_list = [pygame.image.load("assets/character/walk/R1.png"), pygame.image.load("assets/character/walk/R2.png"),\
                pygame.image.load("assets/character/walk/R3.png"), pygame.image.load("assets/character/walk/R4.png"),\
                pygame.image.load("assets/character/walk/R5.png"), pygame.image.load("assets/character/walk/R6.png")]

    left_standing_list = [pygame.image.load("assets/character/standing/standing_L1.png"), pygame.image.load("assets/character/standing/standing_L2.png")]
    right_standing_list = [pygame.image.load("assets/character/standing/standing_R1.png"), pygame.image.load("assets/character/standing/standing_R2.png")]

    def __init__(self, x, y, width, height):
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 10
        self.steps = 0
        self.standing = True
        self.stand_count = 0
        self.walk_right = False
        self.walk_left = False
        self.is_jumping = False
        self.jump_length = 8
        self.hitbox = (x, y, width, 105)


    def draw(self, window):
        
        if self.steps + 1 > 18:
            self.steps = 0

        if not(self.standing):
            self.stand_count = 0
            if self.walk_left:
                window.blit(self.left_list[self.steps//3], (self.x, self.y))
                self.steps += 1
            elif self.walk_right:
                window.blit(self.right_list[self.steps//3], (self.x, self.y))
                self.steps += 1
        else:
            if self.walk_left:
                window.blit(self.left_standing_list[self.stand_count % 2], (self.x, self.y))
            else:
                window.blit(self.right_standing_list[self.stand_count % 2], (self.x, self.y))
            self.stand_count += 1

        self.hitbox = (self.x, self.y, self.width, 105)
                