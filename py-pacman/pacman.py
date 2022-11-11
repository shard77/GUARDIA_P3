import copy  # Import des dépendances requises
import pygame
import math

from board import boards
from constants import * 

pygame.init() # Initisaliser pygame

screen = pygame.display.set_mode([WIDTH, HEIGHT]) # définir la taille de la fenêtre
timer = pygame.time.Clock() # Définir l'horloge pour la vitesse du jeu
font = pygame.font.Font('freesansbold.ttf', 20) # définir la police d'écriture pour notre jeu
level = copy.deepcopy(boards) # Définir le niveau actuel (un seul niveau est disponible, la map du jeu d'origine)
color = COLOR
PI = math.pi # Définir PI pour l'utliser dans les arcs de cercles

player_images = []
for i in range(1, 5): # Loop pour que chaque image du joueur soit ajoutée à la liste
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/img_joueur/{i}.png'), (45, 45)))

# Importer d'autres images pour les fantômes et définir leur taille
rouge_img = pygame.transform.scale(pygame.image.load(f'assets/img_fantomes/rouge.png'), (45, 45))
rose_img = pygame.transform.scale(pygame.image.load(f'assets/img_fantomes/rose.png'), (45, 45))
bleu_img = pygame.transform.scale(pygame.image.load(f'assets/img_fantomes/bleu.png'), (45, 45))
orange_img = pygame.transform.scale(pygame.image.load(f'assets/img_fantomes/orange.png'), (45, 45))
spooked_img = pygame.transform.scale(pygame.image.load(f'assets/img_fantomes/powerup.png'), (45, 45))
dead_img = pygame.transform.scale(pygame.image.load(f'assets/img_fantomes/mort.png'), (45, 45))

# Emplacement du joueur par défault
player_x = 450 
player_y = 663 
direction = 0 # direction par défault du joueur 

# emplacement et direction des fantômes par défault
rouge_x = 56 
rouge_y = 58 
rouge_direction = 0
bleu_x = 440
bleu_y = 388
bleu_direction = 2
rose_x = 440 
rose_y = 438
rose_direction = 2
orange_x = 440 
orange_y = 438
orange_direction = 2

counter = 0
flicker = False

turns_allowed = [False, False, False, False] # Liste pour définir à quel moment le joueur peut tourner
direction_command = 0 
player_speed = 2

score = 0
powerup = False
power_counter = 0

eaten_ghost = [False, False, False, False] # Liste pour les fantomes qui ont été mangés 
targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)] 

# Fantomes morts
rouge_dead = False
bleu_dead = False 
orange_dead = False
rose_dead = False

rouge_box = False
bleu_box = False
orange_box = False
rose_box = False

moving = False
ghost_speeds = [2, 2, 2, 2]

startup_counter = 0
lives = 3
game_over = False
game_won = False


