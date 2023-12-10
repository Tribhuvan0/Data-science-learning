from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'files'

# Ensure the "uploads" folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    # Get the list of uploaded files
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('taskA1index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    # If the user does not select a file, the browser submits an empty file
    if file.filename == '':
        return redirect(request.url)

    # Save the file to the "uploads" folder
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
