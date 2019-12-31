import numpy as np
import Env as e
import copy


def random_agent(snake0):
	while True:
		snake = copy.deepcopy(snake0)
		next_step = np.random.choice(e.dirs)
		snake.go_next(next_step)
		if snake.check():
			continue
		else:
			print(next_step)
			break
	return next_step
