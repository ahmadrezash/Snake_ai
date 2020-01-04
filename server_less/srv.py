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
	screen = pygame.display.set_mode((e.dim + e.dim_score_board, e.dim))
	pygame.display.set_caption('Snake With AI =)')
	font = pygame.font.Font('freesansbold.ttf', 18)

	clock = pygame.time.Clock()


# ===========
def server_program():
	global screen, font, clock

	# CHOOSE FROM: ['A*' , 'IDS', 'MINIMAX']
	food_board = np.random.randint(4, size=(int(e.dim / e.scale), int(e.dim / e.scale)))
	world = World(board=food_board, count=7)
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

		game_over_font = pygame.font.Font('freesansbold.ttf', 55)
		game_over_screen = game_over_font.render('Game is finished....', True, (255, 255, 255))
		game_over_rect = game_over_screen.get_rect()
		game_over_rect.midtop = (e.dim_score_board + e.dim // 2, e.dim // 2)
		snakes = world.snakes.sort(key=lambda x: x.movement)
		dis = 300
		# for i in snakes[:3]:
		# 	color = i.snake_skin
		#
		#
		# 	score_font = font.render('Score: %s' % (i.score), True, (color))
		# 	score_rect = score_font.get_rect()
		# 	score_rect.topleft = (20, 10 + dis)
		# 	screen.blit(score_font, score_rect)
		#
		# 	energy_font = font.render('Energy: %s' % (i.snake_energy), True, (color))
		# 	energy_rect = score_font.get_rect()
		# 	energy_rect.topleft = (160, 10 + dis)
		# 	screen.blit(energy_font, energy_rect)
		#
		# 	move_font = font.render('move: %s' % (i.movement), True, (color))
		# 	move_rect = score_font.get_rect()
		# 	move_rect.topleft = (300, 10 + dis)
		# 	screen.blit(move_font, move_rect)
		# 	dis = dis + 50

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
