import pygame
from Entity import Entity

class Projectile(Entity):

    bullet = pygame.image.load("assets/misc/ammo.png")

    def __init__(self):

        super().__init__(1050, 600, self.bullet)
        self.speed = 10

