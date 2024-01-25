from wtforms import StringField, SubmitField, DecimalField, BooleanField, HiddenField, Form, FormField, FieldList, \
    DateField, RadioField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, ValidationError
from flask_wtf import FlaskForm


class PlayerForm(Form):
    name = HiddenField('Name')
    balance = HiddenField('Balance')
    amount = DecimalField('Debt', render_kw={'style': 'width:7ch'}, validators=[Optional()])
    bank = DecimalField('Bank', render_kw={'style': 'width:7ch'}, validators=[Optional()])
    cash = DecimalField('Cash', render_kw={'style': 'width:7ch'}, validators=[Optional()])
    use_balance = BooleanField('Use Balance')


class InfoListForm(FlaskForm):
    player_info = FieldList(FormField(PlayerForm))
    submit = SubmitField('Submit', render_kw={'style': 'float:right;'})


class GameForm(FlaskForm):
    against = StringField('Game against:')
    date = DateField('Date')
    submit = SubmitField('Submit')


class TrainingForm(FlaskForm):
    name = HiddenField('Name')
    balance = HiddenField('Balance')
    came = BooleanField('Attendance')
    relief = BooleanField('Relief')


class AddTrainingForm(FlaskForm):
    date = DateField('Date')
    attendance = FieldList(FormField(TrainingForm))
    submit = SubmitField('Submit')
