import pygame
from Entity import Entity

right_list = []
for n in range(1, 51):
    right_list.append(pygame.image.load("assets/projectiles/R" + str(n) + ".png"))

class Projectile(Entity):

    right_list = right_list

    def __init__(self, x, y):

        super().__init__(x, y, self.right_list[0])
        self.speed = 20
        self.shot_right = False
        self.count = 0


    def set_image(self):

        if self.shot_right:
            self.image = self.right_list[self.count]
        else:
            self.image = pygame.transform.flip(self.right_list[self.count], True, False)
        self.count += 1
        
        if self.count == 50:
            self.kill()


    def move(self):

        if self.shot_right:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
