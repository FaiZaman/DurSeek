import pygame

class Player(object):

    def __init__(self, x, y, width, height):
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 10
        self.steps = 0


    def draw(self, window):
        
        if self.steps > 9:
            self.steps = 0

        