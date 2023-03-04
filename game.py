### GAME LOGIC ###

# Grid is defined as bits, e.g. 0000 0011 0010 0001 = 0 8 4 2
# i.e. 2 to the power of bits

import random, collections
from multiprocessing.pool import ThreadPool

ROW_MASK = 0xFFFF
COL_MASK = 0x000F_000F_000F_000F

SCORE_MONOTONICITY_POWER = 4
SCORE_MONOTONICITY_WEIGHT = 47
SCORE_SUM_POWER = 3.5
SCORE_SUM_WEIGHT = 11
SCORE_MERGES_WEIGHT = 700
SCORE_EMPTY_WEIGHT = 270
SCORE_LOST_PENALTY = 200000

### HELPER FUNCTIONS ###
def transpose(x):
    ''' transpose the whole grid '''
    a1 = x & 0xF0F00F0FF0F00F0F
    a2 = x & 0x0000F0F00000F0F0
    a3 = x & 0x0F0F00000F0F0000
    a = a1 | (a2 << 12) | (a3 >> 12)
    b1 = a & 0xFF00FF0000FF00FF
    b2 = a & 0x00FF00FF00000000
    b3 = a & 0x00000000FF00FF00
    return b1 | (b2 >> 24) | (b3 << 24)

def reverse_row(row):
    ''' reverse a row in grid '''
    return (row >> 12) | ((row >> 4) & 0x00F0) | ((row << 4) & 0x0F00) | (row << 12) & 0xffff

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
    ''' count distinct tiles in grid '''
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


### LOOP TO CREATE BITBOARD ###
l_combine_d = [0]* 65536
r_combine_d = [0]* 65536
empty_d = [0]* 65536
score_d = [0]* 65536
game_score_d = [0]* 65536

for x in range(65536):
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
    ### int comparison is much faster than float: https://hg.python.org/cpython/file/ea33b61cac74/Objects/floatobject.c#l285
    score_d[x] = int((SCORE_LOST_PENALTY + \
        empty * SCORE_EMPTY_WEIGHT + \
        merges * SCORE_MERGES_WEIGHT - \
        SCORE_MONOTONICITY_WEIGHT * min(mono_left, mono_right) - \
        sum * SCORE_SUM_WEIGHT) * 100)
    
print('Tables generated!')

### GAME FUNCTIONS ###
def count_empty(grid):
    ''' count empty tiles in grid '''
    res = empty_d[grid & 0xffff]
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
    newgrid = l_combine_d[grid & 0xffff]
    newgrid |= l_combine_d[(grid >> 16) & 0xffff] << 16
    newgrid |= l_combine_d[(grid >> 32) & 0xffff] << 32
    newgrid |= l_combine_d[(grid >> 48) & 0xffff] << 48
    return newgrid


def right(grid):
    ''' move grid right '''
    newgrid = r_combine_d[grid & 0xffff]
    newgrid |= r_combine_d[(grid >> 16) & 0xffff] << 16
    newgrid |= r_combine_d[(grid >> 32) & 0xffff] << 32
    newgrid |= r_combine_d[(grid >> 48) & 0xffff] << 48
    return newgrid


def up(grid):
    ''' move grid up '''
    grid = transpose(grid)
    newgrid = l_combine_d[grid & 0xffff]
    newgrid |= l_combine_d[(grid >> 16) & 0xffff] << 16
    newgrid |= l_combine_d[(grid >> 32) & 0xffff] << 32
    newgrid |= l_combine_d[(grid >> 48) & 0xffff] << 48
    return transpose(newgrid)


def down(grid):
    ''' move grid down '''
    grid = transpose(grid)
    newgrid = r_combine_d[grid & 0xffff]
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
    ''' check if game is lost '''
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


### AI PORTION ###

### AI CONSTANTS ###
CPROB_THRESH_BASE = 0.0001
CUR_DEPTH_MIN = 3
CUR_DEPTH_MAX = 15
CACHE_DEPTH_LIMIT  = 15
DEPTH_MIN = 3
DEPTH_MAX = 6
DEPTH_DISCOUNT = 2
DEPTH_ARR = [DEPTH_MIN, DEPTH_MIN, DEPTH_MIN, DEPTH_MIN, DEPTH_MIN, DEPTH_MIN, DEPTH_MIN, DEPTH_MIN, DEPTH_MIN, DEPTH_MIN, DEPTH_MIN, DEPTH_MIN, \
                DEPTH_MIN+1, DEPTH_MIN+1, \
                DEPTH_MIN+1, DEPTH_MIN+2, \
                DEPTH_MIN+2, \
                DEPTH_MIN+2][::-1]

