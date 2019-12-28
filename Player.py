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
        self.stand_count = 0
        self.walk_right = False
        self.walk_left = False
        self.is_jumping = False
        self.jump_length = 8
        self.hitbox = (x, y, width, 105)


    def draw(self, window, left_list, right_list, left_standing_list, right_standing_list):
        
        if self.steps + 1 > 18:
            self.steps = 0

        if not(self.standing):
            self.stand_count = 0
            if self.walk_left:
                window.blit(left_list[self.steps//3], (self.x, self.y))
                self.steps += 1
            elif self.walk_right:
                window.blit(right_list[self.steps//3], (self.x, self.y))
                self.steps += 1
        else:
            if self.walk_left:
                window.blit(left_standing_list[self.stand_count % 2], (self.x, self.y))
            else:
                window.blit(right_standing_list[self.stand_count % 2], (self.x, self.y))
            self.stand_count += 1

        self.hitbox = (self.x, self.y, self.width, 105)
                