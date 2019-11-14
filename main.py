from math import sqrt
import pygame
import random
from pygame import mixer

# Initialize the game
pygame.init()

# Game sounds
background_sound = 'background.wav'
mixer.music.load(background_sound)
mixer.music.set_volume(0.3)
mixer.music.play(-1)
yells = ['yell.wav',
         'yell2.wav']

# Create the screen
img_width = 64
lightning_width = 32
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
background = pygame.image.load('leaf.jpg')

# Caption and Image
pygame.display.set_caption('Bug Wars')
icon = pygame.image.load('bee.png')
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load('bee.png')
player_images = ['bee.png',
                 'butterfly.png',
                 'ladybug.png']
player_selected_image = player_images[0]        # to do
player_movement = 5
player_x = (width / 2) - (img_width / 2)
player_y = height * 4 / 5
player_x_change = 0
x_min = 0
x_max = width - img_width
y_min = height / 2
y_max = height - img_width

# Enemies
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_enemies = 5
enemy_movement = 4

for i in range(num_enemies):
    enemy_img.append(pygame.image.load('fly.png'))
    enemy_x.append(random.randint(0, (width - img_width - 1)))
    enemy_y.append(random.randint((height * 1 / 5), (height * 2 / 5)))
    enemy_x_change.append(enemy_movement)
    enemy_y_change.append(height / 20)

# Lightning
lightning_img = pygame.image.load('lightning.png')
lightning_x = 0
lightning_y = height * 4 / 5
lightning_x_change = 0
lightning_y_change = 10
lightning_state = 'ready'

# Scoring
score_value = 0
score_x = 10
score_y = 10

# Game over
game_over = False


def draw_player_sprites():
    home_font = pygame.font.Font('plantletters.ttf', 48)
    home_text = home_font.render('Choose Your Bug', True, (255, 255, 255))
    home_text_rect = home_text.get_rect(center=(width/2, height/3))
    screen.blit(home_text, home_text_rect)

    num_sprites = len(player_images) + 1
    for i in range(1, num_sprites):
        img = pygame.image.load(player_images[i-1])
        img_x = ((width/num_sprites + 1) * i) - img_width / 2
        img_y = 400
        screen.blit(img, (img_x, img_y))


def show_score(x, y):
    score_font = pygame.font.Font('plantletters.ttf', 32)
    score = score_font.render('Score: ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def show_game_over():
    mixer.music.stop()
    game_over_font = pygame.font.Font('freesansbold.ttf', 64)
    game_over_text = game_over_font.render('GAME OVER', True, (255, 0, 0))
    game_over_text_rect = game_over_text.get_rect(center=(width/2, height/2))
    screen.blit(game_over_text, game_over_text_rect)


def draw_player(img, x, y):
    screen.blit(img, (x, y))


def draw_enemy(img, x, y, i):
    screen.blit(img[i], (x, y))


def shoot_lightning(x, y):
    global lightning_state
    lightning_state = 'fire'
    screen.blit(lightning_img, (x + lightning_width/2, y - lightning_width/2))


def is_collision(x1, y1, x2, y2):
    collision_distance = sqrt(pow((x1 - x2), 2) + pow((y1 - y2), 2))
    if collision_distance < img_width/2:
        return True
    else:
        return False


# Home screen loop
running_home = True
running = False
while running_home:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    draw_player_sprites()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_home = False
        '''if event.type == pygame.MOUSEBUTTONDOWN:
        
        
        YOU ARE HERE
        
        
        '''

    pygame.display.update()

# Game loop
while running:
    # Background color
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))


    # Quit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Left
            if event.key == pygame.K_LEFT:
                player_x_change = -player_movement
            # Right
            if event.key == pygame.K_RIGHT:
                player_x_change = player_movement
            # Space
            if event.key == pygame.K_SPACE:
                if lightning_state is 'ready':
                    lightning_sound = mixer.Sound('laser.wav')
                    mixer.Sound.set_volume(lightning_sound, 0.5)
                    lightning_sound.play()
                    lightning_x = player_x
                    shoot_lightning(lightning_x, lightning_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Adjust player x and y values
    player_x += player_x_change
    if player_x <= x_min:
        player_x = x_min
    if player_x >= x_max:
        player_x = x_max

    # Adjust enemy x and y values
    for i in range(num_enemies):
        # Game over
        if game_over:
            show_game_over()
            break
        if enemy_y[i] >= player_y - img_width:
            game_over_distance = sqrt(pow((player_x - enemy_x[i]), 2) + pow((player_y - enemy_y[i]), 2))
            if game_over_distance < img_width:
                for j in range(num_enemies):
                    enemy_x[j] = 1000
                game_over = True

        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= x_min:
            enemy_x_change[i] = enemy_movement
            enemy_y[i] += enemy_y_change[i]
        if enemy_x[i] >= x_max:
            enemy_x_change[i] = -enemy_movement
            enemy_y[i] += enemy_y_change[i]

        # Collision
        if is_collision(enemy_x[i], enemy_y[i], lightning_x, lightning_y):

            random_yell = random.randint(0, len(yells) - 1)
            collision_sound = mixer.Sound(yells[random_yell])
            collision_sound.play()
            lightning_y = height * 4 / 5
            lightning_state = 'ready'
            score_value += 1
            enemy_x[i] = random.randint(0, (width - img_width - 1))
            enemy_y[i] = random.randint((height * 1 / 5), (height * 2 / 5))

        draw_enemy(enemy_img, enemy_x[i], enemy_y[i], i)

    # Adjust lightning x and y values
    if lightning_y <= 0:
        lightning_y = height * 4 / 5
        lightning_state = 'ready'
    if lightning_state is 'fire':
        shoot_lightning(lightning_x, lightning_y)
        lightning_y -= lightning_y_change

    # Load player and enemy
    draw_player(player_img, player_x, player_y)
    show_score(score_x, score_y)
    pygame.display.update()
