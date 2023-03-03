### GAME LOGIC ###

# Grid is defined as bits, e.g. 0000 0011 0010 0001 = 0 8 4 2
# i.e. 2 to the power of bits

import random

ROW_MASK = 0xFFFF
COL_MASK = 0x000F_000F_000F_000F

SCORE_MONOTONICITY_POWER = 4
SCORE_MONOTONICITY_WEIGHT = 47
SCORE_SUM_POWER = 3.5
SCORE_SUM_WEIGHT = 11
SCORE_MERGES_WEIGHT = 700
SCORE_EMPTY_WEIGHT = 270
SCORE_LOST_PENALTY = 200000


DEPTH_MIN = 3
DEPTH_MAX = 6
DEPTH_DISCOUNT = 2


def transpose(x):
    a1 = x & 0xF0F00F0FF0F00F0F
    a2 = x & 0x0000F0F00000F0F0
    a3 = x & 0x0F0F00000F0F0000
    a = a1 | (a2 << 12) | (a3 >> 12)
    b1 = a & 0xFF00FF0000FF00FF
    b2 = a & 0x00FF00FF00000000
    b3 = a & 0x00000000FF00FF00
    return b1 | (b2 >> 24) | (b3 << 24)


def reverse_row(row):
    return (row >> 12) | ((row >> 4) & 0x00F0) | ((row << 4) & 0x0F00) | (row << 12) & 0xffff


def unpack_col(row):
    tmp = row
    return (tmp | (tmp << 12) | (tmp << 24) | (tmp << 36)) & COL_MASK






def flatten(bitrow):
    ''' flatten a row of bits to right '''
    # check if bits are all 0000
    x = 0
    pastrow = bitrow
    while x < 3:
        cell = bitrow & (0b1111 << x*4)
        if cell == 0:
            # get first x*4 bits
            firstbits = bitrow & ((2**(x*4))-1)
            # set first x*4 bits to 0
            newrow = bitrow & ~firstbits
            # shift bits to the right
            newrow >>= 4
            # combine with first bits
            bitrow = newrow | firstbits
        if bitrow == pastrow:
            x += 1
        pastrow = bitrow

        # print(bin(bitrow))
    return bitrow


def combine(bitrow):
    ''' combine row of bits to right '''
    bitrow = flatten(bitrow)
    game_score = 0
    # pairwise comparison
    for x in range(1, 4):
        prev = bitrow & (0b1111 << (x-1)*4)
        curr = bitrow & (0b1111 << x*4)
        if prev >> (x-1)*4 == curr >> x*4 and prev != 0:
            bitrow += 0b0001 << (x-1)*4
            # null curr bits
            bitrow &= ~(0b1111 << x*4)
            game_score += (2 ** (curr >> x*4)) *2

    return flatten(bitrow), game_score


def grid_to_arr(grid, arr):
    ''' convert grid to array '''
    for x in range(4):
        row = grid & (0b1111_1111_1111_1111 << x*16)
        for y in range(4):
            cell = (row & (0b1111 << y*4)) >> y*4
            if cell:
                cell = 2 ** (cell)
            arr[x][y] = cell
    return arr


def count_distinct_tiles(grid):
    bitset = 0
    while (grid):
        bitset |= 1<<(grid & 0xf)
        grid >>= 4
    bitset >>= 1
    count = 0
    while (bitset):
        bitset &= bitset - 1
        count+=1
    return count


l_combine_d = [0]* 65536
r_combine_d = [0]* 65536
empty_d = [0]* 65536
score_d = [0]* 65536
game_score_d = [0]* 65536
for x in range(65536):
    merges = 0
    sum = 0
    l_combine_d[x], game_score_d[x] = combine(x)
    r_combine_d[x] = reverse_row(combine(reverse_row(x))[0])
    nums = [x & 0xf, (x >> 4) & 0xf, (x >> 8) & 0xf, (x >> 12) & 0xf]

    sum = 0
    empty = 0
    merges = 0

    prev = 0
    counter = 0
    for i in range(4):
        rank = nums[i]
        sum += rank ** SCORE_SUM_POWER
        if (rank == 0):
            empty+=1
        else:
            if (prev == rank):
                counter+=1
            elif (counter > 0):
                merges += 1 + counter
                counter = 0
            
            prev = rank
        
    if (counter > 0):
        merges += 1 + counter
    

    # calculate monotonicity
    mono_left = mono_right = 0
    for y in range(1,4):
        if nums[y-1] > nums[y]:
            mono_left += nums[y-1]**SCORE_MONOTONICITY_POWER - \
                nums[y]**SCORE_MONOTONICITY_POWER
        else:
            mono_right += nums[y]**SCORE_MONOTONICITY_POWER - \
                nums[y-1]**SCORE_MONOTONICITY_POWER

    empty_d[x] = empty
    score_d[x] = int(SCORE_LOST_PENALTY + \
        empty * SCORE_EMPTY_WEIGHT + \
        merges * SCORE_MERGES_WEIGHT - \
        SCORE_MONOTONICITY_WEIGHT * min(mono_left, mono_right) - \
        sum * SCORE_SUM_WEIGHT)
