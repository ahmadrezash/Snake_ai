import Env as e
import copy, random, pygame
import IDS
import A_star
import minimax


class State:
	pass


snake_skin = pygame.Surface((e.scale, e.scale))
snake_head = pygame.Surface((e.scale, e.scale))


# 	snake = None
# 	board = None
#
#
#
# 	def __init__(self, snake, board):
# 		self.board = board
# 		self.snake = snake


class Snake:
	snake = []
	snake_energy = 0
	movement = 0
	score = None
	board = []
	parent = None
	last_action = None
	method_name = ''
	world = None

	def method(self):
		pass

	def __init__(self, snake, snake_energy, score, board, method, world):
		self.snake = snake
		self.snake_energy = snake_energy
		self.score = score
		self.board = board

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
		if snake[0][0] >= e.dim or snake[0][1] >= e.dim or snake[0][0] <= 0 or snake[0][1] <= 0:
			game_over = True
		# print('hit boundaries')
		return game_over

	def self_conflict(self):
		game_over = False
		snake = self.snake
		for i in range(1, len(snake)):
			if snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:
				game_over = True
		# print('hit itself')
		return game_over

	def check(self):
		return self.edge_conflict() or self.self_conflict()

	def go_next(self, my_direction):
		self.movement = self.movement + 1
		if self.snake_energy == 0 and len(self.snake) == 1:
			self.snake_energy = self.board[self.snake[0][0] // e.scale - 1][self.snake[0][1] // e.scale - 1]
			self.score = self.score + self.snake_energy * 5 + 3

		if self.snake_energy:
			self.snake_energy -= 1
			self.snake.append((0, 0))
		else:
			if not len(self.snake) == 1:
				self.snake.pop(len(self.snake) - 1)

		for i in range(len(self.snake) - 1, 0, -1):
			self.snake[i] = (self.snake[i - 1][0], self.snake[i - 1][1])

		if my_direction == e.UP:
			self.snake[0] = (self.snake[0][0], self.snake[0][1] - e.scale)
		if my_direction == e.DOWN:
			self.snake[0] = (self.snake[0][0], self.snake[0][1] + e.scale)
		if my_direction == e.RIGHT:
			self.snake[0] = (self.snake[0][0] + e.scale, self.snake[0][1])
		if my_direction == e.LEFT:
			self.snake[0] = (self.snake[0][0] - e.scale, self.snake[0][1])

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
	x = random.randint(3, e.dim//e.scale)
	y = random.randint(3, e.dim//e.scale)

	return (x * e.scale, y * e.scale)


class World:
	snakes = []
	board = None
	# Nobat Current
	current_snake = None

	def __init__(self, count, board):
		self.board = board
		for i in range(count):
			self.snakes.append(Snake(snake=[on_grid_random()], snake_energy=0, score=0, board=self.board, method='IDS', world=self))

		self.current_snake = self.snakes[0]

	def next_step(self):
		snake = copy.deepcopy(self.current_snake)
		# Snake Thinking
		dir = snake.method(snake)
		self.current_snake.go_next(dir)
		index = (self.snakes.index(self.current_snake) + 1) % len(self.snakes)
		self.current_snake = self.snakes[index]

		if snake.check():
			return False

	def score_check(self):
		for i in self.snakes:
			if i.score >= e.score:
				return True
		return False

	def refresh_screen(self, screen, font):
		screen.fill((0, 0, 0))

		# Line
		for x in range(0, e.dim, e.scale):  # Draw vertical lines
			pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, e.dim))
		for y in range(0, e.dim, e.scale):  # Draw vertical lines
			pygame.draw.line(screen, (40, 40, 40), (0, y), (e.dim, y))

		# Food Board
		board = self.board.tolist()
		for i in range(len(board)):
			for j in range(len(board[0])):
				food_font = font.render(f'{(board[i][j])}', True, (100, 100, 100))
				food_rect = food_font.get_rect()
				food_rect.topleft = (i * e.scale, j * e.scale)
				screen.blit(food_font, food_rect)

		dis = 0
		for i in self.snakes:
			score_font = font.render('Score: %s' % (i.score), True, (255, 255, 255))
			score_rect = score_font.get_rect()
			score_rect.topleft = (e.dim - 120, 10 + dis)
			screen.blit(score_font, score_rect)

			energy_font = font.render('Energy: %s' % (i.snake_energy), True, (255, 255, 255))
			energy_rect = score_font.get_rect()
			energy_rect.topleft = (80, 10 + dis)
			screen.blit(energy_font, energy_rect)

			move_font = font.render('move: %s' % (i.movement), True, (255, 255, 255))
			move_rect = score_font.get_rect()
			move_rect.topleft = (250, 10 + dis)
			screen.blit(move_font, move_rect)
			dis = dis + 50

		for s in self.snakes:
			flag = True
			snake_head.fill(s.snake_head)  # Gray
			snake_skin.fill(s.snake_skin)  # White
			for pos in s.snake:
				if flag:
					screen.blit(snake_head, pos)
					flag = False
				else:
					screen.blit(snake_skin, pos)

		# -----------------------------------------------------------

		pygame.display.update()
