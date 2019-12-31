import pygame
from Entity import Entity

class Projectile(Entity):

    bullet = pygame.image.load("assets/misc/ammo.png")

    def __init__(self, x, y):

        super().__init__(x, y, self.bullet)
        self.speed = 10
        self.shot_right = False


    def set_image(self):

        if self.shot_right:
            self.image = self.bullet
        else:
            self.image = pygame.transform.flip(self.bullet, True, False)


    def move(self):

        if self.shot_right:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
