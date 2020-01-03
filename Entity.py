import pygame

class Entity(pygame.sprite.Sprite):

    def __init__(self, x, y, image):

        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.gravity = 20


    def apply_gravity(self):

        self.rect.y += self.gravity
        

    def platform_collision_handling(self, entity, collisions):

        if collisions:
            highest_y = 0
            for platform in collisions:
                if platform.rect.top > highest_y:
                    highest_y = platform.rect.top
            if entity.rect.y < highest_y:
                entity.rect.bottom = highest_y + 12 
