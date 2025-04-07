from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Optional

class UploadForm(FlaskForm):
    """Form for uploading an email or pasting email content"""
    email_file = FileField('Upload Email File', validators=[
        FileAllowed(['eml', 'txt', 'msg'], 'Only email files are allowed!')
    ])
    email_content = TextAreaField('Or paste email content here')
    submit = SubmitField('Analyze')