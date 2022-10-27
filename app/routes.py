from errno import ENOTEMPTY
from flask import render_template, redirect, url_for, flash, request, jsonify, make_response
from app import app, db
from app.forms import GetPoke, LoginForm, RegistrationForm, AddPoke, DeletePokemonForm
from app.getPokemon import *
from app.colors import *
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, UserPokemon
from werkzeug.urls import url_parse
from datetime import datetime

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title = 'Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect('pokemon')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.first_name = form.first_name.data.lower()
        user.last_name = form.last_name.data.lower()
        user.email = form.email.data
        user.set_password(form.password.data)
        user.wins = 0
        user.losses = 0
        user
        with app.app_context():
            db.session.add(user)
            db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign up', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# TESTING FOR ADDING FROM BROWSING
@app.route('/addpokemon', methods = ['POST'])
def addpokemon():
    
    sent_pokemon = request.get_json()
    mon = UserPokemon()
    mon.user_id = current_user.id
    mon.pokemon_name = sent_pokemon['name'].lower()
    with app.app_context():
        db.session.add(mon)
        db.session.commit()
    return redirect(url_for('pokemon'))

@app.route('/pokemon', methods = ['GET', 'POST'])
@login_required
def pokemon():
    owned = [x.pokemon_name for x in UserPokemon.query.filter_by(user_id = current_user.id)]
    form = GetPoke()
    pokemon = ""
    error = ""
    if form.validate_on_submit():
        pokemon = addPokemon(form.name.data)
        form.name.data = ""
        error = ""
        if not pokemon:
            error = "Please enter a valid PoKémon."
            redirect(url_for('pokemon'))
    return render_template('pokemon.html', title='Pokémon', form=form, pokemon=pokemon, error=error, owned=owned, colors=colors)

@app.route('/<pokemon>')
def showStats(pokemon):
    pokemon = addPokemon(pokemon)
    return render_template('stats.html', pokemon=pokemon, colors=colors)

@app.route('/delete', methods = ['GET', 'POST'])
def delete():
    owned = [x.pokemon_name for x in UserPokemon.query.filter_by(user_id = current_user.id)]
    if len(owned) == 0:
        flash("You have no PoKémon")
        return redirect(url_for('user.showUser', username=current_user.username))
    if request.method == 'POST':
        info = request.get_json()
        for pokemon in info:
            mon = UserPokemon.query.filter_by(pokemon_name=pokemon).first()
            db.session.delete(mon)
            db.session.commit()
        return redirect(url_for('user.showUser', username=current_user.username))

    return render_template('delete.html', owned=owned)

@app.route('/battle')
def battle():
    enemy = 'Steve'
    enemy_pokemon = []
    for i in range(1, 6):
        enemy_pokemon.append(addPokemon(str(i)))
    owned = [x.pokemon_name for x in UserPokemon.query.filter_by(user_id = current_user.id)]
    owned_objects = [addPokemon(x) for x in owned]
    if len(owned) < 5:
        flash(f"You need to catch {5-len(owned)} more PoKémon before you can battle!")
        return redirect(url_for('user.showUser', username=current_user.username))
    # pokemon = [addPokemon(x) for x in owned]
    return render_template('battle.html', enemy=enemy, owned=owned_objects, enemy_pokemon=enemy_pokemon, colors=colors)