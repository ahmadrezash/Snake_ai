import socket
import time, datetime
from Env import *
from snake_agent import *
import json
import atexit

# ============
import pygame, random, numpy as np
from snake_agent import agent
from pygame.locals import *

# ===========init game ============
global score_font, score_rect, screen
global energy_font, energy_rect
global UP, RIGHT, DOWN, LEFT, screen, food_board
global snake, snake_skin, snake_energy, my_direction
global clock, font, score, movement, game_over
global host, port


# dim = 200
# scale = 20


def on_grid_random():
	x = random.randint(3, 8)
	y = random.randint(3, 8)

	return (x * scale, y * scale)


def add_to_snake_tail():
	snake.append((0, 0))


def collision(c1, c2):
	return (c1[0] == c2[0]) and (c1[1] == c2[1])


def init_server():
	global host, port

	host = setting.HOST
	port = setting.PORT  # initiate port no above 1024


def refresh_screen():
	global snake, snake_skin, snake_energy, my_direction
	global clock, font, score, movement, game_over

	score_font = font.render('Score: %s' % (score), True, (255, 255, 255))
	score_rect = score_font.get_rect()
	score_rect.topleft = (dim - 120, 10)
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


def init_game():
	global score_font, score_rect, screen
	global energy_font, energy_rect
	global UP, RIGHT, DOWN, LEFT, screen, food_board
	global snake, snake_skin, snake_energy, my_direction
	global clock, font, score, movement, game_over
	# Macro definition for snake movement.

	UP = 0
	RIGHT = 1
	DOWN = 2
	LEFT = 3
	pygame.init()
	screen = pygame.display.set_mode((dim, dim))
	pygame.display.set_caption('Snake With AI =)')

	# Board
	food_board = np.random.randint(9, size=(int(dim / scale), int(dim / scale)))

	snake = [on_grid_random()]

	# snake_skin = pygame.Surface((10, 10))
	snake_skin = pygame.Surface((scale, scale))
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
	global snake, snake_skin, snake_energy, my_direction
	global clock, font, score, movement, game_over
	global host, port

	# get the hostname
	refresh_screen()
	server_socket = socket.socket()  # get instance

	server_socket.bind((host, port))  # bind host address and port together

	server_socket.listen(2)
	conn, address = server_socket.accept()  # accept new connection
	print("Connection from: " + str(address))
	while True:
		try:
			data = conn.recv(1024).decode()
		except:
			data = None
		if not data:
			continue
		# ======
		# clock.tick(7)
		print(data)
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				exit()
		if snake_energy == 0 and len(snake) == 1:
			snake_energy = food_board[snake[0][0] // scale - 1][snake[0][1] // scale - 1]
			score = score + snake_energy * 5 + 3

		data = json.loads(data)

		if data['action'] == ActionItem.Next:
			my_direction = data['next']
		else:
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
		if snake[0][0] == dim or snake[0][1] == dim or snake[0][0] < 0 or snake[0][1] < 0:
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
			snake[0] = (snake[0][0], snake[0][1] - scale)
		if my_direction == DOWN:
			snake[0] = (snake[0][0], snake[0][1] + scale)
		if my_direction == RIGHT:
			snake[0] = (snake[0][0] + scale, snake[0][1])
		if my_direction == LEFT:
			snake[0] = (snake[0][0] - scale, snake[0][1])

		screen.fill((0, 0, 0))

		for x in range(0, dim, scale):  # Draw vertical lines
			pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, dim))
		for y in range(0, dim, scale):  # Draw vertical lines
			pygame.draw.line(screen, (40, 40, 40), (0, y), (dim, y))

		# =====

		# data=str(datetime.datetime.now())
		refresh_screen()
		time.sleep(.5)
		data = 'Next\n'
		data = {
				'action': ActionItem.Next,
				'board': food_board.tolist(),
				'snake': snake,
				'snake_energy': int(snake_energy),
				'score': int(score)
		}
		data = json.dumps(data)
		conn.sendall(bytes(json.dumps(data), 'utf-8'))
	while True:
		conn.close()
		print('connection closed...')

		game_over_font = pygame.font.Font('freesansbold.ttf', 75)
		# game_over_screen = game_over_font.render('Game Over', True, (255, 255, 255))
		game_over_screen = game_over_font.render('move: {}'.format(movement), True, (255, 255, 255))
		game_over_rect = game_over_screen.get_rect()
		game_over_rect.midtop = (dim / 2, 60)
		screen.blit(game_over_screen, game_over_rect)
		pygame.display.update()
		pygame.time.wait(1000)
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					exit()

	# conn.send(data.encode())  # send data to the client
	print('connection closed...')

	@atexit.register
	def f():
		conn.close()

	conn.close()  # close the connection


if __name__ == '__main__':
	init_server()
	init_game()
	# host = socket.gethostname()
	# port = setting.PORT  # initiate port no above 1024

	while True:
		init_game()
		init_server()
		server_program()
		print('User is Offline')
