
from random import randint, choice
from copy import deepcopy
from typing import List, Tuple

DEBUG = False
COMP_SOLVE = True
grid = []

### HELPER FUNCTIONS ###
def get_val() -> int:
	'''get a random value for a cell'''

	if randint(0,9) > 0:
		return 2
	else:
		return 4
		
def make_grid() -> List[List[int]]:
	'''make a 4x4 grid'''

	grid = [[0 for y in range(4)] for x in range(4)]
	x = randint(0,3)
	y = randint(0,3)
		
	grid[x][y] = get_val()
	while grid[x][y] != 0:
		x = randint(0,3)
		y = randint(0,3)
	grid[x][y] = get_val()
	return grid
	
def find_empty(grid) -> List[Tuple[int, int]]:
	'''find empty cells in grid'''

	empty_list = []
	for i in range(4):
		for j in range(4):
			if grid[i][j] == 0:
				empty_list.append((i,j))
	return empty_list

def get_curr_score(grid) -> int:
	'''get current score'''

	max_score = 0
	for row in grid:
		for el in row:
			max_score = max(max_score, el)
	return max_score

def check_game_state(grid) -> Tuple[bool, int]:
	'''check if game is over and return current score'''

	ngrid = deepcopy(grid)
	grids = [left(ngrid), right(ngrid), up(ngrid), down(ngrid)]
	for g in grids:
		if g != ngrid:
			return True, get_curr_score(ngrid)
	return False, get_curr_score(ngrid)
	
def spawn(grid, empty_list) -> List[List[int]]:
	'''spawn a new cell in an empty cell'''

	x, y = choice(empty_list)
	grid = [list(x) for x in grid]
	grid[x][y] = get_val()
	return grid
	
def flatten(new_row) -> List[int]:
	'''flatten a row (after a move)'''

	for _ in range(3):
		for j in range(1,4):
			if new_row[j-1] == 0:
				new_row[j-1] = new_row[j]
				new_row[j] = 0
	return new_row

### MOVE FUNCTIONS ###
def left(grid):
	new_grid = grid.copy()
	for x in range(4):
		new_row = new_grid[x]
		new_row = flatten(new_row)
		for i in range(4):
			if i < 3 and new_row[i] == new_row[i+1]:
				new_row[i] = new_row[i] + new_row[i+1]
				new_row[i+1] = 0
				
			if i > 0 and new_row[i-1] == 0:
				new_row[i-1] = new_row[i]
				new_row[i] = 0
			new_row = flatten(new_row)
		new_grid[x] = new_row
	return new_grid
	
	
def right(grid):
	new_grid = grid.copy()
	for x in range(4):
		new_row = new_grid[x][::-1]
		new_row = flatten(new_row)
		for i in range(4):
			if i < 3 and new_row[i] == new_row[i+1]:
				new_row[i] = new_row[i] + new_row[i+1]
				new_row[i+1] = 0
				
			if i > 0 and new_row[i-1] == 0:
				new_row[i-1] = new_row[i]
				new_row[i] = 0
			new_row = flatten(new_row)
		new_grid[x] = new_row[::-1]
	return new_grid
	
def up(grid):
	new_grid = list(zip(*grid.copy()))
	new_grid = [list(x) for x in new_grid]
	for x in range(4):
		new_row = new_grid[x]
		new_row = flatten(new_row)
		for i in range(4):
			if i < 3 and new_row[i] == new_row[i+1]:
				new_row[i] = new_row[i] + new_row[i+1]
				new_row[i+1] = 0
				
			if i > 0 and new_row[i-1] == 0:
				new_row[i-1] = new_row[i]
				new_row[i] = 0
			new_row = flatten(new_row)
		new_grid[x] = new_row
	new_grid = list(zip(*new_grid))
	new_grid = new_grid = [list(x) for x in new_grid]
	return new_grid
	
	
def down(grid):
	new_grid = list(zip(*grid.copy()))
	new_grid = [list(x) for x in new_grid]
	for x in range(4):
		new_row = new_grid[x][::-1]
		new_row = flatten(new_row)
		for i in range(4):
			if i < 3 and new_row[i] == new_row[i+1]:
				new_row[i] = new_row[i] + new_row[i+1]
				new_row[i+1] = 0
				
			if i > 0 and new_row[i-1] == 0:
				new_row[i-1] = new_row[i]
				new_row[i] = 0
			new_row = flatten(new_row)
		new_grid[x] = new_row[::-1]
	new_grid = list(zip(*new_grid))
	new_grid = new_grid = [list(x) for x in new_grid]
	return new_grid
	
	
