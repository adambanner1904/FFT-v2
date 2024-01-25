from flask import Blueprint, render_template

common_bp = Blueprint('views', __name__)


@common_bp.route('/')
def home():
    return render_template('home.html')
