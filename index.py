from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/assignments')
def assignments():
    return render_template('list.html', assignments=get_assignments())

@app.route('/assignment/<pid>')
def assignment(pid):
    return render_template('assignment.html', pid=pid, assignment=get_assignment(int(pid)))

@app.route('/profile')
def profile():
    return render_template('login.html')

@app.route('/submit/<pid>', methods=['POST'])
def submit(pid):
    if request.method == 'POST':
        if 'file' not in request.files:
            # No file parts
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            # No selected file
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))

if __name__ == '__main__':
    app.run(debug=True)