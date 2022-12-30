from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models import User, UserPokemon
from flask_login import current_user, login_required
from app.user.forms import EditProfileForm
from app.models import db
from datetime import datetime
from app.getPokemon import *
from app.colors import colors

user = Blueprint('user', __name__, template_folder='user_templates', url_prefix = "/user")

@user.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@user.route('/<username>')
@login_required
def showUser(username):
    user = User.query.filter_by(username=username).first_or_404()
    owned = [x.pokemon_name for x in UserPokemon.query.filter_by(user_id = user.id).order_by(UserPokemon.pokemon_name)]
    owned_objects = [addPokemon(x) for x in owned]
    wins = user.wins
    losses = user.losses
    if wins == 0 and losses == 0:
        ratio = 0
    else:
        ratio = int((wins/(wins + losses)) * 100)
    return render_template('user.html', title = 'Profile', user=user, owned=owned_objects, colors=colors, wins=wins, losses=losses, ratio=ratio)

@user.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user.showUser', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@user.route('/updatewins')
@login_required
def wins():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    user.wins += 1
    db.session.add(user)
    db.session.commit()
    return {'losses': user.losses, 'wins': user.wins}

@user.route('/updatelosses')
@login_required
def losses():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    user.losses += 1
    db.session.add(user)
    db.session.commit()
    return {'losses': user.losses, 'wins': user.wins}
