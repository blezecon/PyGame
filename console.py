import pygame
from sys import exit

pygame.init()

SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("GAME")
clock = pygame.time.Clock()


# Load images and scale them to fit the screen
sky_surface = pygame.image.load("images/sky.png")
sky_image = pygame.transform.scale(sky_surface, (1366, 768))
ground_surface = pygame.image.load("images/ground.png")
ground_image = pygame.transform.scale(ground_surface, (1366, 768))
cloud_surface = pygame.image.load("images/cloud.png")
cloud_image = pygame.transform.scale(cloud_surface, (1366, 768))
support_surface = pygame.image.load("images/support.png")
support_image = pygame.transform.scale(support_surface, (1366, 768))
hills_surface = pygame.image.load("images/hills.png")
hills_image = pygame.transform.scale(hills_surface, (1366, 768))
bush_surface = pygame.image.load("images/bush.png")
bush_image = pygame.transform.scale(bush_surface, (1366, 768))
tree_surface = pygame.image.load("images/tree1.png")
tree_image = pygame.transform.scale(tree_surface, (1366, 768))
tree2_surface = pygame.image.load("images/tree2.png")
tree2_image = pygame.transform.scale(tree2_surface, (1366, 768))



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    
    screen.blit(sky_image, (0, 0))
    screen.blit(cloud_image, (0, 0))
    screen.blit(hills_image, (0, 0))
    screen.blit(support_image, (0, 0))
    screen.blit(tree_image, (0, 0))
    screen.blit(tree2_image, (0, 0))
    screen.blit(bush_image, (0, 0))
    screen.blit(ground_image, (0, 0))
   
    
    pygame.display.update()  # Update the display
    clock.tick(60)  # Limit the frame rate to 60 FPS