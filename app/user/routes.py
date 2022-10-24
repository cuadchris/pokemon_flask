from flask import Blueprint, render_template
from app.models import User

user = Blueprint('user', __name__, template_folder='user_templates')

@user.route('/<username>')
def showUser(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('user.html', user=user)