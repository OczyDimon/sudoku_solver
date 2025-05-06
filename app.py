from flask import Flask, request, render_template

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
    solved = '5 3 . |. 7 . |. . .\n' \
             '6 . . |1 9 5 |. . .\n' \
             '. 9 8 |. . . |. 6 .\n' \
             '------+------+------\n'\
             '8 . . |. 6 . |. . 3\n'\
             '4 . . |8 . 3 |. . 1\n' \
             '7 . . |. 2 . |. . 6\n' \
             '------+------+------\n' \
             '. 6 . |. . . |2 8 .\n' \
             '. . . |4 1 9 |. . 5\n' \
             '. . . |. 8 . |. 7 9\n'
    solvable = True
    return render_template('sudoku.html', solved=solved, solvable=solvable)


app.run()
