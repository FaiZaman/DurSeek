import pygame
from Entity import Entity

class Treasure(Entity):

    treasure = pygame.image.load("assets/misc/treasure.png")

    def __init__(self, x, y):
        super().__init__(x, y, self.treasure)
