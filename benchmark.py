import game
from tqdm import tqdm
import collections

move_ls = [game.left, game.right, game.up, game.down]
score_ls = [game.score_hori, game.score_hori, game.score_vert, game.score_vert]

def score_model():
    grid = 0
    score = 0
    game.trans_table=collections.defaultdict()
    grid = game.add_random(grid)
    grid = game.add_random(grid)
    move = game.n_find_best_move(grid)
    while move != -1:
        new_grid = move_ls[move](grid)
        score += score_ls[move](grid)
        if new_grid != grid:
            grid = game.add_random(new_grid)
        move = game.find_best_move(grid)
    return score


iterations = 100
scores = []
for x in tqdm(range(iterations)):
    scores.append(score_model())

print(scores)
print('Mean:')
print(sum(scores) / len(scores))
print()
print('Median:')
print(scores[len(scores) // 2])
print()
print('Max:')
print(max(scores))
print()
print('Min:')
print(min(scores))

