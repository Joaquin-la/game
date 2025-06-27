import pygame
from sys import exit
import math
import random as rand
import heapq
import asyncio

pygame.init()
pygame.display.set_caption('GAME')

clock = pygame.time.Clock()

game_active = True
xpos = 20
ypos = 350
score = 0  
level = 0
SCREEN_WIDTH= 800
SCREEN_HEIGHT = 600
white = (255, 255, 255)
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

positions = [

    (100, 100), (200, 100), (300, 100), (400, 100),
    (100, 150), (200, 150), (300, 150), (400, 150),
    (100, 450), (200, 450), (300, 450), (400, 450),
    (100, 300), (200, 300), (300, 300), (400, 300),
    (100, 350), (200, 350), (300, 350), (400, 350),
    (500, 100), (600, 100), (700, 100),
    (500, 250), (600, 250), (700, 250),
    (500, 450), (600, 450), (700, 450),
    (500, 350), (600, 350), (700, 350),

   
]
font = pygame.font.Font('Pixeltype.ttf', 50)

text_surface = font.render('Score:', False, (64, 64, 64))
text_rect = text_surface.get_rect(center=(325, 50))
score_surface = font.render(str(score), False, (64, 64, 64))  
score_rect = score_surface.get_rect(center=(400, 50))
game_surface = font.render('Game Over', False, 'White')
game_rect = game_surface.get_rect(center=(400, 200))
play_sur = font.render('PLAY AGAIN', False, 'White')
play_rect = play_sur.get_rect(center=(400, 300))

