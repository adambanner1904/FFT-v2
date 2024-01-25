from flask import Blueprint, render_template, flash, url_for, redirect
from sqlalchemy import select, inspect

from website import db
from website.models import Player, Game, Training, Debt
from website.subdomains.events.event_forms import GameForm, InfoListForm, AddTrainingForm

events_bp = Blueprint('events_bp',
                      __name__,
                      template_folder='templates')


@events_bp.route('/')
def events():
    all_events = db.session.query(Debt.game_id, Debt.training_id, Game.date).all()
    print(all_events)
    games = db.session.scalars(select(Game)).all()
    return render_template('events.html', events=games)


@events_bp.route('/add_game', methods=['GET', 'POST'])
def add_game():
    # Game form
    form = GameForm()
    # Handling form information
    if form.validate_on_submit():
        date = form.date.data
        against = form.against.data
        game_exists = Game.query.filter(Game.date == date).first()
        # If game exists then game needs to be edited instead
        if game_exists:
            flash("Game already exists", category='error')
        # Else create the game
        else:
            game = Game(date=date, against=against)
            db.session.add(game)
            db.session.commit()
            flash("Game added", category='success')

    return render_template('add_game.html', form=form)


@events_bp.route('/edit_game/<game_name>', methods=['GET', 'POST'])
def edit_game(game_name):
    return render_template('edit_game.html')


def get_player_list(db, type):
    players_with_debt = db.session.query(Player.id, Player.name, Player.balance, Debt.amount). \
        filter(Player.id == Debt.player_id).order_by(Player.name).all()
    all_players = db.session.query(Player.name).all()

    players_with_debt_list = [player.name for player in players_with_debt]
    all_players_list = [player.name for player in all_players]
    players_info = db.session.query(Player.id, Player.name, Player.balance, Debt.amount). \
        filter(Player.id == Debt.player_id).order_by(Player.name).all()
    players_without_debt = db.session.query(Player.id, Player.name, Player.balance). \
        filter(Player.name.notin_(players_with_debt_list)).order_by(Player.name).all()
    for player in players_without_debt:
        players_info.append(player)

    return players_info


@events_bp.route('/update_game/<game_date>', methods=['GET', 'POST'])
def update_game(game_date):
    # Generate forms for display
    game = db.session.scalar(select(Game).where(Game.date == game_date))

    players = get_player_list(db, type='game')
    data = {'player_info': players}
    form = InfoListForm(data=data)
    if form.validate_on_submit():
        print(form.data)

        # Iterate through all players
        for row in form.player_info:

            # Get form data
            name = row.form.name.data
            if not row.form.amount.data:
                amount = 0
            else:
                amount = float(row.form.amount.data)
            bank = row.form.bank.data
            cash = row.form.cash.data
            use_balance = row.form.use_balance.data

            # Get player object from database
            player = db.session.scalar(select(Player).where(Player.name == name))

            # If the amount is not 0 then update balance and create a debt for that player for that game
            debt_if_exists = db.session.scalar(select(Debt).where(Debt.player_id == player.id))

            # Check if debt already exists
            # If so continue

            if debt_if_exists:
                if amount == 0:
                    player.balance += debt_if_exists.amount - amount
                    db.session.delete(debt_if_exists)
                    db.session.commit()
                    flash("Debt deleted", category='success')

                elif debt_if_exists.amount != amount:
                    player.balance += debt_if_exists.amount - amount
                    debt_if_exists.amount = amount
                    db.session.commit()
                    flash("Debt updated", category='success')


            elif amount != 0:
                player.balance -= amount
                debt = Debt(player_id=player.id, amount=amount, game_id=game.id)
                db.session.add(debt)
                db.session.commit()
                flash("Debt added", category='success')

        return redirect(url_for('events_bp.events'))
    return render_template('update_game.html', form=form, game=game)


@events_bp.route('/add_training', methods=['GET', 'POST'])
def add_training():
    players = db.session.query(Player.id, Player.name, Player.balance). \
        filter(Player.id == Debt.player_id).order_by(Player.name).all()
    print(players)
    data = {'attendance': players}
    form = AddTrainingForm(data=data)
    print(form.data)
    return render_template('add_training.html', form=form)