def print_grid(grid):
	for row in grid:
		print(row)

def on_press(key, move_no, grid):
	
	# key_map = {'w':'up','a':'left','s':'down', 'd':'right'}
	if key == ('w'):
		ug = up(grid)
		empty_list = find_empty(ug)
		state, score = check_game_state(ug)
		if state and grid != ug: grid = spawn(ug, empty_list); move_no += 1
		return grid, state, score, move_no
	elif key == ('s'):
		dg = down(grid)
		empty_list = find_empty(dg)
		state, score = check_game_state(dg)
		if state and grid != dg: grid = spawn(dg, empty_list); move_no += 1
		return grid, state, score, move_no
	elif key == ('a'):
		lg = left(grid)
		empty_list = find_empty(lg)
		state, score = check_game_state(lg)
		if state and grid != lg: grid = spawn(lg, empty_list); move_no += 1
		return grid, state, score, move_no
	elif key == ('d'):
		rg = right(grid)
		empty_list = find_empty(rg)
		state, score = check_game_state(rg)
		if state and grid != rg: grid = spawn(rg, empty_list); move_no += 1
		return grid, state, score, move_no
	
def format_grid(grid):
	'''format grid for html'''

	return [[' ' if x==0 else x for x in y] for y in grid]

CELL_COLOR_DICT = { 2:"#776e65", 4:"#776e65", 8:"#f9f6f2", 16:"#f9f6f2", \
                    32:"#f9f6f2", 64:"#f9f6f2", 128:"#f9f6f2", 256:"#f9f6f2", \
                    512:"#f9f6f2", 1024:"#f9f6f2", 2048:"#f9f6f2" }
		

	
# def fill_inverse(grid):
# 	empty_list = find_empty(grid)
# 	for i, (x,y) in enumerate(empty_list):
# 		grid[x][y] = -i -1
# 	return grid
	
# def unfill_inverse(grid):
# 	return [[0 if x<0 else x for x in y] for y in grid]
	
	
### Bot logic ###
def calc_move(grid, depth=4, eval = 0, isspawn=False):
	if depth==0:
		empty_list = find_empty(grid)
		return '',eval_v1(grid) 
	empty_list = find_empty(grid)
	if isspawn:
		min_eval = 0
		for i in [2,4]:
			for (x,y) in empty_list:
				new_grid = grid.copy()
				new_grid[x][y] = i
				_, eval =  calc_move(new_grid, depth, eval, False)
				if i == 2:
					min_eval += eval * (1/(len(empty_list)*0.9))
				else:
					min_eval += eval * (1/(len(empty_list)*0.1))
				
		return '',min_eval
	
	move='a'
	lg = left(grid)
	lg_empty = find_empty(lg)
	lg_eval = len(lg_empty)
	
	rg = right(grid)
	rg_empty = find_empty(rg)
	rg_eval = len(rg_empty)
	
	ug = up(grid)
	ug_empty = find_empty(ug)
	ug_eval = len(ug_empty)
	
	dg = down(grid)
	dg_empty = find_empty(dg)
	dg_eval = len(dg_empty)
	
	if lg_eval > 0:
		_, left_eval = calc_move(lg, depth-1, eval, True)
		if left_eval > eval:
			eval = left_eval
			move='a'
	if rg_eval > 0:
		_, right_eval = calc_move(rg, depth-1, eval, True)
		if right_eval > eval:
			eval = right_eval
			move='d'
	if ug_eval > 0:
		_, up_eval = calc_move(ug, depth-1, eval, True)
		if up_eval > eval:
			eval = up_eval
			move='w'
	if dg_eval > 0:
		_, down_eval = calc_move(dg, depth-1, eval, True)
		if down_eval > eval:
			eval = down_eval
			move='s'
		
	return move, eval

def mono_score(grid):
	inv_grid = list(zip(*grid))
	inv_grid = [list(x) for x in inv_grid]
	score =0 
	for row in grid:
		if all(x<y for x, y in zip(row, row[1:])) or all(x<y for x, y in zip(row[::-1], row[1::-1])):
			score += 1
	for row in inv_grid:
		if all(x<y for x, y in zip(row, row[1:])) or all(x<y for x, y in zip(row[::-1], row[1::-1])):
			score += 1
	return score
	
def large_no(grid):
	thres = get_curr_score(grid)//4
	score = 0
	for row in grid:
		if row[0] >= thres:
			score += 1
		if row[-1] >= thres:
			score += 1
	inv_grid = list(zip(*grid))
	inv_grid = [list(x) for x in inv_grid]
	for row in grid:
		if row[0] >= thres:
			score += 1
		if row[-1] >= thres:
			score += 1
	return score
	
