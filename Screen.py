import pygame

class Screen(object):

    def __init__(self, screen_width, screen_height):

        self.screen_width = screen_width
        self.screen_height = screen_height
    

    def create_screen(self):

        window = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("DurSeek")
        return window
