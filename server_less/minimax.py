import Env as e
# from Random import random
import math


def minimax(snake_root):
	w = minimax_func(snake_root.world, me=snake_root, curDepth=2, )
	# self = w[1]
	# index = (w[1].current_snake.id - 1) % len(self.snakes)
	# x = self.snakes[index]


	return w[1].current_snake.last_action
	# return x.last_action


# A simple Python3 program to find
# maximum score that
# maximizing player can get
import math


# treeDepth = math.log(len(e.scores), 2)
# function minimax(node, depth, maximizingPlayer) is
#     if depth = 0 or node is a terminal node then
#         return the heuristic value of node
#     if maximizingPlayer then
#         value := −∞
#         for each child of node do
#             value := max(value, minimax(child, depth − 1, FALSE))
#         return value
#     else (* minimizing player *)
#         value := +∞
#         for each child of node do
#             value := min(value, minimax(child, depth − 1, TRUE))
#         return value
def minimax_func(world_root, me, curDepth):
	# base case : targetDepth reached
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

# Driver code
# scores = [3, 5, 2, 9, 12, 5, 23, 23]

# treeDepth = math.log(len(scores), 2)

# print("The optimal value is : ", end="")
# print(minimax(0, 0, True, scores, treeDepth))

# This code is contributed
# by rootshadow
