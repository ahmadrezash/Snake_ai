import Env as e


# depth = 2


def IDDFS(root):
	depth = e.IDS_depth
	while True:
		depth = depth + 2
		print(depth)
		found, remaining = DLS(root, depth)
		if not found == None:
			# return found
			return found.last_action
		elif not remaining:
			return None


def DLS(node, depth):
	if depth == 0:
		if node.score > e.score:
			return (node, True)
		else:
			return (None, True)
	# (Not found, but may have children)

	elif depth > 0:
		any_remaining = False
		all_child = node.get_child()
		for child in all_child:
			print(f'score is :{child.score} in depth {child.movement}')
			found, remaining = DLS(child, depth - 1)
			if not found == None:
				# if hasattr(found.parent,'parent'):
				if found.parent.parent:
					if found.movement < 4:
						pass
					return (found.parent, True)

				else:
					return (found, True)
			if remaining:
				any_remaining = True
		# (At least one node found at depth, let IDDFS deepen)
		return (None, any_remaining)
