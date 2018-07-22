from flask import Flask, render_template

from lib.utils import get_assignments, get_assignment

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/assignments')
def assignments():
    return render_template('list.html', assignments=get_assignments())

@app.route('/assignment/<pid>')
def assignment(pid):
    return render_template('assignment.html', assignment=get_assignment(int(pid)))

@app.route('/submit')
def submit():
    return render_template('submit.html')

if __name__ == '__main__':
    app.run(debug=True)