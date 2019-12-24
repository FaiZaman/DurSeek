import pygame

class Player(object):

    def __init__(self, x, y, width, height):
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 10
        self.steps = 0
        self.standing = True
        self.walk_right = False
        self.walk_left = False
        self.is_jumping = False
        self.jump_length = 10


    def draw(self, window, left_list, right_list):
        
        if self.steps + 1 > 18:
            self.steps = 0

        if not(self.standing):
            if self.walk_left:
                window.blit(left_list[self.steps//3], (self.x, self.y))
                self.steps += 1
            elif self.walk_right:
                window.blit(right_list[self.steps//3], (self.x, self.y))
        else:
            if self.walk_left:
                window.blit(left_list[0], (self.x, self.y))
            else:
                window.blit(right_list[0], (self.x, self.y))

        