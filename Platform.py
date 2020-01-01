import pygame
from Entity import Entity

class Platform(Entity):

    ground = pygame.image.load("assets/platforms/2NE.png")
    platform = pygame.image.load("assets/platforms/2NE_rsz.png")

    def __init__(self, x, y):

        super().__init__(x, y, self.ground)
        self.image = self.ground
