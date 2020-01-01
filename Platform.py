import pygame
from Entity import Entity

class Platform(Entity):

    platform = pygame.image.load("assets/platforms/2NE.png")

    def __init__(self, x, y):

        super().__init__(x, y, self.platform)
        self.image = self.platform
