import pygame
from Entity import Entity

explosion_list = []
for n in range(1, 91):
    explosion_list.append(pygame.image.load("assets/explosions/E (" + str(n) + ").png"))

class Enemy(Entity):

    left_list = [pygame.image.load("assets/enemy/L1.png"), pygame.image.load("assets/enemy/L2.png"),\
                 pygame.image.load("assets/enemy/L3.png"), pygame.image.load("assets/enemy/L4.png"),\
                 pygame.image.load("assets/enemy/L5.png"), pygame.image.load("assets/enemy/L6.png"),\
                 pygame.image.load("assets/enemy/L7.png"), pygame.image.load("assets/enemy/L8.png"),\
                 pygame.image.load("assets/enemy/L9.png"), pygame.image.load("assets/enemy/L10.png")]
    explosion_list = explosion_list

    def __init__(self, x, y):
        
        super().__init__(x, y, self.left_list[0])
        self.speed = 3
        self.steps = 0
        self.exploding = False
        self.explode_count = 0

    
    def set_image(self):
        
        if not(self.exploding):
            if self.steps + 1 > 30:
                self.steps = 0

            self.image = self.left_list[self.steps//3]
            self.steps += 1
            self.rect.x -= self.speed
        else:
            self.image = self.explosion_list[self.explode_count]
            self.explode_count += 1

            if self.explode_count == 90:
                self.kill()
