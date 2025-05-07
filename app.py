from flask import Flask, request, render_template, url_for
from solver import solve_sudoku, check_solution, solved_to_image, empty_grid

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/solve')
def solve():
    return render_template('solve.html')


@app.route('/sudoku', methods=['POST'])
def sudoku():
    photo = request.files
    grid = [['5', '3', '.', '.', '7', '.', '.', '.', '.'],
            ['6', '.', '.', '1', '9', '5', '.', '.', '.'],
            ['.', '9', '8', '.', '.', '.', '.', '6', '.'],
            ['8', '.', '.', '.', '6', '.', '.', '.', '3'],
            ['4', '.', '.', '8', '.', '3', '.', '.', '1'],
            ['7', '.', '.', '.', '2', '.', '.', '.', '6'],
            ['.', '6', '.', '.', '.', '.', '2', '8', '.'],
            ['.', '.', '.', '4', '1', '9', '.', '.', '5'],
            ['.', '.', '.', '.', '8', '.', '.', '7', '9']]
    # solvable = False
    solvable = True
    if solvable:
        filename = solved_to_image(solve_sudoku(grid))

    else:
        filename = 'empty_grid.png'

    return render_template('sudoku.html', image=url_for("static", filename=filename), solvable=solvable)


app.run()
