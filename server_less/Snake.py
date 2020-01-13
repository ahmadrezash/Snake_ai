import copy
import random

import A_star
import Env as e
import IDS
import minimax
import numpy as np
import pygame

snake_skin = pygame.Surface((e.scale, e.scale))
snake_head = pygame.Surface((e.scale, e.scale))


class Snake:
	snake = []
	footprint = []
	snake_energy = 0
	movement = 0
	score = None
	# board = []
	parent = None
	last_action = None
	method_name = ''
	world = None
	id = None
	is_active = True

	def method(self):
		pass

	def __init__(self, snake, snake_energy, score, board, method, world):
		self.snake = snake
		self.snake_energy = snake_energy
		self.score = score
		# self.board = board

		self.snake_head = (120, 120, 120)  # Gray
		self.snake_skin = (255, 255, 255)  # White

		if world:
			self.world = world
		if method == 'IDS':
			self.method = IDS.IDDFS
		elif method == 'A*':
			self.method = A_star.a_star_search
		elif method == 'MINIMAX':
			self.method = minimax.minimax

	# self.method = method

	# self.parent = self

	def __lt__(self, other):
		return True if (self.f_cost > other.f_cost) else False

	def edge_conflict(self):
		game_over = False
		snake = self.snake
		if snake[0][0] >= e.dim or snake[0][1] >= e.dim or snake[0][0] < 0 or snake[0][1] < 0:
			game_over = True
			print('hit boundaries')
		return game_over

	def self_conflict(self):
		game_over = False
		snake = self.snake
		for i in range(1, len(snake)):
			if snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:
				game_over = True
				print('hit itself')
		return game_over

	def check(self):
		return self.edge_conflict() or self.self_conflict()

	def go_next(self, my_direction):
		self.movement = self.movement + 1
		# self.footprint.append(self.snake[0])

		if self.snake_energy == 0 and len(self.snake) == 1:
			x = self.snake[0][0] // e.scale - 1
			y = self.snake[0][1] // e.scale - 1
			self.snake_energy = self.world.get_food_energy(x, y)
			self.score = self.score + self.snake_energy * 5 + 3

		if self.snake_energy:
			self.snake_energy -= 1
			self.snake.append((0, 0))
		else:
			if not len(self.snake) == 1:
				old = self.snake.pop(len(self.snake) - 1)

		for i in range(len(self.snake) - 1, 0, -1):
			self.snake[i] = (self.snake[i - 1][0], self.snake[i - 1][1])

		if my_direction == e.UP:
			self.snake[0] = (self.snake[0][0], self.snake[0][1] - e.scale)
			self.last_action = e.UP
		if my_direction == e.DOWN:
			self.snake[0] = (self.snake[0][0], self.snake[0][1] + e.scale)
			self.last_action = e.DOWN
		if my_direction == e.RIGHT:
			self.snake[0] = (self.snake[0][0] + e.scale, self.snake[0][1])
			self.last_action = e.RIGHT
		if my_direction == e.LEFT:
			self.snake[0] = (self.snake[0][0] - e.scale, self.snake[0][1])
			self.last_action = e.LEFT

	def get_child(self):
		child = []
		for i in e.dirs:
			snake = copy.deepcopy(self)
			snake.go_next(i)
			if not snake.check():
				snake.last_action = i
				snake.parent = self
				child.append(snake)
			else:
				continue

		return child

	@property
	def g_path_cost(self):
		return self.score

	@property
	def heuristic(self):
		return self.snake_energy

	@property
	def f_cost(self):
		return self.g_path_cost + self.heuristic


