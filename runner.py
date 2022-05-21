from sys import exit
import pygame

def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surf = font.render(f'Score: {current_time}', False, 'Brown')
    score_rect = score_surf.get_rect(center = (400,100))
    box_color = '#c0e8ec'
    pygame.draw.rect(screen, box_color, score_rect)
    screen.blit(score_surf, score_rect)

pygame.init()
width = 800
height = 400
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("RUNNER")
clock = pygame.time.Clock()
font = pygame.font.Font('font/Pixeltype.ttf',50)
game_active = True
start_time = 0

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()
text_color = (64,64,64)
text_surf = font.render('Mygame for now', None, text_color)

# #score text
# score = 0
# score_surf = font.render('Score: ' + str(score), None, 'Brown')
# score_rect = score_surf.get_rect(center = (400,100))
# box_color = '#c0e8ec'

snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(bottomright = (800,300))

player_surf = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (100,300)) #replace position of player_surf
player_gravity = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            exit()

        if game_active :
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom == 300:
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                        player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.x = 800 
                start_time = int(pygame.time.get_ticks()/1000)

    if game_active:
        #phong canh
        screen.blit(sky_surf, (0,0))
        screen.blit(ground_surf,(0,300))
        screen.blit(text_surf, (300,50))

        #score
        display_score()

        #snail movements
        snail_rect.x -= 4
        if snail_rect.right <= 0:
            snail_rect.x = 800
        screen.blit(snail_surf,snail_rect)

        #player movements
        player_gravity += 0.8
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_surf,player_rect)

        #collision
        if player_rect.colliderect(snail_rect):
            game_active = False


    pygame.display.update()
    clock.tick(60)
