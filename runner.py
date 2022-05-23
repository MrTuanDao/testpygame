
from sys import exit
import pygame
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        self.player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [self.player_walk_1, self.player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0
        self.cool_down = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        
    
        self.cool_down = self.cool_down +  1
        print(self.cool_down)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
         
            self.gravity = -20
            self.jump_sound.play()
            print('single')
        
        if keys[pygame.K_UP] and self.cool_down > 300:
            print('double')
            self.cool_down = 0
            self.gravity = -20
        
        
        
        
            

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300: self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): 
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
        if self.cool_down > 300:
            pygame.draw.circle(screen,'White',(200,100), 30)
        else: pygame.draw.circle(screen,'Black',(200,100), 30)
        

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
       

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type) :
        super().__init__()

        if type =='fly':
            self.fly_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            self.fly_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [self.fly_1, self.fly_2]
            y_pos = 210
        
        if type == 'snail':
            self.snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            self.snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [self.snail_1,self.snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

    def animation_state(self):
        # if randint(0,2): self.type = 'snail'
        # else: self.type = 'fly'
        if self.animation_index == 0: self.animation_index = 1
        else: self.animation_index = 0
        self.image = self.frames[self.animation_index]
        
    def destroy(self):
        if self.rect.x <= 100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= 6

def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surf = font.render(f'Score: {current_time}', False, 'Brown')
    score_rect = score_surf.get_rect(center = (400,100))
    box_color = '#c0e8ec'
    pygame.draw.rect(screen, box_color, score_rect)
    screen.blit(score_surf, score_rect)
    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else: return True


pygame.init()
width = 800
height = 400
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("RUNNER")

#clock
clock = pygame.time.Clock()
font = pygame.font.Font('font/Pixeltype.ttf',50)
game_active = False
start_time = 0
score = 0
bg = pygame.mixer.Sound('audio/music.wav')
bg.set_volume(1)
bg.play(loops = -1)

#groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()
text_color = (64,64,64)
text_surf = font.render('Mygame for now', None, text_color)

#intro screen
def game_over_screen():
    #player stand
    player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
    player_stand = pygame.transform.scale2x(player_stand)
    player_stand_rec = player_stand.get_rect(center = (400, 200))
    screen.fill((94,129,162))
    screen.blit(player_stand, player_stand_rec)

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

        if event.type == pygame.KEYDOWN:
            print('keydown')

        if game_active:
            if event.type == obstacle_timer :
                obstacle_group.add(Obstacle(choice(['fly','snail','snail'])))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks()/1000)

    if game_active:
        #phong canh
        screen.blit(sky_surf, (0,0))
        screen.blit(ground_surf,(0,300))
        screen.blit(text_surf, (300,50))
        score = display_score()

        #score
        display_score()
  
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        #collision
        game_active = collision_sprite()

    else:
        game_over_screen()

    pygame.display.update()
    clock.tick(60)
