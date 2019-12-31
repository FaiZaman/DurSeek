import pygame
from Entity import Entity

class Treasure(Entity):

    treasure = pygame.image.load("assets/misc/treasure.png")

    def __init__(self):
        super().__init__(1050, 590, self.treasure)


    def hit(self, player, treasure, game_objects):
        game_objects.pop(game_objects.index(treasure))
