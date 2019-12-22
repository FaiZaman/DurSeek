import pygame

pygame.init()

# create game window
screen_width = 1000
screen_height = 700
window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("DurSeek")

# main event loop
running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

pygame.quit()