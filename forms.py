from wtforms import Form,StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,length 
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileRequired,FileAllowed


class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),length(8,128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')

class UploadForm(FlaskForm):
    photo = FileField('Upload Image',validators=[FileRequired(),FileAllowed(['jpg','jpeg','png','gif'])])
    submit = SubmitField()

