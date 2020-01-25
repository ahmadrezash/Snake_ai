class ActionItem:
	GIVE_ME_DATA = '1'
	Next = '2'


class ResponceStat:
	Board_data = '12'
	dict = {
			Board_data: 'board data'
	}


dimantion = 9
scale = 40

dim = dimantion * scale
# dim=200
dim_score_board = 450


class setting:
	HOST = '127.0.0.1'
	PORT = 57368


UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
dirs = [UP, DOWN, RIGHT, LEFT]

score = 200

IDS_depth = score // 3
# IDS_depth = score//5
#
minimax_depth = score // 3
minimax_depth = 2
alpha_beta_depth = 4

start_pos = 50
