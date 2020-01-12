import pygame
from Entity import Entity

class Heart(Entity):

    heart = pygame.image.load("assets/misc/heart.png")
    heart = pygame.transform.scale(heart, (64, 64))

    def __init__(self, x, y):

        super().__init__(x, y, self.heart)
        self.image = self.heart