print(score_d[16969])
print('Tables generated!')

def count_empty(grid):
    res = 0
    res += empty_d[grid & 0xffff]
    res += empty_d[(grid >> 16) & 0xffff]
    res += empty_d[(grid >> 32) & 0xffff]
    res += empty_d[(grid >> 48) & 0xffff]
    return res

def add_random(grid):
    ''' add random tile to grid '''
    i = random.randint(1, 10)
    if i == 1:
        tile = 2
    else:
        tile = 1
    if grid == 0:
        empty = 16
    else:
        empty = count_empty(grid)
    index = random.randint(0, empty-1)
    added = False
    i = j = 0
    while not added:
        if (grid & (0xf << j*4)) == 0:
            if i == index:
                grid |= tile << j*4
                added = True
            else:
                i += 1
        j += 1
    return grid


def left(grid):
    ''' move grid left '''
    newgrid = 0
    newgrid |= l_combine_d[grid & 0xffff]
    newgrid |= l_combine_d[(grid >> 16) & 0xffff] << 16
    newgrid |= l_combine_d[(grid >> 32) & 0xffff] << 32
    newgrid |= l_combine_d[(grid >> 48) & 0xffff] << 48
    return newgrid


def right(grid):
    ''' move grid right '''
    newgrid = 0
    newgrid |= r_combine_d[grid & 0xffff]
    newgrid |= r_combine_d[(grid >> 16) & 0xffff] << 16
    newgrid |= r_combine_d[(grid >> 32) & 0xffff] << 32
    newgrid |= r_combine_d[(grid >> 48) & 0xffff] << 48
    return newgrid


def up(grid):
    ''' move grid up '''
    grid = transpose(grid)
    newgrid = 0
    newgrid |= l_combine_d[grid & 0xffff]
    newgrid |= l_combine_d[(grid >> 16) & 0xffff] << 16
    newgrid |= l_combine_d[(grid >> 32) & 0xffff] << 32
    newgrid |= l_combine_d[(grid >> 48) & 0xffff] << 48
    return transpose(newgrid)


def down(grid):
    ''' move grid down '''
    grid = transpose(grid)
    newgrid = 0
    newgrid |= r_combine_d[grid & 0xffff]
    newgrid |= r_combine_d[(grid >> 16) & 0xffff] << 16
    newgrid |= r_combine_d[(grid >> 32) & 0xffff] << 32
    newgrid |= r_combine_d[(grid >> 48) & 0xffff] << 48
    return transpose(newgrid)


def score_hori(grid):
    ''' score horizontal moves '''
    score =  game_score_d[grid & 0xffff]
    score += game_score_d[(grid >> 16) & 0xffff]
    score += game_score_d[(grid >> 32) & 0xffff]
    score += game_score_d[(grid >> 48) & 0xffff]
    return score

def score_vert(grid):
    ''' score vertical moves '''
    grid = transpose(grid)
    score =  game_score_d[grid & 0xffff]
    score += game_score_d[(grid >> 16) & 0xffff]
    score += game_score_d[(grid >> 32) & 0xffff]
    score += game_score_d[(grid >> 48) & 0xffff]
    return score


def check_survive(grid):
    if grid == left(grid) == right(grid) == up(grid) == down(grid):
        return False
    return True


def print_grid(grid):
    ''' print grid '''
    for x in range(4):
        for y in range(4):
            cell = grid & 0xf
            if cell:
                cell = 2 ** (cell)
            grid >>= 4
            print(cell, end=' ')
        print()
    print()


def format_grid(grid):
    ''' format grid '''
    res = []
    for x in range(4):
        t = []
        for y in range(4):
            cell = grid & 0xf
            if cell:
                cell = 2 ** (cell)
            else:
                cell = ' '

            grid >>= 4
            t.append(cell)
        res.append(t)
    return res

CPROB_THRESH_BASE = 0.0001
CUR_DEPTH_MIN = 3
CUR_DEPTH_MAX = 15
CACHE_DEPTH_LIMIT  = 15
trans_table={}

import collections
class eval_state():
    def __init__(self):
        self.table = collections.defaultdict()
        self.maxdepth = 0
        self.curdepth = 0
        self.cachehits = 0
        self.moves_evaled = 0
        self.depthlimit = 0

move_ls = [left, right, up, down]

def score_grid(grid):
    ''' Score the grid '''
    return score_d[grid & 0xffff] \
        + score_d[(grid >> 16) & 0xffff] \
        + score_d[(grid >> 32) & 0xffff] \
        + score_d[(grid >> 48) & 0xffff] \
        + transpose(grid) \
        + score_d[grid & 0xffff] \
        + score_d[(grid >> 16) & 0xffff] \
        + score_d[(grid >> 32) & 0xffff] \
        + score_d[(grid >> 48) & 0xffff]

