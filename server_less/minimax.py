import Env as e
import math

import copy


def minimax(snake_root):
	snake = copy.deepcopy(snake_root)
	w = minimax_func(snake.world, me=snake, curDepth=2, )

	return w[1].current_snake.last_action


def minimax_func(world_root, me, curDepth):
	if curDepth == 0 or world_root.current_snake.score > e.score:
		return world_root.current_snake.score, world_root

	child = world_root.get_child()

	if world_root.current_snake.id == me.id:
		val = -math.inf
		obj = None

		for i in child:
			res = minimax_func(world_root=i, me=me, curDepth=curDepth - 1)
			if val < res[0]:
				val = res[0]
				obj = res[1]
		if obj.parent == me.world:
			return val, obj
		else:
			return val, obj.parent

	else:
		val = +math.inf
		obj = None

		for i in child:
			res = minimax_func(world_root=i, me=me, curDepth=curDepth - 1)
			if val > res[0]:
				val = res[0]
				obj = res[1]

		if obj.parent.parent == me.world:
			return val, obj
		else:
			return val, obj.parent
