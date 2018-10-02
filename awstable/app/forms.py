from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    aws_access_key_id = StringField('AWS_Access_Key_Id', validators=[DataRequired()])
    aws_secret_access_key = StringField('AWS_Secret_Access_Key', validators=[DataRequired()])
    aws_region = StringField('Aws_Region', validators=[DataRequired()])

    submit = SubmitField('Submit')
