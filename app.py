from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SUPERSECRETKEY'
app.config['UPLOAD_FOLDER'] = 'static/files'  # Folder to save uploaded files

class UploadFileForm(FlaskForm): # Form for file upload
    file = FileField('File', validators=[InputRequired()]) # File field with validation
    submit = SubmitField('Uplaod File')

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data # Get the uploaded file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename))) # Save the file securely
        return "File uploaded successfully!"  # Return a success message
    return render_template('home.html', form=form) 

if __name__ == '__main__':
    app.run(debug=True)