def on_grid_random():
	x = random.randint(3, e.dim // e.scale)
	y = random.randint(3, e.dim // e.scale)

	return (x * e.scale, y * e.scale)


def arrow(x=0, y=0):
	# return (173, 79, 79), ((0 + x, 10 + y), (0 + x, 20 + y), (10 + x, 20 + y), (10 + x, 25 + y), (20 + x, 15 + y), (10 + x, 5 + y), (10 + x, 10 + y))
	return (250, 250, 250), ((0 + x, 10 + y), (0 + x, 20 + y), (10 + x, 20 + y), (10 + x, 25 + y), (20 + x, 15 + y), (10 + x, 5 + y), (10 + x, 10 + y))


class World:
	color = [
			((93, 2, 9), (213, 106, 114)),  # 1
			((69, 91, 2), (183, 208, 104)),  # 2
			((6, 33, 62), (77, 108, 143)),  # 3
			((43, 5, 64), (121, 77, 146)),  # 4
			((58, 4, 0), (241, 157, 150)),  # 5
			((58, 26, 0), (241, 191, 150)),  # 6
			((20, 61, 50), (46, 127, 105)),  # 7
	]
	snakes = []
	board = None
	# Nobat Current
	current_snake = None
	parent = None
	last_action = 1000

	def __init__(self, count=2, board=[]):
		if board:
			self.board = board
		else:
			self.board = np.random.randint(9, size=(int(e.dim / e.scale), int(e.dim / e.scale)))

		id_counter = 0
		for i in range(count):
			# CHOOSE FROM: ['A*' , 'IDS', 'MINIMAX']
			new = Snake(snake=[on_grid_random()], snake_energy=0, score=0, board=self.board, method='MINIMAX', world=self)
			new.id = id_counter
			new.last_action = i
			self.snakes.append(new)
			id_counter = id_counter + 1
			index_color = np.random.randint(len(self.color))
			new.snake_head = self.color[index_color][0]
			new.snake_skin = self.color[index_color][1]
			self.color.pop(index_color)

		self.current_snake = self.snakes[0]

	def get_food_energy(self, x, y):
		val = self.board[x][y]
		return val

	def next_step(self):
		if not self.current_snake.is_active:
			x = list(filter(lambda x: x.id == self.current_snake.id, self.snakes))[0]
			index = (self.snakes.index(x) + 1) % len(self.snakes)
			self.current_snake = self.snakes[index]

			return False
		### For Automatic handling
		snake = copy.deepcopy(self.current_snake)

		# Snake Thinking
		dir = snake.method(snake)
		self.current_snake.go_next(dir)
		if snake.check():
			return True
		x = list(filter(lambda x: x.id == self.current_snake.id, self.snakes))[0]
		index = (self.snakes.index(x) + 1) % len(self.snakes)
		self.current_snake = self.snakes[index]
		return False

	def score_check(self):
		finished = True
		for i in self.snakes:
			if i.score >= e.score:
				i.is_active = False
				finished = finished and True
			else:
				finished = finished and False

		return finished

	def refresh_screen(self, screen, font):
		# screen.fill((0, 0, 0))
		screen.fill((38, 37, 37))

		# Line
		for x in range(0, e.dim, e.scale):  # Draw vertical lines
			pygame.draw.line(screen, (60, 60, 60), (e.dim_score_board + x, 0), (e.dim_score_board + x, e.dim))
		for y in range(0, e.dim, e.scale):  # Draw vertical lines
			pygame.draw.line(screen, (60, 60, 60), (e.dim_score_board + 0, y), (e.dim_score_board + e.dim, y))

		# Food Board
		board = self.board.tolist()
		for i in range(len(board)):
			for j in range(len(board[0])):
				food_font = font.render(f'{(board[i][j])}', True, (60, 60, 60))
				food_rect = food_font.get_rect()
				food_rect.topleft = (e.dim_score_board + i * e.scale, j * e.scale)
				screen.blit(food_font, food_rect)

		dis = 50
		score_font = font.render('Turn: %s' % (self.current_snake.id), True, self.current_snake.snake_skin)
		score_rect = score_font.get_rect()
		score_rect.topleft = (50, 10)
		screen.blit(score_font, score_rect)
		for i in self.snakes:
			if i.is_active:
				color = i.snake_skin
			else:
				color = (90, 90, 90)
			# continue

			if self.current_snake.id == i.id:
				a = arrow(x=-1, y=dis + 3)
				pygame.draw.polygon(screen, a[0], a[1])

			score_font = font.render('Score: %s' % (i.score), True, (color))
			score_rect = score_font.get_rect()
			score_rect.topleft = (20, 10 + dis)
			screen.blit(score_font, score_rect)

			energy_font = font.render('Energy: %s' % (i.snake_energy), True, (color))
			energy_rect = score_font.get_rect()
			energy_rect.topleft = (160, 10 + dis)
			screen.blit(energy_font, energy_rect)

			move_font = font.render('move: %s' % (i.movement), True, (color))
			move_rect = score_font.get_rect()
			move_rect.topleft = (300, 10 + dis)
			screen.blit(move_font, move_rect)
			dis = dis + 50

		for s in self.snakes:
			snake_skin.fill((255, 255, 255))  # White
			for pos in s.footprint:
				screen.blit(snake_skin, (e.dim_score_board + pos[0], pos[1]))

			flag = True
			if s.is_active:
				snake_head.fill(s.snake_head)  # Gray
				snake_skin.fill(s.snake_skin)  # White
			else:
				snake_head.fill((90, 90, 90))  # Gray
				snake_skin.fill((110, 110, 110))  # White

			for pos in s.snake:
				if flag:
					screen.blit(snake_head, (e.dim_score_board + pos[0], pos[1]))
					flag = False
					move_font = font.render('%s' % (s.id), True, (255, 255, 255))
					move_rect = score_font.get_rect()
					move_rect.topleft = ((e.dim_score_board + pos[0], pos[1]))
					screen.blit(move_font, move_rect)
				else:
					screen.blit(snake_skin, (e.dim_score_board + pos[0], pos[1]))

		# -----------------------------------------------------------

		pygame.display.update()

	def get_child(self):
		child = []
		for i in e.dirs:
			world = copy.deepcopy(self)
			world.current_snake.go_next(i)
			res = world.current_snake.check()
			# print(f'res is {res}')
			if res:
				pass
			# print(f'res is {res}')
			if not res:
				world.parent = self
				world.last_action = i
				child.append(world)
			else:
				del world
		# print(f'{len(child)}-------')

		return child


class StocasticWorld(World):
	bord_prob = []

	def __init__(self, count=2, board=[]):
		super().__init__(count, board)
		x = int(e.dim / e.scale)
		self.bord_prob = np.random.rand(x, x)

	def get_food_energy(self, x, y):
		my_chance = np.random.random(1)[0]
		food_prob = self.bord_prob[x][y]

		if my_chance < food_prob:
			val = self.board[x][y]
		else:
			val = 0
		return val
