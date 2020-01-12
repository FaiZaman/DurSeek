import pygame
import random as rand
from Entity import Entity

class Platform(Entity):

    ground = pygame.image.load("assets/platforms/2NE.png")
    platform = pygame.image.load("assets/platforms/2NE_rsz.png")

    def __init__(self, x, y):

        super().__init__(x, y, self.ground)
        self.image = self.ground


    def get_coords_list(self, ground_coords, tx, ty):

        no_ground_list = []

        i = 0
        while i <= (20000/tx) + tx:
            ground_spawn = rand.random()
            if ground_spawn > 0.2 or i == 0:
                ground_coords.append(i*tx)
            else:
                no_ground_list.append(i*tx)
            i += 1
    
        return ground_coords, no_ground_list
