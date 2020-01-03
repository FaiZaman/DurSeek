import pygame
from Entity import Entity

class Enemy(Entity):

    left_list = [pygame.image.load("assets/enemy/L1.png"), pygame.image.load("assets/enemy/L2.png"),\
                 pygame.image.load("assets/enemy/L3.png"), pygame.image.load("assets/enemy/L4.png"),\
                 pygame.image.load("assets/enemy/L5.png"), pygame.image.load("assets/enemy/L6.png"),\
                 pygame.image.load("assets/enemy/L7.png"), pygame.image.load("assets/enemy/L8.png"),\
                 pygame.image.load("assets/enemy/L9.png"), pygame.image.load("assets/enemy/L10.png")]

    def __init__(self, x, y):
        
        super().__init__(x, y, self.left_list[0])
        self.speed = 4
        self.steps = 0

    
    def set_image(self):
        
        if self.steps + 1 > 30:
            self.steps = 0

        self.image = self.left_list[self.steps//3]
        self.steps += 1
        self.rect.x -= self.speed
        