from math import sqrt

import pygame
import random

# Initialize the game
pygame.init()

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
player_movement = 5
player_x = (width / 2) - (img_width / 2)
player_y = height * 4 / 5
player_x_change = 0
x_min = 0
x_max = width - img_width
y_min = height / 2
y_max = height - img_width

# Enemy
enemy_img = []
enemy_movement = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_enemies = 6
enemy_movement = 4

for i in range(num_enemies):
    enemy_img.append(pygame.image.load('spider.png'))
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
score = 0


def draw_player(img, x, y):
    screen.blit(img, (x, y))


def draw_enemy(img, x, y, i):
    screen.blit(img[i], (x, y))


def shoot_lightning(x, y):
    global lightning_state
    lightning_state = 'fire'
    screen.blit(lightning_img, (x + lightning_width/2, y - lightning_width/2))


def is_collision(x1, y1, x2, y2):
    distance = sqrt(pow((x1 - x2), 2) + pow((y1 - y2), 2))
    if distance < img_width/2:
        return True
    else:
        return False


# Game loop
running = True
while running:
    # Background color
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # Quit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -player_movement
            if event.key == pygame.K_RIGHT:
                player_x_change = player_movement
            if event.key == pygame.K_SPACE:
                if lightning_state is 'ready':
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
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= x_min:
            enemy_x_change[i] = enemy_movement
            enemy_y[i] += enemy_y_change[i]
        if enemy_x[i] >= x_max:
            enemy_x_change[i] = -enemy_movement
            enemy_y[i] += enemy_y_change[i]

        # Collision
        if is_collision(enemy_x[i], enemy_y[i], lightning_x, lightning_y):
            lightning_y = height * 4 / 5
            lightning_state = 'ready'
            score += 1
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
    pygame.display.update()
