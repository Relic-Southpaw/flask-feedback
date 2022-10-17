from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length


class UserForm(FlaskForm):
    """Form for adding / editing user."""

    username = StringField("Username",
                       validators=[InputRequired()])

    password = PasswordField("Password",
                       validators=[InputRequired()])

    email = StringField("Email Address",
                        validators=[InputRequired(), Email()])

    first_name = StringField("First",
                       validators=[InputRequired()])

    last_name = StringField("Last",
                       validators=[InputRequired()])

class LoginForm(FlaskForm):
    """form for logging in user"""
    username = StringField("Username",
                       validators=[InputRequired()])

    password = PasswordField("Password",
                       validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    """Form for user feedback"""

    title = StringField("Title",
                        validators=[InputRequired(), Length(max=100)],
    )
    content = StringField("Content",
                        validators=[InputRequired()],
    )