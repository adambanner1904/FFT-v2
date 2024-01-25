from wtforms import StringField, SubmitField, DecimalField, BooleanField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


class NewPlayerForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    balance = DecimalField("Balance")
    submit = SubmitField("Submit")


class EditPlayerForm(FlaskForm):
    name = StringField("Name", render_kw={"placeholder": "Name"})
    balance = DecimalField("Balance", render_kw={"placeholder": "Balance"})
    is_active = BooleanField("Is active")
    submit = SubmitField("Save changes")