def corner(grid):
	score = get_curr_score(grid)
	if grid[0][0] ==score:
		return 0
	return -99999999999999
def free_squares(grid):
	score = 0
	for row in grid:
		if (2 in row or 4 in row or 8 in row) and 0 in row:
			score += 1
	inv_grid = list(zip(*grid))
	inv_grid = [list(x) for x in inv_grid]
	for row in inv_grid:
		if (2 in row or 4 in row or 8 in row) and 0 in row:
			score += 1
	return score
eval_dict = {2**x:x for x in range(15)}
def mono_v2(grid):
	weights = [[10,8,7,6.8],
				[.5,.7,1,3],
				[-.5,-1.5,-1.8,-2],
				[-3.8,-3.7,-3.5,-3]]
	# weights = [[20,16,13,10.5], #8
	# [.5,.7,1,1.3], #1, 4
	# [-.5,-1.5,-1.8,-2],
	# [-3.8,-3.7,-3.5,-3]]
	res = 0
	for j in range(4):
		for i in range(4):
			res += weights[i][j] * grid[i][j]
	return res
	
def findmerge(grid):
	score =0
	for row in grid:
		for i in range(3):
			if row[i] == row[i+1]:
				score += 1
	for row in zip(*grid):
		for i in range(3):
			if row[i] == row[i+1]:
				score += 1
	return score
	
def corner_big(grid, score):
	if grid[0][0] != score or grid[0][0]!= score//2:
		return -99
	else:
		return 0
eval_dict = {2**x:x for x in range(100)}
def eval_v1(grid, weight):
	w = eval_dict[weight]
	
	empty_list = find_empty(grid)
	val = 0
	val += len(empty_list)* w
	val += mono_v2(grid)*2
	# val += corner_big(grid, weight)
	# val += corner(grid)
	# val += findmerge(grid)*w*0.1
	# val += calc_mono(grid)
	#want a nearly monotonic board but lose? put *1, *5
	# val += large_no(grid)
	# val += free_squares(grid)
	return val
	
def calc_mono(grid):
	totalscore =0
	row= grid[0]
	
	reverse = False
	for weight, row in enumerate(grid):
		upscore =0
		reverse = not reverse
		if reverse: row = row[::-1]
		for i in range(1, len(row)):
			
			if row[i] > row[i-1]:
				upscore += row[i]
				if i ==1:
					upscore += row[i-1]
			else:
				upscore -= max(row[i],row[i-1])
				if i ==1:
					upscore -= max(row[i],row[i-1])
		
		
		totalscore += upscore * (4-weight) 
	return totalscore
	
def expectimax(grid, depth=4, spawn=False):
	'''Returns the best move and the corresponding score'''
	if depth == 0:
		return 'a', eval_v1(grid, get_curr_score(grid))
	if not spawn:
		eval=-9999999
		move=choice(['a','s','d','w'])
		lg = left(grid)
		lg_empty = find_empty(lg)
		lg_eval = len(lg_empty)
			
		rg = right(grid)
		rg_empty = find_empty(rg)
		rg_eval = len(rg_empty)
		
		ug = up(grid)
		ug_empty = find_empty(ug)
		ug_eval = len(ug_empty)
		
		dg = down(grid)
		dg_empty = find_empty(dg)
		dg_eval = len(dg_empty)
		
		if lg_eval > 0 and grid != lg:
			_, left_eval = expectimax(lg, depth-1, True)
			if left_eval > eval:
				eval = left_eval
				move='d'
		if rg_eval > 0 and grid != rg:
			_, right_eval = expectimax(rg, depth-1, True)
			if right_eval > eval:
				eval = right_eval
				move='d'
		if ug_eval > 0 and grid != ug:
			_, up_eval = expectimax(ug, depth-1, True)
			if up_eval > eval:
				eval = up_eval
				move='w'
		if dg_eval > 0 and grid != dg:
			_, down_eval = expectimax(dg, depth-1, True)
			if down_eval > eval:
				eval = down_eval
				move='s'
		return move, eval
		
	else:
		empty_list = find_empty(grid)
		empty_list_len = len(empty_list)
		min_eval = 0
		for i in [2, 4]:
			for (x,y) in empty_list:
				new_grid = deepcopy(grid)
				new_grid[x][y] = i
				_, eval = expectimax(new_grid, depth-1, False)
				
				# For minimax: min_eval = min(min_eval, eval)
				if i==2:
					min_eval += eval * ((1/empty_list_len)*0.9)
				else:
					min_eval += eval * ((1/empty_list_len)*0.1)
				
		return '',min_eval




