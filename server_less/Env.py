class ActionItem:
	GIVE_ME_DATA = '1'
	Next = '2'


class ResponceStat:
	Board_data = '12'
	dict = {
			Board_data: 'board data'
	}


dim = 700
dim_score_board = 400
scale = 20


class setting:
	HOST = '127.0.0.1'
	PORT = 57368


UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
dirs = [UP, DOWN, RIGHT, LEFT]

score = 10

IDS_depth = score // 3
# IDS_depth = score//5

minimax_depth = score // 3

start_pos = 50