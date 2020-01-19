import pygame
import random as rand
from Entity import Entity

black_list = []
explosion_list = []

for n in range(1, 44):
    black_list.append(pygame.image.load("assets/black_enemy/L" + str(n) + ".png"))

for m in range(1, 91):
    explosion_list.append(pygame.image.load("assets/explosions/E (" + str(m) + ").png"))

class Enemy(Entity):

    red_list = [pygame.image.load("assets/red_enemy/L1.png"), pygame.image.load("assets/red_enemy/L2.png"),\
                 pygame.image.load("assets/red_enemy/L3.png"), pygame.image.load("assets/red_enemy/L4.png"),\
                 pygame.image.load("assets/red_enemy/L5.png"), pygame.image.load("assets/red_enemy/L6.png"),\
                 pygame.image.load("assets/red_enemy/L7.png"), pygame.image.load("assets/red_enemy/L8.png"),\
                 pygame.image.load("assets/red_enemy/L9.png"), pygame.image.load("assets/red_enemy/L10.png")]
    
    black_list = black_list
    explosion_list = explosion_list

    def __init__(self, x, y):
        
        self.is_red = True
        if rand.random() >= 0.33:
            super().__init__(x, y, self.red_list[0])
            self.speed = 2
        else:
            super().__init__(x, y, self.black_list[0])
            self.is_red = False
            self.speed = 4
        self.steps = 0
        self.exploding = False
        self.explode_count = 0

    
    def set_image(self):
        
        if not(self.exploding):

            if self.is_red:
                if self.steps + 1 > 30:
                    self.steps = 0
                self.image = self.red_list[self.steps//3]
            else:
                if self.steps + 1 > 129:
                    self.steps = 0
                self.image = self.black_list[self.steps//3]
            
            self.steps += 1
            self.rect.x -= self.speed
        else:
            self.image = self.explosion_list[self.explode_count]
            self.explode_count += 1

            if self.explode_count == 90:
                self.kill()
