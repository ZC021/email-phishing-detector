from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class TrainForm(FlaskForm):
    """Form for training the model"""
    dataset_path = StringField('Dataset Path', validators=[DataRequired()])
    test_size = FloatField('Test Size', validators=[
        NumberRange(min=0.1, max=0.5, message='Test size must be between 0.1 and 0.5')
    ], default=0.2)
    random_state = IntegerField('Random State', default=42)
    submit = SubmitField('Train Model')