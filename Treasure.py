import pygame

class Treasure(object):

    treasure = pygame.image.load("assets/treasure.png")

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (x, y, width, height)


    def draw(self, window):

        window.blit(self.treasure, (self.x, self.y))
        self.hitbox = (self.x, self.y, self.width, self.height)
        pass


    def hit(self, treasure, game_objects):
        game_objects.pop(game_objects.index(treasure))