class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id): # Init de la classe (définition des valeurs par défault)
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()

    def draw(self):
        if (not powerup and not self.dead) or (eaten_ghost[self.id] and powerup and not self.dead):
            screen.blit(self.img, (self.x_pos, self.y_pos))
        elif powerup and not self.dead and not eaten_ghost[self.id]:
            screen.blit(spooked_img, (self.x_pos, self.y_pos))
        else:
            screen.blit(dead_img, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return ghost_rect

    def check_collisions(self): # Check les collisions avec les murs pour nos fantômes
        num1 = ((HEIGHT - 50) // 32)
        num2 = (WIDTH // 30)
        num3 = 15
        self.turns = [False, False, False, False]
        if 0 < self.center_x // 30 < 29:
            if level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[1] = True
            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[0] = True
            if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[3] = True
            if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True
        if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:
            self.in_box = True
        else:
            self.in_box = False
        return self.turns, self.in_box

    def move_orange(self): # le fantome bouge a l'endroit le plus avantageux pour poursuivre le joueur - chaque fantome a un mouvement différent
        # 0 = Droite, 1 = Gauche, 2 = Haut, 3 = Bas
        match self.direction:
            case 0:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.x_pos += self.speed
                elif not self.turns[0]:
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                elif self.turns[0]:
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    if self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    else:
                        self.x_pos += self.speed
            
            case 1:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.x_pos -= self.speed
                elif not self.turns[1]:
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                elif self.turns[1]:
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    if self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    else:
                        self.x_pos -= self.speed
            
            case 2:
                if self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif not self.turns[2]:
                    if self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                elif self.turns[2]:
                    if self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    else:
                        self.y_pos -= self.speed
            
            case 3:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.y_pos += self.speed
                elif not self.turns[3]:
                    if self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                elif self.turns[3]:
                    if self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    else:
                        self.y_pos += self.speed

        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
            
        return self.x_pos, self.y_pos, self.direction

    def move_rouge(self): # le fantome bouge a l'endroit le plus avantageux pour poursuivre le joueur - chaque fantome a un mouvement différent
        # 0 = Droite, 1 = Gauche, 2 = Haut, 3 = Bas

        match self.direction:
            case 0:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.x_pos += self.speed
                elif not self.turns[0]:
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                elif self.turns[0]:
                    self.x_pos += self.speed
            
            case 1:
                if self.target[0] < self.x_pos and self.turns[1]:
                    self.x_pos -= self.speed
                elif not self.turns[1]:
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                elif self.turns[1]:
                    self.x_pos -= self.speed
            
            case 2:
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif not self.turns[2]:
                    if self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                elif self.turns[2]:
                    self.y_pos -= self.speed

            case 3:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.y_pos += self.speed
                elif not self.turns[3]:
                    if self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                elif self.turns[3]:
                    self.y_pos += self.speed

        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30

        return self.x_pos, self.y_pos, self.direction

    def move_bleu(self): # le fantome bouge a l'endroit le plus avantageux pour poursuivre le joueur - chaque fantome a un mouvement différent
        # 0 = Droite, 1 = Gauche, 2 = Haut, 3 = Bas
        # Le fantome bleu tourne de haut en bas a son avantage, mais de droite a gauche juste si il touche une collision  
        match self.direction:
            case 0:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.x_pos += self.speed
                elif not self.turns[0]:
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                elif self.turns[0]:
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    if self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    else:
                        self.x_pos += self.speed
            
            case 1:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.x_pos -= self.speed
                elif not self.turns[1]:
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                elif self.turns[1]:
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    if self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    else:
                        self.x_pos -= self.speed
            
            case 2:
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif not self.turns[2]:
                    if self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                elif self.turns[2]:
                    self.y_pos -= self.speed
        
            case 3:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.y_pos += self.speed
                elif not self.turns[3]:
                    if self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                elif self.turns[3]:
                    self.y_pos += self.speed
        
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        
        return self.x_pos, self.y_pos, self.direction

    def move_rose(self): # le fantome bouge a l'endroit le plus avantageux pour poursuivre le joueur - chaque fantome a un mouvement différent
        # 0 = Droite, 1 = Gauche, Haut = 2, Bas = 3
        # Le fantome bleu tourne a gauche ou a droite a son avantage, mais de haut en bas juste si il touche une collision  
        match self.direction:
            case 0:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.x_pos += self.speed
                elif not self.turns[0]:
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                elif self.turns[0]:
                    self.x_pos += self.speed
        
            case 1:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.x_pos -= self.speed
                elif not self.turns[1]:
                    if self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                elif self.turns[1]:
                    self.x_pos -= self.speed
            
            case 2:
                if self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif not self.turns[2]:
                    if self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.target[1] > self.y_pos and self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                elif self.turns[2]:
                    if self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    else:
                        self.y_pos -= self.speed
            
            case 3:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.y_pos += self.speed
                elif not self.turns[3]:
                    if self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.target[1] < self.y_pos and self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.turns[2]:
                        self.direction = 2
                        self.y_pos -= self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                elif self.turns[3]:
                    if self.target[0] > self.x_pos and self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.target[0] < self.x_pos and self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                    else:
                        self.y_pos += self.speed
        
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30

        return self.x_pos, self.y_pos, self.direction


def draw_misc(): # déssine le score, les vies et le message de fin de partie 
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, 920))
    if powerup:
        pygame.draw.circle(screen, 'blue', (140, 930), 15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (30, 30)), (650 + i * 40, 915))
    if game_over:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Game over! Space bar to restart!', True, 'red')
        screen.blit(gameover_text, (100, 300))
    if game_won:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Victory! Space bar to restart!', True, 'green')
        screen.blit(gameover_text, (100, 300))


