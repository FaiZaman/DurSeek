import pygame

class Enemy(object):

    left_list = [pygame.image.load("assets/enemy/L1.png"), pygame.image.load("assets/enemy/L2.png"),\
                 pygame.image.load("assets/enemy/L3.png"), pygame.image.load("assets/enemy/L4.png"),\
                 pygame.image.load("assets/enemy/L5.png"), pygame.image.load("assets/enemy/L6.png"),\
                 pygame.image.load("assets/enemy/L7.png"), pygame.image.load("assets/enemy/L8.png"),\
                 pygame.image.load("assets/enemy/L9.png"), pygame.image.load("assets/enemy/L10.png")]

    def __init__(self, x, y, width, height):
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 8
        self.steps = 0
        self.hitbox = (x, y, width, height)

    
    def draw(self, window):
        
        if self.steps + 1 > 30:
            self.steps = 0

        window.blit(self.left_list[self.steps//3], (self.x, self.y))
        self.steps += 1
        self.x -= self.speed

        self.hitbox = (self.x, self.y, self.width, self.height)

    
    def hit(self, game_object, game_objects):
        print("oof")