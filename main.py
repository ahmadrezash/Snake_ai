##### 10 - Game over ####
import pygame, random, numpy as np
from snake_agent import agent
from pygame.locals import *

import socket
import atexit
import json
import numpy as np

# ----------- Server Config ----------
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Helper functions
def on_grid_random():
	x = random.randint(3, 56)
	y = random.randint(3, 56)

	return (x * 10, y * 10)


def collision(c1, c2):
	return (c1[0] == c2[0]) and (c1[1] == c2[1])


# Macro definition for snake movement.
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Snake With AI =)')

# Board
food_board = np.random.randint(50, size=(60, 60))

snake = [on_grid_random()]

snake_skin = pygame.Surface((10, 10))
snake_skin.fill((255, 255, 255))  # White
snake_energy = 3

my_direction = LEFT

clock = pygame.time.Clock()

font = pygame.font.Font('freesansbold.ttf', 18)
score = 0
movement = 0

game_over = False
# while not game_over:

while score <= 200:
	clock.tick(7)
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			exit()


	def add_to_snake_tail():
		snake.append((0, 0))

#===== Ta INJA
	if snake_energy == 0 and len(snake) == 1:
		snake_energy = food_board[snake[0][0] // 10][snake[0][1] // 10]
		# snake.append((0, 0))
		score = score + snake_energy * 5 + 1

	my_direction = agent(food_board.copy(), snake.copy(), snake_energy, score)

	data = {
			'food_board': food_board.tolist(),
	}
	movement += 1
	if snake_energy:
		snake_energy -= 1
		add_to_snake_tail()
	else:
		if not len(snake) == 1:
			snake.pop(len(snake) - 1)
	# Check if snake collided with boundaries
	if snake[0][0] == 600 or snake[0][1] == 600 or snake[0][0] < 0 or snake[0][1] < 0:
		game_over = True
		print('hit boundaries')
		break

	# Check if the snake has hit itself
	for i in range(1, len(snake) - 1):
		if snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:
			game_over = True
			print('hit itself')
			break

	if game_over:
		break

	for i in range(len(snake) - 1, 0, -1):
		snake[i] = (snake[i - 1][0], snake[i - 1][1])

	# Actually make the snake move.
	if my_direction == UP:
		snake[0] = (snake[0][0], snake[0][1] - 10)
	if my_direction == DOWN:
		snake[0] = (snake[0][0], snake[0][1] + 10)
	if my_direction == RIGHT:
		snake[0] = (snake[0][0] + 10, snake[0][1])
	if my_direction == LEFT:
		snake[0] = (snake[0][0] - 10, snake[0][1])

	screen.fill((0, 0, 0))

	for x in range(0, 600, 10):  # Draw vertical lines
		pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, 600))
	for y in range(0, 600, 10):  # Draw vertical lines
		pygame.draw.line(screen, (40, 40, 40), (0, y), (600, y))

	# ---------------- Refresh Score On Screen ------------------

	score_font = font.render('Score: %s' % (score), True, (255, 255, 255))
	score_rect = score_font.get_rect()
	score_rect.topleft = (600 - 120, 10)
	screen.blit(score_font, score_rect)

	energy_font = font.render('Energy: %s' % (snake_energy), True, (255, 255, 255))
	energy_rect = score_font.get_rect()
	energy_rect.topleft = (80, 10)
	screen.blit(energy_font, energy_rect)

	move_font = font.render('move: %s' % (movement), True, (255, 255, 255))
	move_rect = score_font.get_rect()
	move_rect.topleft = (250, 10)
	screen.blit(move_font, move_rect)

	for pos in snake:
		screen.blit(snake_skin, pos)
	# -----------------------------------------------------------

	pygame.display.update()

while True:
	game_over_font = pygame.font.Font('freesansbold.ttf', 75)
	# game_over_screen = game_over_font.render('Game Over', True, (255, 255, 255))
	game_over_screen = game_over_font.render('move: {}'.format(movement), True, (255, 255, 255))
	game_over_rect = game_over_screen.get_rect()
	game_over_rect.midtop = (600 / 2, 60)
	screen.blit(game_over_screen, game_over_rect)
	pygame.display.update()
	pygame.time.wait(1000)
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				exit()