pygame.mixer.music.load("music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(loops=-1, start=0.0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
ice_surface = pygame.image.load('ice.jpg').convert()
lava_surface = pygame.image.load('lava.jpg').convert()
player_surface = pygame.image.load('player.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom=(xpos, ypos))
gun_img = pygame.image.load('gun.png').convert_alpha()
bullet_img = pygame.image.load('bullet.png').convert_alpha()
bullet_rect = bullet_img.get_rect()
enemy_img = pygame.image.load('enemy.png').convert_alpha()
lava_block = pygame.image.load('lava_block.jpg')
lava_rect = lava_block.get_rect()
game_over = pygame.image.load('game_over.png').convert()
ice_block = pygame.image.load('ice_block.png')
ice_block_rect = ice_block.get_rect()
def create_grid(positions):
    grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]  
    for pos in positions:
        x, y = pos
        grid[y // GRID_SIZE][x // GRID_SIZE] = 1  
    return grid
MIN_DISTANCE_FROM_PLAYER =300
def create_enemy():
    while True:
       
        enemy_rect = pygame.Rect(rand.randrange(SCREEN_WIDTH), rand.randrange(SCREEN_HEIGHT), 20, 20)
        
        for block_pos in positions:
            block_rect = pygame.Rect(block_pos[0], block_pos[1], 20, 20)
            if enemy_rect.colliderect(block_rect):
                break  
        else:
            distance = math.sqrt((enemy_rect.centerx - player_rect.centerx) ** 2 +
                                 (enemy_rect.centery - player_rect.centery) ** 2)
            if distance > MIN_DISTANCE_FROM_PLAYER:
                return enemy_rect
enemies = [create_enemy()] 


enemy_speed = 1
bullets = []


def move_enemy_towards_player(enemy_rect, player_rect, speed=2):
 
    dx = player_rect.centerx - enemy_rect.centerx
    dy = player_rect.centery - enemy_rect.centery

    distance = math.sqrt(dx ** 2 + dy ** 2)

    if distance != 0: 
        dx /= distance
        dy /= distance

    enemy_rect.x += dx * speed
    enemy_rect.y += dy * speed

def check_collision_with_ice_block(player_rect, ice_block_positions):


    ice_block_rects = [pygame.Rect(pos[0], pos[1], 20, 20) for pos in ice_block_positions]
    

    for block_rect in ice_block_rects:
        if player_rect.colliderect(block_rect):
            return True
        
    return False
def remove_bullets_on_ice_block_collision(bullets, ice_block_positions):
    ice_block_rects = [pygame.Rect(pos[0], pos[1], 20, 20) for pos in ice_block_positions] 
    for bullet_tuple in bullets[:]:
        bullet_rect, _ = bullet_tuple
        for block_rect in ice_block_rects:
            if bullet_rect.colliderect(block_rect):
                bullets.remove(bullet_tuple)  
                break
    return bullets
move_amount = 5

while True:

    pygame.mixer.music.unpause() 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - player_rect.centerx
            dy = mouse_y - player_rect.centery
            distance = math.sqrt(dx ** 2 + dy ** 2)
            dx /= distance
            dy /= distance
            bullets.append([pygame.Rect(player_rect.centerx, player_rect.centery, 10, 10), [dx, dy]])
    if game_active:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_rect.x += move_amount
            if check_collision_with_ice_block(player_rect, positions): 
                player_rect.x -= move_amount
            if player_rect.right > SCREEN_WIDTH:
                player_rect.right = SCREEN_WIDTH
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_rect.x -= move_amount
            if check_collision_with_ice_block(player_rect, positions): 
                player_rect.x += move_amount
            if player_rect.left < 0:
                player_rect.left = 0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_rect.y -= move_amount
            if check_collision_with_ice_block(player_rect, positions): 
                player_rect.y += move_amount
            if player_rect.top < 0:
                player_rect.top = 0
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_rect.y += move_amount
            if check_collision_with_ice_block(player_rect, positions): 
                player_rect.y -= move_amount
        if score > len(enemies):  
            enemies.append(create_enemy())
        if player_rect.bottom > SCREEN_HEIGHT:
            player_rect.bottom = SCREEN_HEIGHT

        for enemy_rect in enemies:
            move_enemy_towards_player(enemy_rect, player_rect, enemy_speed)

        screen.fill(white)
        screen.blit(ice_surface, (0, 0)) 
        for pos in positions:
            ice_block_rect = pygame.Rect(pos[0], pos[1], 20, 20)
            screen.blit(ice_block, ice_block_rect)
       
        screen.blit(player_surface, player_rect)
       
        pos = pygame.mouse.get_pos()
        angle = 360 - math.atan2(pos[1] - player_rect.centery, pos[0] - player_rect.centerx) * 180 / math.pi
        rotated_gun = pygame.transform.rotate(gun_img, angle)
        screen.blit(rotated_gun, (player_rect.centerx - rotated_gun.get_width() / 2, player_rect.centery - rotated_gun.get_height() / 2))
       
        for bullet_tuple in bullets[:]:
            
            bullet_rect, bullet_velocity = bullet_tuple
            bullet_rect.x += bullet_velocity[0] * 10
            bullet_rect.y += bullet_velocity[1] * 10
            screen.blit(bullet_img, bullet_rect)
     
            for enemy_rect in enemies[:]:
                if bullet_rect.colliderect(enemy_rect):
                    enemies.remove(enemy_rect)
                    bullets.remove(bullet_tuple)
                    score += 1
                    break
            if (bullet_rect.x > SCREEN_WIDTH or bullet_rect.y > SCREEN_HEIGHT or 
                bullet_rect.x < 0 or bullet_rect.y < 0):
                bullets.remove(bullet_tuple)
        bullets = remove_bullets_on_ice_block_collision(bullets, positions)
        for enemy_rect in enemies:
            screen.blit(enemy_img, enemy_rect)
        score_surface = font.render(str(score), False, (64, 64, 64))
        screen.blit(text_surface, text_rect)
        screen.blit(score_surface, score_rect)
        for enemy_rect in enemies:
            if enemy_rect.colliderect(player_rect):
                game_active = False
        if score >=4 and score<10 :
            positions = [(300, 150), (100, 250), (500, 150), (200, 150), (700, 150), (500, 300),
 (400, 100), (700, 300), (600, 100),
 (300, 100), (500, 100), (100, 100), (100, 150), (600, 300), (300, 250),
 (500, 350), (200, 100), (700, 350), (400, 150), (600, 350), (700, 100), (100,500), (150,500), (300, 400),(100,400), (200,450),(500,500)]
            ice_surface = lava_surface
            ice_block = lava_block
            move_amount = 8 
            enemy_speed = 2.3



    else:
        pygame.mixer.music.pause() 
        screen.blit(game_over, (0, 0))
        score_surface = font.render(f'Score: {score}', False, 'White')
        screen.blit(score_surface,(50,50))
        screen.blit(game_surface, game_rect)
        screen.blit(play_sur, play_rect)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if play_rect.collidepoint(mouse_x, mouse_y):
                game_active = True
                ice_surface = pygame.image.load('ice.jpg').convert()
                lava_surface = pygame.image.load('lava.jpg').convert()
                ice_block = pygame.image.load('ice_block.png')
                ice_block_rect = ice_block.get_rect()
                move_amount = 5
                player_rect = player_surface.get_rect(midbottom=(xpos, ypos)) 
                score = 0
                bullets.clear()
                enemies = [create_enemy()]  
                enemy_x = rand.randrange(SCREEN_WIDTH)
                enemy_y = rand.randrange(SCREEN_HEIGHT)
                enemy_rect = pygame.Rect(enemy_x, enemy_y, 20, 20)
                enemy_speed = 1
                positions = [

            (100, 100), (200, 100), (300, 100), (400, 100),
            (100, 150), (200, 150), (300, 150), (400, 150),
            (100, 450), (200, 450), (300, 450), (400, 450),
            (100, 300), (200, 300), (300, 300), (400, 300),
            (100, 350), (200, 350), (300, 350), (400, 350),
            (500, 100), (600, 100), (700, 100),
            (500, 250), (600, 250), (700, 250),
            (500, 450), (600, 450), (700, 450),
            (500, 350), (600, 350), (700, 350),

        
        ]
    pygame.display.flip()
    clock.tick(60)