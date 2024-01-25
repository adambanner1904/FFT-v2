from flask import Blueprint, render_template, flash, redirect, url_for
from sqlalchemy import select

from .people_forms import NewPlayerForm, EditPlayerForm
from ... import db
from ...models import Player

people_bp = Blueprint('people_bp', __name__, template_folder='templates')


@people_bp.route('')
def people():
    players = db.session.scalars(select(Player)).all()
    return render_template('people.html', players=players)


@people_bp.route('/add_person', methods=['GET', 'POST'])
def add_person():
    form = NewPlayerForm()

    if form.validate_on_submit():
        name = form.name.data.lower()
        balance = form.balance.data
        club_id = 1
        is_active = True
        player_exists = Player.query.filter(Player.name == name).first()
        if player_exists:
            flash("Player already exists", category='error')
        else:
            player = Player(name=name, balance=balance, club_id=club_id, is_active=is_active)
            db.session.add(player)
            db.session.commit()
            flash("Player added", category='success')

    return render_template('add_person.html', form=form)


@people_bp.route('/edit_person/<player_name>', methods=['GET', 'POST'])
def edit_person(player_name):
    player = Player.query.filter(Player.name == player_name).first()
    form = EditPlayerForm(obj=player)
    if form.validate_on_submit():
        if form.name.data != player.name or form.balance.data != player.balance or form.is_active.data != player.is_active:
            player.name = form.name.data.lower()
            player.balance = form.balance.data
            player.is_active = form.is_active.data
            db.session.commit()
            flash("Player updated", category='success')
            return redirect(url_for('people_bp.people'))
        else:
            flash("You need to make a change", category='error')
    return render_template('edit_person.html', form=form, player=player)
