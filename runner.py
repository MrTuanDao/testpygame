from tkinter import CENTER
from turtle import width
from sys import exit
import pygame

pygame.init()
width = 800
height = 400
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("RUNNER")
clock = pygame.time.Clock()
font = pygame.font.Font('font/Pixeltype.ttf',50)

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()
text_color = (64,64,64)
text_surf = font.render('Mygame for now', None, text_color)

#score text
score = 0
score_surf = font.render('Score: ' + str(score), None, 'Brown')
score_rect = score_surf.get_rect(center = (400,100))
box_color = '#c0e8ec'

snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(bottomright = (800,300))

player_surf = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (100,300)) #replace position of player_surf

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            exit()
   
    #phong canh
    screen.blit(sky_surf, (0,0))
    screen.blit(ground_surf,(0,300))
    screen.blit(text_surf, (300,50))

    #score
    pygame.draw.rect(screen, box_color, score_rect)

    screen.blit(score_surf, score_rect)

    #snail movements
    snail_rect.x -= 4
    if snail_rect.right <= 0:
        snail_rect.x = 800
        score += 1
    screen.blit(snail_surf,snail_rect)
    #player movements
    screen.blit(player_surf,player_rect)

    #collsion
    # if player_rect.colliderect(snail_rect):
    #     print("vcl")

    #mouse
    mouse_pos = pygame.mouse.get_pos()
    mouse_down = pygame.MOUSEBUTTONDOWN

    # if player_rect.collidepoint(mouse_pos):
    #     print("chuot cham player")

    pygame.display.update()
    clock.tick(60)
