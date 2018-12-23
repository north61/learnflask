from wtforms import Form,StringField,PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,length 
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileRequired,FileAllowed
from flask_ckeditor import CKEditorField


class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),length(8,128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')

class UploadForm(FlaskForm):
    photo = FileField('Upload Image',validators=[FileRequired(),FileAllowed(['jpg','jpeg','png','gif'])])
    submit = SubmitField()

class RichTextForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired(),length(1,50)])
    body = CKEditorField('Body',validators=[DataRequired()])
    submit = SubmitField('Publish')

class NewNoteForm(FlaskForm):
    body = TextAreaField('Body',validators=[DataRequired()])
    submit = SubmitField('Submit')

class EditNoteForm(FlaskForm):
    body = TextAreaField('Body',validators=[DataRequired()])
    submit = SubmitField('Edit')

class DeleteNoteForm(FlaskForm):
    submit = SubmitField('Delete')
