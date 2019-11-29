import pygame, random, numpy as np
  
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
dirs = [UP, DOWN, RIGHT, LEFT]


class state:
	def __init__(self, board, snake, snake_energy, score):
		self.board = board
		self.score = score
		self.snake_energy = snake_energy
		self.snake = snake

	snake = []
	snake_energy = 0
	board = None
	score = None


def is_valid_state(snake):
	game_over = False
	if snake[0][0] == 600 or snake[0][1] == 600 or snake[0][0] < 0 or snake[0][1] < 0:
		game_over = True

	# Check if the snake has hit itself
	for i in range(1, len(snake)):
		if snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:
			game_over = True
	# if game_over()
	return game_over


def after_next_step(snake, snake_energy, my_direction):
	if snake_energy:
		snake_energy -= 1
		snake.append((0, 0))
	else:
		if not len(snake) == 1:
			snake.pop(len(snake) - 1)

	for i in range(len(snake) - 1, 0, -1):
		snake[i] = (snake[i - 1][0], snake[i - 1][1])

	if my_direction == UP:
		snake[0] = (snake[0][0], snake[0][1] - 10)
	if my_direction == DOWN:
		snake[0] = (snake[0][0], snake[0][1] + 10)
	if my_direction == RIGHT:
		snake[0] = (snake[0][0] + 10, snake[0][1])
	if my_direction == LEFT:
		snake[0] = (snake[0][0] - 10, snake[0][1])

	return snake, snake_energy


def random_agent(board, snake, snake_energy):
	next_step = np.random.choice(dirs)
	while is_valid_state(after_next_step(snake.copy(), snake_energy, next_step)[0].copy()):
		print(next_step)
		next_step = np.random.choice(dirs)
	return next_step


def BFS_agent(state):
	frontier = list()
	node = (state, 0)
	if node[0].score >= 500:
		pass
	frontier.push(state)
	pass


def agent(board, snake, snake_energy, score):
	node = state(board=board,
	             snake=snake,
	             snake_energy=snake_energy,
	             score=score)
	return random_agent(board, snake, snake_energy)
