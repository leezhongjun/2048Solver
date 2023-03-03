from flask import Flask, render_template, request, redirect, url_for
from game import up, down, left, right, format_grid, add_random, check_survive, \
	score_hori, score_vert, find_best_move
import random

DEBUG = False

### Flask App ###
app = Flask(__name__)

move_ls = [left, right, up, down]
score_ls = [score_hori, score_hori, score_vert, score_vert]

@app.route('/', methods=['GET', 'POST'])
def main():
	global grid, move_no, score
	grid = 0
	grid = add_random(grid)
	grid = add_random(grid)
	move_no = 0
	score = 0
	return render_template('home.html', grid=format_grid(grid), score=score, state=True, moves=move_no)


@app.route('/gameup', methods=['GET', 'POST'])
def gameup():
	if request.method == 'GET':
		return redirect(url_for('main'))
	global grid, move_no, score
	try:
		new_grid = up(grid)
	except:
		return redirect(url_for('main'))
	
	score += score_vert(grid)
	if new_grid != grid:
		grid = add_random(new_grid)
		move_no += 1
	return render_template('home.html', grid=format_grid(grid), score=score, state=check_survive(grid), moves=move_no)


@app.route('/gamedown', methods=['GET', 'POST'])
def gamedown():
	if request.method == 'GET':
		return redirect(url_for('main'))
	global grid, move_no, score
	try:
		new_grid = down(grid)
	except:
		return redirect(url_for('main'))
	
	score += score_vert(grid)
	if new_grid != grid:
		grid = add_random(new_grid)
		move_no += 1
	return render_template('home.html', grid=format_grid(grid), score=score, state=check_survive(grid), moves=move_no)


@app.route('/gameleft', methods=['GET', 'POST'])
def gameleft():
	if request.method == 'GET':
		return redirect(url_for('main'))
	global grid, move_no, score
	try:
		new_grid = left(grid)
	except:
		return redirect(url_for('main'))
	
	score += score_hori(grid)
	if new_grid != grid:
		grid = add_random(new_grid)
		move_no += 1
	return render_template('home.html', grid=format_grid(grid), score=score, state=check_survive(grid), moves=move_no)


@app.route('/gameright', methods=['GET', 'POST'])
def gameright():
	if request.method == 'GET':
		return redirect(url_for('main'))
	global grid, move_no, score
	try:
		new_grid = right(grid)
	except:
		return redirect(url_for('main'))
	
	score += score_hori(grid)
	if new_grid != grid:
		grid = add_random(new_grid)
		move_no += 1
	return render_template('home.html', grid=format_grid(grid), score=score, state=check_survive(grid), moves=move_no)


@app.route('/bot', methods=['GET', 'POST'])
def bot():
	if request.method == 'GET':
		return redirect(url_for('main'))
	global grid, move_no, score
	try:
		grid
	except:
		return redirect(url_for('main'))
	
	move = find_best_move(grid)
	if move == -1:
		print('ended')
		move = random.randint(0,3)
	new_grid = move_ls[move](grid)
	score += score_ls[move](grid)
	if new_grid != grid:
		grid = add_random(new_grid)
		move_no += 1
	state = check_survive(grid)

	# additional debug info: eval_score, depth
	return render_template('home.html', grid = format_grid(grid), score=score, state=state, debug=DEBUG, moves=move_no)
		
if __name__ == '__main__':
	app.run(debug=True)