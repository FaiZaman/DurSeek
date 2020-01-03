import pygame
from Entity import Entity

class Projectile(Entity):

    right_list = [pygame.image.load("assets/projectiles/R1.png"), pygame.image.load("assets/projectiles/R2.png"),\
                  pygame.image.load("assets/projectiles/R3.png"), pygame.image.load("assets/projectiles/R4.png"),\
                  pygame.image.load("assets/projectiles/R5.png"), pygame.image.load("assets/projectiles/R6.png"),\
                  pygame.image.load("assets/projectiles/R7.png"), pygame.image.load("assets/projectiles/R8.png"),\
                  pygame.image.load("assets/projectiles/R9.png"), pygame.image.load("assets/projectiles/R10.png"),\
                  pygame.image.load("assets/projectiles/R11.png"), pygame.image.load("assets/projectiles/R12.png"),\
                  pygame.image.load("assets/projectiles/R13.png"), pygame.image.load("assets/projectiles/R14.png"),\
                  pygame.image.load("assets/projectiles/R15.png"), pygame.image.load("assets/projectiles/R16.png"),\
                  pygame.image.load("assets/projectiles/R17.png"), pygame.image.load("assets/projectiles/R18.png"),\
                  pygame.image.load("assets/projectiles/R19.png"), pygame.image.load("assets/projectiles/R20.png"),\
                  pygame.image.load("assets/projectiles/R21.png"), pygame.image.load("assets/projectiles/R22.png"),\
                  pygame.image.load("assets/projectiles/R23.png"), pygame.image.load("assets/projectiles/R24.png"),\
                  pygame.image.load("assets/projectiles/R25.png"), pygame.image.load("assets/projectiles/R26.png"),\
                  pygame.image.load("assets/projectiles/R27.png"), pygame.image.load("assets/projectiles/R28.png"),\
                  pygame.image.load("assets/projectiles/R29.png"), pygame.image.load("assets/projectiles/R30.png"),\
                  pygame.image.load("assets/projectiles/R31.png"), pygame.image.load("assets/projectiles/R32.png"),\
                  pygame.image.load("assets/projectiles/R33.png"), pygame.image.load("assets/projectiles/R34.png"),\
                  pygame.image.load("assets/projectiles/R35.png"), pygame.image.load("assets/projectiles/R36.png"),\
                  pygame.image.load("assets/projectiles/R37.png"), pygame.image.load("assets/projectiles/R38.png"),\
                  pygame.image.load("assets/projectiles/R39.png"), pygame.image.load("assets/projectiles/R40.png"),\
                  pygame.image.load("assets/projectiles/R41.png"), pygame.image.load("assets/projectiles/R42.png"),\
                  pygame.image.load("assets/projectiles/R43.png"), pygame.image.load("assets/projectiles/R44.png"),\
                  pygame.image.load("assets/projectiles/R45.png"), pygame.image.load("assets/projectiles/R46.png"),\
                  pygame.image.load("assets/projectiles/R47.png"), pygame.image.load("assets/projectiles/R48.png"),\
                  pygame.image.load("assets/projectiles/R49.png"), pygame.image.load("assets/projectiles/R50.png")]

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
