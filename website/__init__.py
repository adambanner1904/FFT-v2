from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hellostensetheisrntesrn'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from common_routes import common_bp
    from .subdomains.people.people_routes import people_bp
    from .subdomains.events.events_routes import events_bp

    app.register_blueprint(people_bp, url_prefix='/people')
    app.register_blueprint(common_bp, url_prefix='/')
    app.register_blueprint(events_bp, url_prefix='/events')

    from .models import Club, Income, Expense, Player, Payment, Debt, Game, Training

    create_database(app)

    return app


def create_database(app):
    if not path.exists("website/instance/" + DB_NAME):
        with app.app_context():
            # db.drop_all()
            db.create_all()

            # from .models import Club
            #
            # club = Club(name='DY Athletic')
            # db.session.add(club)
            # db.session.commit()
            # print('DY created')
        print("Created database!")
