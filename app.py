from flask import Flask, request, render_template, url_for
from solver import solve_sudoku, solved_to_image, check_solution
from sudoku_recognition import recognize_img
import cv2


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/solve')
def solve():
    return render_template('solve.html')


@app.route('/sudoku', methods=['POST'])
def sudoku():
    if request.method == 'POST':
        photo = request.files['photo']
        photo.save(f"uploads/{photo.filename}")
        img = cv2.imread(f"uploads/{photo.filename}")
        grid, solvable = recognize_img(img)

        solved = solve_sudoku(grid)

        filename = 'numbers/0.png'

        if solved == -1:
            solvable = False

        else:
            if solvable:
                if check_solution(solved):
                    filename = solved_to_image(solved)

                else:
                    solvable = False

            else:
                solvable = False

        return render_template('sudoku.html', image=url_for("static", filename=filename), solvable=solvable)


app.run()
