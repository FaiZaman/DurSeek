import pygame

class Entity(pygame.sprite.Sprite):

    def __init__(self, x, y, image):

        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.gravity = 20