def score_tilechoose_node(state, grid, cprob):
    ''' Score the tile choose node '''
    if cprob < CPROB_THRESH_BASE or state.curdepth >= state.depth_limit:
        state.maxdepth = max(state.curdepth, state.maxdepth)
        return score_grid(grid)
    
    if state.curdepth < CACHE_DEPTH_LIMIT:
        if grid in state.table:
            if state.table[grid][0] >= state.curdepth: # 0 is depth
                state.cachehits += 1
                return state.table[grid][1] # 1 is heuristic score
    
    empty_count = count_empty(grid)
    cprob /= empty_count

    res = 0
    tmp = grid
    res= 0
    tile = 1
    while tile & 0xffff_ffff_ffff_ffff:
        if (tmp & 0xf) == 0:
            res += score_move_node(state, grid | tile, cprob * 0.9) * 0.9
            res += score_move_node(state, grid | (tile << 1), cprob * 0.1) * 0.1
        
        tmp >>= 4
        tile <<= 4
    
    res /= empty_count

    if state.curdepth < CACHE_DEPTH_LIMIT:
        entry = [state.curdepth, res]
        state.table[grid] = entry

    return res

def score_move_node(state, grid, cprob):
    best = 0
    state.curdepth += 1
    for move in range(4):
        new_grid = move_ls[move](grid)
        state.moves_evaled+=1

        if grid != new_grid:
            best = max(best, score_tilechoose_node(state, new_grid, cprob))
    state.curdepth-=1

    return best

def find_best_move(grid):
    move = 0
    best = 0
    bestmove = -1
    for move in range(4):
        res = score_toplevel_move(grid, move)

        if res > best:
            best = res
            bestmove = move
    return bestmove

def _score_toplevel_move(state, grid, move):
    # Move node
    new_grid = move_ls[move](grid)
    if new_grid == grid:
        return 0
    return score_tilechoose_node(state, new_grid, 1)

def score_toplevel_move(grid, move):
    res = 0
    state =  eval_state()
    state.depth_limit = max(DEPTH_MIN, count_distinct_tiles(grid) - DEPTH_DISCOUNT)
    state.depth_limit = min(state.depth_limit, DEPTH_MAX)
    res = _score_toplevel_move(state, grid, move)
    return res

def expectimax(grid, depth_limit=3, spawn=False, cprob=1.0, cur_depth=0):
    '''Returns the best move and the corresponding score'''
    global trans_table
    # print('calculating', depth)
    if not spawn:
        eval = 0
        lg = left(grid)
        rg = right(grid)
        ug = up(grid)
        dg = down(grid)
        move = -1
        if grid != lg:
            left_eval = expectimax(lg, depth_limit, True, cprob, cur_depth+1)[1]
            if left_eval > eval:
                eval = left_eval
                move = 0
        if grid != rg:
            right_eval = expectimax(rg, depth_limit, True, cprob, cur_depth+1)[1]
            if right_eval > eval:
                eval = right_eval
                move = 1
        if grid != ug:
            up_eval = expectimax(ug, depth_limit, True, cprob, cur_depth+1)[1]
            if up_eval > eval:
                eval = up_eval
                move = 2
        if grid != dg:
            down_eval = expectimax(dg, depth_limit, True, cprob, cur_depth+1)[1]
            if down_eval > eval:
                eval = down_eval
                move = 3
        return move, eval

    else:
        if cur_depth >= depth_limit or cprob < CPROB_THRESH_BASE:
            res = score_d[grid & 0xffff]
            res += score_d[(grid >> 16) & 0xffff]
            res += score_d[(grid >> 32) & 0xffff]
            res += score_d[(grid >> 48) & 0xffff]
            grid = transpose(grid)
            res += score_d[grid & 0xffff]
            res += score_d[(grid >> 16) & 0xffff]
            res += score_d[(grid >> 32) & 0xffff]
            res += score_d[(grid >> 48) & 0xffff]
            return -1, res
        
        if grid in trans_table:
            if trans_table[grid][0] >= cur_depth:
                return -1, trans_table[grid][1]
            
        empty_count = count_empty(grid)
        cprob /= empty_count
        tile = 1
        tmp = grid
        res= 0
        while (tile & 0xffff_ffff_ffff_ffff):
            if ((tmp & 0xf) == 0):
                res += expectimax(grid | tile, depth_limit, False, cprob*0.9, cur_depth)[1]*0.9
                res += expectimax(grid | (tile << 1), depth_limit, False, cprob*0.1, cur_depth)[1]*0.1
            
            tmp >>= 4
            tile <<= 4
        
        res /= empty_count

        # if cur_depth > CUR_DEPTH_MIN and cur_depth < CUR_DEPTH_MAX:
        if grid in trans_table:
            if cur_depth > trans_table[grid][0]:
                trans_table[grid] = (cur_depth, res)
        else:
            trans_table[grid] = (cur_depth, res)

        
        return -1, res