def check_collisions(scor, power, power_count, eaten_ghosts):
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    
    if 0 < player_x < 870:
        if level[center_y // num1][center_x // num2] == 1:
            level[center_y // num1][center_x // num2] = 0
            scor += 10
        if level[center_y // num1][center_x // num2] == 2:
            level[center_y // num1][center_x // num2] = 0
            scor += 50
            power = True
            power_count = 0
            eaten_ghosts = [False, False, False, False]
    
    return scor, power, power_count, eaten_ghosts


def draw_board(): # déssine le labyrinthe
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    for i in range(len(level)): # loop pour itérer sur les lignes de boards.py 
        for j in range(len(level[i])):
            match level[i][j]:
                case 1:
                    pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
                
                case 2:
                    if not flicker:
                        pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
                
                case 3:
                    pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1), (j * num2 + (0.5 * num2), i * num1 + num1), 3)
                
                case 4:
                    pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)), (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
                
                case 5:
                    pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1], 0, PI / 2, 3)
                
                case 6:
                    pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
                
                case 7:
                    pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI, 3 * PI / 2, 3)
                
                case 8:
                    pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2, 2 * PI, 3)
                
                case 9:
                    pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)), (j * num2 + num2, i * num1 + (0.5 * num1)), 3)


def draw_player(): # déssine le joueur
    # 0 = Droite, 1 = Gauche, 2 = Haut, 3 = Bas
    match direction:
        case 0:
            screen.blit(player_images[counter // 5], (player_x, player_y))
        
        case 1:
            screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
        
        case 2:
            screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
        
        case 3:
            screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))


