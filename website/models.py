from sqlalchemy import ForeignKey

from website import db
# from flask_login import UserMixin
from sqlalchemy.sql import func


class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    players = db.Relationship('Player', backref='club_players')
    income = db.Relationship('Income', backref='club_income')
    expenses = db.Relationship('Expense', backref='club_expenses')


class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    club_id = db.Column(db.Integer, ForeignKey('club.id'))
    amount = db.Column(db.Float)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    club_id = db.Column(db.Integer, ForeignKey('club.id'))
    amount = db.Column(db.Float)


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    club_id = db.Column(db.Integer, ForeignKey("club.id"))
    name = db.Column(db.String(150), unique=True)
    is_active = db.Column(db.Boolean, nullable=False)
    balance = db.Column(db.Float)
    player_payments = db.Relationship('Payment', backref='player_payments')
    player_debts = db.Relationship('Debt', backref='player_debts')


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, ForeignKey('player.id'))
    amount = db.Column(db.Integer, primary_key=True)
    payment_method = db.Column(db.Integer, primary_key=True)


class Debt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, ForeignKey('player.id'))
    game_id = db.Column(db.Integer, ForeignKey('game.id'))
    training_id = db.Column(db.Integer, ForeignKey('training.id'))
    amount = db.Column(db.Float)
    payment_id = db.Column(db.Integer, ForeignKey('payment.id'))


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    against = db.Column(db.String(100))
    debts = db.Relationship('Debt', backref='game')


class Training(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    debts = db.Relationship('Debt', backref='training')