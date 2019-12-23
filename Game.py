import pygame
from Screen import Screen

pygame.init()

# create game window and background
screen_width = 1024
screen_height = 389
window = Screen(screen_width, screen_height)
window = window.create_screen()
background = pygame.image.load("assets/cathedral.jpg")


# main event loop
running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    window.blit(background, (0,0))
    pygame.display.update()

pygame.quit()