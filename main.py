from flask import Flask, render_template, request, redirect, url_for
from web import *

### Flask App ###
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def main():
	global grid, move_no
	grid = make_grid()
	move_no = 0
	score = 0
	return render_template('home.html', grid = format_grid(grid), score=score, state=True, moves=move_no)
	
@app.route('/gameup', methods=['GET', 'POST'])
def gameup():
	if request.method == 'GET':
		return redirect(url_for('main'))
	global grid,move_no
	grid, state, score, move_no = on_press('w', move_no, grid)
	return render_template('home.html', grid = format_grid(grid), score=score, state=state, moves=move_no)
	
@app.route('/gamedown', methods=['GET', 'POST'])
def gamedown():
	if request.method == 'GET':
		return redirect(url_for('main'))
	global grid, move_no
	grid, state, score, move_no = on_press('s', move_no, grid)
	return render_template('home.html', grid = format_grid(grid), score=score, state=state, moves=move_no)
	
@app.route('/gameleft', methods=['GET', 'POST'])
def gameleft():
	if request.method == 'GET':
		return redirect(url_for('main'))
	global grid, move_no
	grid, state, score, move_no = on_press('a', move_no, grid)
	return render_template('home.html', grid = format_grid(grid), score=score, state=state, moves=move_no)
	
@app.route('/gameright', methods=['GET', 'POST'])
def gameright():
	if request.method == 'GET':
		return redirect(url_for('main'))
	global grid, move_no
	grid, state, score, move_no = on_press('d', move_no, grid)
	return render_template('home.html', grid = format_grid(grid), score=score, state=state, moves=move_no)

@app.route('/bot', methods=['GET', 'POST'])
def bot():
	if request.method == 'GET':
		return redirect(url_for('main'))
	global grid, move_no
	if len(find_empty(grid)) <5:
		depth = 6
	else:
		depth = 4
	move, eval = expectimax(grid, depth)
	grid, state, score, move_no = on_press(move, move_no, grid)

	# additional argument for debug: mono, free, total
	return render_template('home.html', grid = format_grid(grid), score=score, state=state, debug=True, total=eval, moves=move_no)
		
if __name__ == '__main__':
	app.run(debug=True)