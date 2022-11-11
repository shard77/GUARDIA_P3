import pygame
import random
import math
from math import inf as infinity
import sys
import os
import time

from constants import *

pygame.font.init() # Initialiser la police d'écriture utilisée 

Win = pygame.display.set_mode((WIDTH, HEIGHT))

Cross = pygame.transform.scale(pygame.image.load(os.path.join("assets", "cross.png")), (WIDTH // 3, HEIGHT // 3)) # Définir notre croix
Circle = pygame.transform.scale(pygame.image.load(os.path.join("assets", "circle.png")), (WIDTH // 3, HEIGHT // 3)) # Définir notre rond 

Bg = (0, 0, 0) # Noir 
Clock = pygame.time.Clock()

AI = +1
Human = -1


def fill(surface, color):
    w, h = surface.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color(r, g, b, a))

def create_board():
    new_board = [[0 for i in range(3)] for j in range(3)]
    return new_board


def check_game(board, player):
    for row in board:
        if row[0] == row[1] == row[2] == player:
            return True

    for col in range(len(board)):
        check = []
        for row in board:
            check.append(row[col])
        if check.count(player) == len(check) and check[0] != 0:
            return True

    diags = []
    for indx in range(len(board)):
        diags.append(board[indx][indx])
    if diags.count(player) == len(diags) and diags[0] != 0:
        return True

    diags_2 = []
    for indx, rev_indx in enumerate(reversed(range(len(board)))):
        diags_2.append(board[indx][rev_indx])
    if diags_2.count(player) == len(diags_2) and diags_2[0] != 0:
        return True

    if len(empty_cells(board)) == 0:
        return True


def empty_cells(board):
    empty_cells = []
    for y,row in enumerate(board):
        for x,case in enumerate(row):
            if case == 0:
                empty_cells.append([x, y])

    return empty_cells

def valid_locations(board, x, y, player):
    if [x, y] in empty_cells(board):
        return True
    else:
        return False

def set_locations(board, x, y, player):
    if valid_locations(board, x, y, player):
        board[y][x] = player
        return True
    else:
        return False

def is_terminal_node(board):
    return check_game(board, +1) or check_game(board, -1)


def evaluate(board):
    if check_game(board, 1):
        score = 1
    elif check_game(board, -1):
        score = -1
    else:
        score = 0

    return score


def minimax(board, depth, alpha, beta, player):
    if player == AI:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or is_terminal_node(board):
        score = evaluate(board)
        return [-1, -1, score]

    for location in empty_cells(board):
        x, y = location[0], location[1]
        board[y][x] = player
        info = minimax(board, depth-1, alpha, beta, -player)
        board[y][x] = 0
        info[0], info[1] = x, y

        if player == AI:
            if info[2] > best[2]:
                best = info
            alpha = max(alpha, best[2])
            if alpha >= beta:
                break

        else:
            if best[2] > info[2]:
                best = info
            beta = min(beta, best[2])
            if alpha >= beta:
                break

    return best

def text_objects(text, font):
    textSurface = font.render(text, True, "white")
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((WIDTH / 2),(HEIGHT / 2))
    Win.blit(TextSurf, TextRect)

    pygame.display.update()
    time.sleep(2)


def ai_turn(board, alpha, beta):
    depth = len(empty_cells(board))

    if depth == 0 or is_terminal_node(board):
        return

    if depth == 9:
        x = random.choice([0, 1, 2])
        y = random.choice([0, 1, 2])
    else:
        move = minimax(board, depth, alpha, beta, AI)
        x,y = move[0], move[1]


    set_locations(board,x,y, AI)


def print_board(board):
    for row in board:
        print(row)

def reset_board(board):
    for x, row in enumerate(board):
        for y in range(len(row)):
            board[y][x] = 0


def draw_board(Win):
    for i in range(1, 3): #Draw vertical lines
        pygame.draw.line(Win, (255, 255, 255), (WIDTH * (i / 3), 0), (WIDTH * (i / 3), HEIGHT), 1)

    for j in range(1, 3): #Draw horizontal lines
        pygame.draw.line(Win, (255, 255, 255), (0, WIDTH * (j / 3)), (WIDTH, WIDTH*(j / 3)), 1)

def draw_pieces(Win, board):
    for x in range(len(board)):
        for y in range(len(board)):
            if board[y][x] == -1:
                Win.blit(Circle, (x*(WIDTH // 3), y*(WIDTH // 3)))
            elif board[y][x] == 1:
                Win.blit(Cross, (x*(WIDTH // 3), y*(WIDTH // 3)))


def redraw_window(Win, board, player, game_over, AI_wins, Player_wins):
    Win.fill(Bg)
    draw_board(Win)
    draw_pieces(Win, board)
    pygame.display.update()

game_board = create_board()

def main():
    global game_board
    AI_wins = False
    Player_wins = False
    No_one = False
    turn = random.choice([-1, 1])
    run = True
    green = (0,255,0,0)
    game_over = False

    while run:
        Clock.tick(FPS)
        redraw_window(Win, game_board, turn, game_over, AI_wins, Player_wins)
        fill(Circle, green)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    Player_wins = True
                    game_over = True
                    message_display("You won")
                    quit()

                if event.key == pygame.K_SPACE and game_over:
                    reset_board(game_board)
                    turn = random.choice([-1, 1])
                    game_over = False
                    if AI_wins:
                        AI_wins = False
                    if Player_wins:
                        Player_wins = False
                    if No_one:
                        No_one = False

            if event.type == pygame.MOUSEBUTTONDOWN and turn == Human and not game_over:
                if pygame.mouse.get_pressed()[0] and turn == Human and not game_over:
                    pos = pygame.mouse.get_pos()
                    if turn == Human and not game_over:
                        if set_locations(game_board, pos[0] // (WIDTH // 3), pos[1] // (WIDTH // 3), turn):
                            if check_game(game_board, Human):
                                Player_wins = True
                                game_over = True
                            turn = AI

        if turn == AI and not game_over:
            alpha = -infinity
            beta = +infinity

            ai_turn(game_board, alpha, beta)
            if check_game(game_board, AI):
                AI_wins = True
                game_over = True

            turn = Human

main()
