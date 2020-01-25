# ============
import numpy as np
import pygame
from pygame.locals import *

import Env as e
from Snake import GroupWorld

# import Snake

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

	# CHOOSE FROM: ['A*' , 'IDS', 'MINIMAX' , 'AlphaBeta' ]
	food_board = np.random.randint(9, size=(int(e.dim / e.scale), int(e.dim / e.scale)))
	# world = World(board=food_board, count=7)
	# world = World(count=7)
	# world = StocasticWorld(count=4)

	group_count = 2
	snake_count = 8
	board = None
	# b = np.random.randint(9, size=(int(e.dim / e.scale), int(e.dim / e.scale)))
	# np.savetxt('./board1.txt', b)
	# board = np.loadtxt('./board1.txt').astype('int')
	# world = GroupWorld(group_count=group_count, snake_count=snake_count, board=board)
	world = GroupWorld(group_count=group_count, snake_count=snake_count)
	h = max(int(group_count + snake_count + 1) * 50, int(e.dim))
	screen = pygame.display.set_mode((e.dim + e.dim_score_board, h))
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
