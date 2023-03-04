import cma
import game
from timeit import default_timer as timer
from multiprocessing.pool import ThreadPool

SCORE_MONOTONICITY_POWER = 4
SCORE_MONOTONICITY_WEIGHT = 47
SCORE_SUM_POWER = 3.5
SCORE_SUM_WEIGHT = 11
SCORE_MERGES_WEIGHT = 700
SCORE_EMPTY_WEIGHT = 270
SCORE_LOST_PENALTY = 200000
# SCORE_LOST_PENALTY = 0
w = [SCORE_MONOTONICITY_WEIGHT, SCORE_SUM_WEIGHT, SCORE_MERGES_WEIGHT, SCORE_EMPTY_WEIGHT]
move_ls = [game.left, game.right, game.up, game.down]
score_ls = [game.score_hori, game.score_hori, game.score_vert, game.score_vert]

def calc_dict(weights):
    SCORE_MONOTONICITY_WEIGHT, SCORE_SUM_WEIGHT, SCORE_MERGES_WEIGHT, SCORE_EMPTY_WEIGHT = list(map(lambda a,b:a*b, w, weights))
    score_d = [0]* 65536
    for x in range(65536):
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
        ### int comparison is much faster than float: https://hg.python.org/cpython/file/ea33b61cac74/Objects/floatobject.c#l285
        score_d[x] = int((SCORE_LOST_PENALTY + \
            empty * SCORE_EMPTY_WEIGHT + \
            merges * SCORE_MERGES_WEIGHT - \
            SCORE_MONOTONICITY_WEIGHT * min(mono_left, mono_right) - \
            sum * SCORE_SUM_WEIGHT) * 100)
    return score_d

def score_model(weights):
    game.score_d = calc_dict(weights)
    grid = 0
    score = 0
    grid = game.add_random(grid)
    grid = game.add_random(grid)
    move = game.n_find_best_move(grid)
    while move != -1:
        new_grid = move_ls[move](grid)
        score += score_ls[move](grid)
        if new_grid != grid:
            grid = game.add_random(new_grid)
        move = game.n_find_best_move(grid)
    return score

# Define the fitness function to be maximized
def fitness_function(weights):
    iterations = 50
    scores = 0
    for x in range(iterations):
        # start = timer()
        scores += score_model(weights)
        # end = timer()
        # print(end - start)

    return scores/iterations


# Initialize the CMA-ES algorithm
num_features = len(w)
es = cma.CMAEvolutionStrategy(num_features*[1], 0.1)

# Evaluate the initial weights
best_score = fitness_function(num_features*[1])  # Evaluate fitness
print("Initial weights:", w)
print("Avg score:", best_score)

# Run the optimization
for i in range(50):  # Number of iterations
    solutions = es.ask()  # Generate candidate solutions
    fitness_values = []
    print(solutions)
    for i in range(8):
        res  = fitness_function(solutions[i])
        fitness_values.append(res)
    print(fitness_values[-1])
    es.tell(solutions, fitness_values)  # Update the covariance matrix

# Get the best solution and evaluate it
best_weights = es.result.xbest
best_score = fitness_function(best_weights)  # Evaluate fitness
print("Best weights:", best_weights)
print("Avg score:", best_score)

# Run the optimization
for i in range(50):  # Number of iterations
    solutions = es.ask(number=8)  # Generate candidate solutions
    fitness_values = []
    for i in range(8):
        res  = fitness_function(solutions[i])
        fitness_values.append(res)
    es.tell(solutions, fitness_values)  # Update the covariance matrix

# Get the best solution and evaluate it
best_weights = es.result.xbest
best_score = fitness_function(best_weights)  # Evaluate fitness
print("Best weights:", best_weights)
print("Avg score:", best_score)