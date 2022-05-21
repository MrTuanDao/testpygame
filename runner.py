from sys import exit
import pygame
from random import randint

def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surf = font.render(f'Score: {current_time}', False, 'Brown')
    score_rect = score_surf.get_rect(center = (400,100))
    box_color = '#c0e8ec'
    pygame.draw.rect(screen, box_color, score_rect)
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300: screen.blit(snail_surf, obstacle_rect)
            else: screen.blit(fly_surf, obstacle_rect)
    
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: return []

def collison(player, obstacles):
    if obstacles:
        for obtacle_rect in obstacles:
            if player.colliderect(obtacle_rect): return False
    return True

pygame.init()
width = 800
height = 400
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("RUNNER")
clock = pygame.time.Clock()
font = pygame.font.Font('font/Pixeltype.ttf',50)
game_active = False
start_time = 0
score = 0

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()
text_color = (64,64,64)
text_surf = font.render('Mygame for now', None, text_color)

#obstacles
snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
fly_surf = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()

obstacle_rect_list = []

player_surf = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (100,300)) #replace position of player_surf
player_gravity = 0

#intro screen
def game_over_screen():
    #player stand
    player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
    player_stand = pygame.transform.scale2x(player_stand)
    player_stand_rec = player_stand.get_rect(center = (400, 200))
    screen.fill((94,129,162))
    screen.blit(player_stand, player_stand_rec)
    obstacle_rect_list.clear()
    player_rect.midbottom = (100,300)
    player_gravity = 0

    #text: Title
    game_name = font.render('Pixle Runner', None, (111,196,169))
    game_name_rect = game_name.get_rect(midtop = (400, 60))
    screen.blit(game_name, game_name_rect)
    if score == 0:
        #text: Play play
        game_over_text = font.render('Press to space to run!', None, 'White')
        game_over_rect = game_over_text.get_rect(midbottom = (400, 350))
        screen.blit(game_over_text,game_over_rect)
    else:
        #score_message
        score_message = font.render(f'Your score: {score}', False, (111,196,169))
        score_message_rect = score_message.get_rect(center = (400, 330))
        screen.blit(score_message,score_message_rect)

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500) 

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
                start_time = int(pygame.time.get_ticks()/1000)

        if event.type == obstacle_timer and game_active:
            print('go')
            if randint(0,2):
                obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1100),300)))
            else:     
                obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900,1100),210)))


    if game_active:
        #phong canh
        screen.blit(sky_surf, (0,0))
        screen.blit(ground_surf,(0,300))
        screen.blit(text_surf, (300,50))
        score = display_score()

        #score
        display_score()

        # obstacle movements
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #player movements
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_surf,player_rect)

        #collision
        game_active = collison(player_rect, obstacle_rect_list)

    else:
        game_over_screen()

    pygame.display.update()
    clock.tick(60)
