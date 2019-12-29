import pygame, random, numpy as np
from Env import *

# dim=600
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
dirs = [UP, DOWN, RIGHT, LEFT]


class state:
    snake = None
    board = None
    
    def __init__(self, snake,board):
		self.board = board
		self.snake = snake


class Snake:
	snake = []
	snake_energy = 0
	score = None
	board = []

	def __init__(self, snake, snake_energy, score):
		self.snake = snake
		self.snake_energy = snake_energy
		self.score = score
		# self.board = board

	def edge_conflict(self):
		game_over = False
		snake = self.snake
		if snake[0][0] == dim or snake[0][1] == dim or snake[0][0] < 0 or snake[0][1] < 0:
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
		return self.edge_conflict() and self.self_conflict()

	def go_next(self, snake_energy, my_direction):
		# snake = self.snake

		if self.snake_energy:
			self.snake_energy -= 1
			self.snake.append((0, 0))
		else:
			if not len(self.snake) == 1:
				self.snake.pop(len(self.snake) - 1)

		for i in range(len(self.snake) - 1, 0, -1):
			# self.snake[i] = (self.snake[i - 1][0], self.snake[i - 1][1])
			self.snake[i] = self.snake[i - 1]

		if my_direction == UP:
			self.snake[0] = (self.snake[0][0], self.snake[0][1] - scale)
		if my_direction == DOWN:
			self.snake[0] = (self.snake[0][0], self.snake[0][1] + scale)
		if my_direction == RIGHT:
			self.snake[0] = (self.snake[0][0] + scale, self.snake[0][1])
		if my_direction == LEFT:
			self.snake[0] = (self.snake[0][0] - scale, self.snake[0][1])


# return snake, snake_energy


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
	snake = Snake(snake=snake,
	              snake_energy=snake_energy,
	              score=score
	              )
	node = state(board=board,
	             snake=snake,
	             snake_energy=snake_energy,
	             score=score)
	return random_agent(board, snake, snake_energy)
