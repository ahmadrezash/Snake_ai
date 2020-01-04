import socket
import time, datetime
import Env as e
from snake_agent import *
import json
# import Snake
import atexit
import copy

# ============
import pygame, random, numpy as np
from snake_agent import agent
from Snake import World
from pygame.locals import *

# ===========init game ============
global screen


def init_game():
	global screen, font, clock
	pygame.init()
	screen = pygame.display.set_mode((e.dim, e.dim))
	pygame.display.set_caption('Snake With AI =)')
	font = pygame.font.Font('freesansbold.ttf', 18)

	clock = pygame.time.Clock()


# ===========
def server_program():
	global screen, font, clock

	# CHOOSE FROM: ['A*' , 'IDS', 'MINIMAX']
	food_board = np.random.randint(4, size=(int(e.dim / e.scale), int(e.dim / e.scale)))
	world = World(board=food_board, count=4)
	world.refresh_screen(screen, font)

	while True:
		clock.tick(2)

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				exit()

		if world.next_step():
			print('check issue...')
			break

		world.refresh_screen(screen, font)
		if world.score_check():
			print('score complete...')
			break

	# =====

	while True:

		game_over_font = pygame.font.Font('freesansbold.ttf', 75)
		game_over_screen = game_over_font.render('move: {}'.format(world.snakes[0].movement), True, (255, 255, 255))
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