MULTITHREAD = True

trans_table = collections.defaultdict()
move_ls = [left, right, up, down]

### AI FUNCTIONS ###
def score_grid(grid):
    ''' Score the grid '''
    score = score_d[grid & 0xffff] \
        + score_d[(grid >> 16) & 0xffff] \
        + score_d[(grid >> 32) & 0xffff] \
        + score_d[(grid >> 48) & 0xffff] 
    grid = transpose(grid)
    score += score_d[grid & 0xffff] \
        + score_d[(grid >> 16) & 0xffff] \
        + score_d[(grid >> 32) & 0xffff] \
        + score_d[(grid >> 48) & 0xffff]
    
    return score

def score_tilechoose_node(trans_table, curdepth, depth_limit, grid, cprob):
    ''' Score the tile choose node '''
    if cprob < CPROB_THRESH_BASE or curdepth >= depth_limit:
        if grid in trans_table:
            if trans_table[grid][0] >= curdepth: # 0 is depth
                return trans_table[grid][1] # 1 is heuristic score
        return score_grid(grid)
    
    if grid in trans_table:
        if trans_table[grid][0] >= curdepth: # 0 is depth
            return trans_table[grid][1] # 1 is heuristic score
    
    empty_count = count_empty(grid)
    cprob /= empty_count

    tmp = grid
    res= 0
    tile = 1
    while tile & 0xffff_ffff_ffff_ffff:
        if (tmp & 0xf) == 0:
            res += score_move_node(trans_table, curdepth, depth_limit, grid | tile, cprob * 0.9) * 0.9
            res += score_move_node(trans_table, curdepth, depth_limit, grid | (tile << 1), cprob * 0.1) * 0.1
        
        tmp >>= 4
        tile <<= 4
    
    res /= empty_count
    trans_table[grid] = (curdepth, res)
    return res

def score_move_node(trans_table, curdepth, depth_limit, grid, cprob):
    ''' Score the move node '''
    curdepth += 1
    lg = left(grid)
    rg = right(grid)
    ug = up(grid)
    dg = down(grid)
    best = 0

    if grid != lg:
        ev = score_tilechoose_node(trans_table, curdepth, depth_limit, lg, cprob)
        if ev > best:
            best = ev
    if grid != rg:
        ev = score_tilechoose_node(trans_table, curdepth, depth_limit, rg, cprob)
        if ev > best:
            best = ev
    if grid != ug:
        ev = score_tilechoose_node(trans_table, curdepth, depth_limit, ug, cprob)
        if ev > best:
            best = ev
    if grid != dg:
        ev = score_tilechoose_node(trans_table, curdepth, depth_limit, dg, cprob)
        if ev > best:
            best = ev
    
    curdepth -= 1
    return best

def score_toplevel_move(grid, move, trans_table, depth_limit):
    ''' Score the top level move '''
    if move == 0:
        lg = left(grid)
        if grid == lg:
            return 0
        return score_tilechoose_node(trans_table, 0, depth_limit, lg, 1)
    elif move == 1:
        rg = right(grid)
        if grid == rg:
            return 0
        return score_tilechoose_node(trans_table, 0, depth_limit, rg, 1)
    elif move == 2:
        ug = up(grid)
        if grid == ug:
            return 0
        return score_tilechoose_node(trans_table, 0, depth_limit, ug, 1)
    elif move == 3:
        dg = down(grid)
        if grid == dg:
            return 0
        return score_tilechoose_node(trans_table, 0, depth_limit, dg, 1)
    return 0

def find_best_move(grid):
    ''' Find the best move '''
    empty_count = count_empty(grid)
    depth_limit = DEPTH_ARR[empty_count]
    if MULTITHREAD:
        pool = ThreadPool(4)
        scores = pool.starmap(score_toplevel_move, [(grid, move, trans_table, depth_limit) for move in range(4)])
    else:
        ls = zip(*((grid, move, trans_table, depth_limit) for move in range(4)))
        scores = map(score_toplevel_move, *ls)
    bestmove, bestscore = max(enumerate(scores), key=lambda x:x[1])
    if bestscore == 0:
        return -1
    return bestmove