def check_position(centerx, centery):  # check les collisions basées sur center x et center y du joueur +/- fudge number (fudge number permet de laisser un espace entre le mur et le joueur pour la collision)
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    num3 = 15
    if centerx // 30 < 29:
        match direction:
            case 0:
                if 12 <= centerx % num2 <= 18:
                    if level[(centery + num1) // num1][centerx // num2] < 3:
                        turns[3] = True
                    if level[(centery - num1) // num1][centerx // num2] < 3:
                        turns[2] = True
                if 12 <= centery % num1 <= 18:
                    if level[centery // num1][(centerx - num3) // num2] < 3:
                        turns[1] = True
                    if level[centery // num1][(centerx + num3) // num2] < 3:
                        turns[0] = True

                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
            
            case 1:
                if 12 <= centerx % num2 <= 18:
                    if level[(centery + num1) // num1][centerx // num2] < 3:
                        turns[3] = True
                    if level[(centery - num1) // num1][centerx // num2] < 3:
                        turns[2] = True
                if 12 <= centery % num1 <= 18:
                    if level[centery // num1][(centerx - num3) // num2] < 3:
                        turns[1] = True
                    if level[centery // num1][(centerx + num3) // num2] < 3:
                        turns[0] = True

                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
            
            case 2:
                if 12 <= centerx % num2 <= 18:
                    if level[(centery + num3) // num1][centerx // num2] < 3:
                        turns[3] = True
                    if level[(centery - num3) // num1][centerx // num2] < 3:
                        turns[2] = True
                if 12 <= centery % num1 <= 18:
                    if level[centery // num1][(centerx - num2) // num2] < 3:
                        turns[1] = True
                    if level[centery // num1][(centerx + num2) // num2] < 3:
                        turns[0] = True

                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
            
            case 3:
                if 12 <= centerx % num2 <= 18:
                    if level[(centery + num3) // num1][centerx // num2] < 3:
                        turns[3] = True
                    if level[(centery - num3) // num1][centerx // num2] < 3:
                        turns[2] = True
                if 12 <= centery % num1 <= 18:
                    if level[centery // num1][(centerx - num2) // num2] < 3:
                        turns[1] = True
                    if level[centery // num1][(centerx + num2) // num2] < 3:
                        turns[0] = True

                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True

            
            case _:
                turns[0] = True
                turns[1] = True
    
    return turns


def move_player(play_x, play_y): # permet de bouger le joueur
    # 0 = Droite, 1 = Gauche, 2 = Haut , 3 = Bas
    match direction:
        case 0:
            if turns_allowed[0]:
                play_x += player_speed
        
        case 1:
            if turns_allowed[1]:
                play_x -= player_speed
        
        case 2:
            if turns_allowed[2]:
                play_y -= player_speed
        
        case 3:
            if turns_allowed[3]:
                play_y += player_speed

    return play_x, play_y


def get_targets(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y): # Logique des fantomes quand le joueur a mangé un powerup
    if player_x < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if player_y < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    return_target = (380, 400)
    if powerup:
        if not rouge.dead and not eaten_ghost[0]:
            blink_target = (runaway_x, runaway_y)
        elif not rouge.dead and eaten_ghost[0]:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not bleu.dead and not eaten_ghost[1]:
            ink_target = (runaway_x, player_y)
        elif not bleu.dead and eaten_ghost[1]:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not rose.dead:
            pink_target = (player_x, runaway_y)
        elif not rose.dead and eaten_ghost[2]:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not orange.dead and not eaten_ghost[3]:
            clyd_target = (450, 450)
        elif not orange.dead and eaten_ghost[3]:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
    else:
        if not rouge.dead:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not bleu.dead:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not rose.dead:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not orange.dead:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
    return [blink_target, ink_target, pink_target, clyd_target]


run = True # True pour faire une loop infinie
while run:
    timer.tick(FPS) # Framerate
    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True
    if powerup and power_counter < 600:
        power_counter += 1
    elif powerup and power_counter >= 600:
        power_counter = 0
        powerup = False
        eaten_ghost = [False, False, False, False]
    if startup_counter < 180 and not game_over and not game_won:
        moving = False
        startup_counter += 1
    else:
        moving = True

    screen.fill('black') # Remplit le fond d'écran de noir
    draw_board() # Dessine le labyrinthe
    center_x = player_x + 23
    center_y = player_y + 24

    if powerup: # Si le joueur mange un powerup les fantomes sont moins rapides
        ghost_speeds = [1, 1, 1, 1]
    else:
        ghost_speeds = [2, 2, 2, 2]

    if eaten_ghost[0]: # Reset de la vitesse lors du respawn si un fantome s'est fait mangé
        ghost_speeds[0] = 2
    if eaten_ghost[1]:
        ghost_speeds[1] = 2
    if eaten_ghost[2]:
        ghost_speeds[2] = 2
    if eaten_ghost[3]:
        ghost_speeds[3] = 2
    if rouge_dead:
        ghost_speeds[0] = 4
    if bleu_dead:
        ghost_speeds[1] = 4
    if rose_dead:
        ghost_speeds[2] = 4
    if orange_dead:
        ghost_speeds[3] = 4

    game_won = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            game_won = False

    player_circle = pygame.draw.circle(screen, 'black', (center_x, center_y), 20, 2)

    draw_player()

    rouge = Ghost(rouge_x, rouge_y, targets[0], ghost_speeds[0], rouge_img, rouge_direction, rouge_dead,
                   rouge_box, 0)
    bleu = Ghost(bleu_x, bleu_y, targets[1], ghost_speeds[1], bleu_img, bleu_direction, bleu_dead,
                 bleu_box, 1)
    rose = Ghost(rose_x, rose_y, targets[2], ghost_speeds[2], rose_img, rose_direction, rose_dead,
                  rose_box, 2)
    orange = Ghost(orange_x, orange_y, targets[3], ghost_speeds[3], orange_img, orange_direction, orange_dead,
                  orange_box, 3)
    draw_misc()

    targets = get_targets(rouge_x, rouge_y, bleu_x, bleu_y, rose_x, rose_y, orange_x, orange_y)
    turns_allowed = check_position(center_x, center_y)

    if moving:
        player_x, player_y = move_player(player_x, player_y)
        if not rouge_dead and not rouge.in_box:
            rouge_x, rouge_y, rouge_direction = rouge.move_rouge()
        else:
            rouge_x, rouge_y, rouge_direction = rouge.move_orange()
        if not rose_dead and not rose.in_box:
            rose_x, rose_y, rose_direction = rose.move_rose()
        else:
            rose_x, rose_y, rose_direction = rose.move_orange()
        if not bleu_dead and not bleu.in_box:
            bleu_x, bleu_y, bleu_direction = bleu.move_bleu()
        else:
            bleu_x, bleu_y, bleu_direction = bleu.move_orange()
        orange_x, orange_y, orange_direction = orange.move_orange()
    score, powerup, power_counter, eaten_ghost = check_collisions(score, powerup, power_counter, eaten_ghost)

    if not powerup: # Si le joueur n'a pas mangé de powerup et qu'un fantome le mange
        if (player_circle.colliderect(rouge.rect) and not rouge.dead) or \
                (player_circle.colliderect(bleu.rect) and not bleu.dead) or \
                (player_circle.colliderect(rose.rect) and not rose.dead) or \
                (player_circle.colliderect(orange.rect) and not orange.dead):
            if lives > 0:
                lives -= 1
                startup_counter = 0
                powerup = False
                power_counter = 0
                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0
                rouge_x = 56
                rouge_y = 58
                rouge_direction = 0
                bleu_x = 440
                bleu_y = 388
                bleu_direction = 2
                rose_x = 440
                rose_y = 438
                rose_direction = 2
                orange_x = 440
                orange_y = 438
                orange_direction = 2
                eaten_ghost = [False, False, False, False]
                rouge_dead = False
                bleu_dead = False
                orange_dead = False
                rose_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0

    if powerup and player_circle.colliderect(rouge.rect) and eaten_ghost[0] and not rouge.dead: # Si le joueur a mangé un powerup mais que le fantome mangé respawn
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            player_x = 450
            player_y = 663
            direction = 0
            direction_command = 0
            rouge_x = 56
            rouge_y = 58
            rouge_direction = 0
            bleu_x = 440
            bleu_y = 388
            bleu_direction = 2
            rose_x = 440
            rose_y = 438
            rose_direction = 2
            orange_x = 440
            orange_y = 438
            orange_direction = 2
            eaten_ghost = [False, False, False, False]
            rouge_dead = False
            bleu_dead = False
            orange_dead = False
            rose_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0

    if powerup and player_circle.colliderect(bleu.rect) and eaten_ghost[1] and not bleu.dead:
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            player_x = 450
            player_y = 663
            direction = 0
            direction_command = 0
            rouge_x = 56
            rouge_y = 58
            rouge_direction = 0
            bleu_x = 440
            bleu_y = 388
            bleu_direction = 2
            rose_x = 440
            rose_y = 438
            rose_direction = 2
            orange_x = 440
            orange_y = 438
            orange_direction = 2
            eaten_ghost = [False, False, False, False]
            rouge_dead = False
            bleu_dead = False
            orange_dead = False
            rose_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0

    if powerup and player_circle.colliderect(rose.rect) and eaten_ghost[2] and not rose.dead:
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            player_x = 450
            player_y = 663
            direction = 0
            direction_command = 0
            rouge_x = 56
            rouge_y = 58
            rouge_direction = 0
            bleu_x = 440
            bleu_y = 388
            bleu_direction = 2
            rose_x = 440
            rose_y = 438
            rose_direction = 2
            orange_x = 440
            orange_y = 438
            orange_direction = 2
            eaten_ghost = [False, False, False, False]
            rouge_dead = False
            bleu_dead = False
            orange_dead = False
            rose_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0

    if powerup and player_circle.colliderect(orange.rect) and eaten_ghost[3] and not orange.dead:
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            player_x = 450
            player_y = 663
            direction = 0
            direction_command = 0
            rouge_x = 56
            rouge_y = 58
            rouge_direction = 0
            bleu_x = 440
            bleu_y = 388
            bleu_direction = 2
            rose_x = 440
            rose_y = 438
            rose_direction = 2
            orange_x = 440
            orange_y = 438
            orange_direction = 2
            eaten_ghost = [False, False, False, False]
            rouge_dead = False
            bleu_dead = False
            orange_dead = False
            rose_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0

    if powerup and player_circle.colliderect(rouge.rect) and not rouge.dead and not eaten_ghost[0]:
        rouge_dead = True
        eaten_ghost[0] = True
        score += (2 ** eaten_ghost.count(True)) * 100

    if powerup and player_circle.colliderect(bleu.rect) and not bleu.dead and not eaten_ghost[1]:
        bleu_dead = True
        eaten_ghost[1] = True
        score += (2 ** eaten_ghost.count(True)) * 100

    if powerup and player_circle.colliderect(rose.rect) and not rose.dead and not eaten_ghost[2]:
        rose_dead = True
        eaten_ghost[2] = True
        score += (2 ** eaten_ghost.count(True)) * 100

    if powerup and player_circle.colliderect(orange.rect) and not orange.dead and not eaten_ghost[3]:
        orange_dead = True
        eaten_ghost[3] = True
        score += (2 ** eaten_ghost.count(True)) * 100

    for event in pygame.event.get(): # Check les events des touches clavier
        match event.type:
            case pygame.QUIT: # Si l'utilisateur clique sur la croix de la fenêtre
                run = False

            case pygame.KEYDOWN: # Si une touche est appuyée
                match event.key:
                    case pygame.K_RIGHT:
                        direction_command = 0
                    
                    case pygame.K_LEFT:
                        direction_command = 1
                    
                    case pygame.K_UP:
                        direction_command = 2
                    
                    case pygame.K_DOWN:
                        direction_command = 3
                    
                    case pygame.K_SPACE:
                        if game_over or game_won:
                            power_counter = 0
                            lives -= 1
                            startup_counter = 0
                            player_x = 450
                            player_y = 663
                            direction = 0
                            direction_command = 0
                            rouge_x = 56
                            rouge_y = 58
                            rouge_direction = 0
                            bleu_x = 440
                            bleu_y = 388
                            bleu_direction = 2
                            rose_x = 440
                            rose_y = 438
                            rose_direction = 2
                            orange_x = 440
                            orange_y = 438
                            orange_direction = 2
                            eaten_ghost = [False, False, False, False]
                            rouge_dead = False
                            bleu_dead = False
                            orange_dead = False
                            rose_dead = False
                            score = 0
                            lives = 3
                            level = copy.deepcopy(boards)
                            game_over = False
                            game_won = False

            case pygame.KEYUP:
                match event.key:
                    case pygame.K_RIGHT:
                        if direction_command == 0:
                            direction_command = direction
                    
                    case pygame.K_LEFT:
                        if direction_command == 1:
                            direction_command = direction
                    
                    case pygame.K_UP:
                        if direction_command == 2:
                            direction_command = direction 
                    
                    case pygame.K_DOWN:
                        if direction_command == 3:
                            direction_command = direction
    
        match direction_command:
            case 0:
                if turns_allowed[0]:
                    direction = 0
            
            case 1:
                if turns_allowed[1]:
                    direction = 1
            
            case 2:
                if turns_allowed[2]:
                    direction = 2
            
            case 3:
                if turns_allowed[3]:
                    direction = 3

    if player_x > 900:
        player_x = -47
    elif player_x < -50:
        player_x = 897

    if rouge.in_box and rouge_dead:
        rouge_dead = False
    if bleu.in_box and bleu_dead:
        bleu_dead = False
    if rose.in_box and rose_dead:
        rose_dead = False
    if orange.in_box and orange_dead:
        orange_dead = False

    pygame.display.flip()
pygame.quit()
