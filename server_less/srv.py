import socket
import time, datetime
import Env as e
from snake_agent import *
import json
import atexit
import copy

# ============
import pygame, random, numpy as np
from snake_agent import agent
from Snake import Snake, State
from pygame.locals import *

# ===========init game ============
global score_font, score_rect, screen
global energy_font, energy_rect
global UP, RIGHT, DOWN, LEFT, screen, food_board
global snake_skin, snake_head, snake_energy, my_direction
global clock, font, score, movement, game_over
global host, port


# dim = 200
# scale = 20


def on_grid_random():
	x = random.randint(3, 8)
	y = random.randint(3, 8)

	return (x * e.scale, y * e.scale)


# def add_to_snake_tail():
# 	snake.append((0, 0))


def collision(c1, c2):
	return (c1[0] == c2[0]) and (c1[1] == c2[1])


def refresh_screen():
	global snake, snake_skin, snake_energy, my_direction
	global clock, font, score, movement, game_over

	score_font = font.render('Score: %s' % (snake.score), True, (255, 255, 255))
	score_rect = score_font.get_rect()
	score_rect.topleft = (e.dim - 120, 10)
	screen.blit(score_font, score_rect)

	energy_font = font.render('Energy: %s' % (snake.snake_energy), True, (255, 255, 255))
	energy_rect = score_font.get_rect()
	energy_rect.topleft = (80, 10)
	screen.blit(energy_font, energy_rect)

	move_font = font.render('move: %s' % (snake.movement), True, (255, 255, 255))
	move_rect = score_font.get_rect()
	move_rect.topleft = (250, 10)
	screen.blit(move_font, move_rect)

	board = food_board.tolist()
	for i in range(len(board)):
		for j in range(len(board[0])):
			food_font = font.render(f'{(board[i][j])}', True, (100, 100, 100))
			food_rect = food_font.get_rect()
			food_rect.topleft = (i * e.scale, j * e.scale)
			screen.blit(food_font, food_rect)

	# snake_head = pygame.Surface((e.scale, e.scale))

	snake_head.fill((120, 120, 120))

	flag = True
	for pos in snake.snake:
		if flag:
			screen.blit(snake_head, pos)
			flag = False
		else:
			screen.blit(snake_skin, pos)
	# -----------------------------------------------------------

	pygame.display.update()


def init_game():
	global score_font, score_rect, screen
	global energy_font, energy_rect
	global UP, RIGHT, DOWN, LEFT, screen, food_board
	global snake, snake_skin, snake_head, snake_energy, my_direction
	global clock, font, score, movement, game_over
	# Macro definition for snake movement.

	UP = 0
	RIGHT = 1
	DOWN = 2
	LEFT = 3
	pygame.init()
	screen = pygame.display.set_mode((e.dim, e.dim))
	pygame.display.set_caption('Snake With AI =)')

	# Board
	food_board = np.random.randint(4, size=(int(e.dim / e.scale), int(e.dim / e.scale)))

	snake_skin = pygame.Surface((e.scale, e.scale))
	snake_head = pygame.Surface((e.scale, e.scale))

	snake_head.fill((120, 120, 120))  #
	snake_skin.fill((255, 255, 255))  # White
	snake_energy = 3

	my_direction = LEFT

	clock = pygame.time.Clock()

	font = pygame.font.Font('freesansbold.ttf', 18)
	score = 0
	movement = 0

	game_over = False


# ===========
def server_program():
	global score_font, score_rect, screen
	global energy_font, energy_rect
	global UP, RIGHT, DOWN, LEFT, screen, food_board
	global snake, snake_skin, snake_head, snake_energy, my_direction
	global clock, font, score, movement, game_over
	global host, port

	snake = Snake(snake=[on_grid_random()], snake_energy=0, score=0, board=food_board.tolist())
	refresh_screen()
	while True:
		clock.tick(2)

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				exit()

		dir = agent(copy.deepcopy(snake))
		snake.go_next(dir)
		if snake.check():
			break
		screen.fill((0, 0, 0))

		for x in range(0, e.dim, e.scale):  # Draw vertical lines
			pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, e.dim))
		for y in range(0, e.dim, e.scale):  # Draw vertical lines
			pygame.draw.line(screen, (40, 40, 40), (0, y), (e.dim, y))
		refresh_screen()
		if snake.score >= e.score:
			break


	# =====

	while True:

		game_over_font = pygame.font.Font('freesansbold.ttf', 75)
		game_over_screen = game_over_font.render('move: {}'.format(snake.movement), True, (255, 255, 255))
		game_over_rect = game_over_screen.get_rect()
		game_over_rect.midtop = (e.dim / 2, 60)
		screen.blit(game_over_screen, game_over_rect)
		pygame.display.update()
		pygame.time.wait(1000)
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					exit()


if __name__ == '__main__':
	init_game()
	server_program()
	print('User is Offline')
