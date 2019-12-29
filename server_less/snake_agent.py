import pygame, random, numpy as np
from Env import *
from Snake import Snake, State
import copy


def random_agent(snake0):
	while True:
		snake = copy.deepcopy(snake0)
		next_step = np.random.choice(dirs)
		snake.go_next(next_step)
		if snake.check():
			continue
		else:
			print(next_step)
			break
	return next_step


def BFS_agent(state):
	frontier = list()
	node = (state, 0)
	if node[0].score >= 500:
		pass
	frontier.push(state)
	pass


import IDS
import A_star

# def IDS_agent(snake0):
# 	return IDS.IDDFS(snake0)
def agent(snake0):
	return random_agent(snake0)
	# return IDS.IDDFS(snake0)
	# return A_star.a_star_search(snake0)

# def agent(board, snake, snake_energy, score):
# 	snake = Snake(snake=snake,
# 	              snake_energy=snake_energy,
# 	              score=score
# 	              )
# 	node = State(board=board,
# 	             snake=snake,
# 	             snake_energy=snake_energy,
# 	             score=score)
# 	return random_agent(board, snake, snake_energy)
