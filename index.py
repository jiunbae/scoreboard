from app import app

if __name__ == '__main__':
    app.run(debug=True)

# @app.route('/profile')
# def profile():
#     return render_template('login.html')

# @app.route('/submit/<pid>', methods=['POST'])
# def submit(pid):
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             # No file parts
#             return redirect(request.url)
#         file = request.files['file']
#         if file.filename == '':
#             # No selected file
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('uploaded_file', filename=filename))
