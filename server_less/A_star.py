import Env as e


# def heuristic(snake):
# 	return 1 / (snake.g_path_cost + 1)

from queue import PriorityQueue

def a_star_search(start):
	frontier = PriorityQueue()
	# frontier.put((0, start))
	frontier.put(start)
	# came_from = {}
	came_from = []
	cost_so_far = {}
	# came_from[start] = None
	cost_so_far[start] = 0

	while not frontier.empty():
		# current = frontier.get()[1]
		current = frontier.get()
		# current = current[
		if current.score >= e.score:
			came_from.append(current)
			break
		child = current.get_child()
		for next in child:
			new_cost = current.g_path_cost  # + graph.cost(current, next)
			if next not in cost_so_far or new_cost < next.g_path_cost:
				# cost_so_far[next] = new_cost
				# priority = int(new_cost + heuristic(next))
				# frontier.put((next.f_cost, next))
				frontier.put(next)
				# print(f'score is :{next.score} in depth {next.movement}')

		# came_from[next] = current
		if not current == start:
			came_from.append(current)

	if not len(came_from):
		pass
	# return came_from, cost_so_far
	return came_from[0].last_action
