import Env as e
# from Random import random
import math


def minimax(self, other):
	minimax_func(self, other,curDepth=4,)


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
def minimax_func(self, root, curDepth, is_max):
	# base case : targetDepth reached
	if curDepth == e.minimax_depth or root.score > e.score:
		return root.f_cost, root

	if is_max:
		child = self.get_child()
		val = -math.inf
		node = None

		for i in child:
			val, node = max(val, minimax_func(root=i, curDepth=curDepth - 1, is_max=False))
		return val, node.parent

	else:
		child = root.get_child()
		val = +math.inf
		node = None

		for i in child:
			val, node = max(val, minimax_func(root=i, curDepth=curDepth - 1, is_max=True))
		return val, node.parent

# Driver code
# scores = [3, 5, 2, 9, 12, 5, 23, 23]

# treeDepth = math.log(len(scores), 2)

# print("The optimal value is : ", end="")
# print(minimax(0, 0, True, scores, treeDepth))

# This code is contributed
# by rootshadow
