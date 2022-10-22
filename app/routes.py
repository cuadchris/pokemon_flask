from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.forms import GetPoke, LoginForm, RegistrationForm, AddPoke
from app.getPokemon import *
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, UserPokemon
from werkzeug.urls import url_parse

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

@app.route('/add', methods = ['GET', 'POST'])
@login_required
def add():
    owned = [x.pokemon_name for x in UserPokemon.query.filter_by(user_id = current_user.id)]
    form = AddPoke()
    if form.validate_on_submit():
        if not addPokemon(form.name.data):
            flash('Enter valid pokemon')
            return redirect(url_for('add'))
        if form.name.data in owned:
            flash('You own this pokemon already!')
            return redirect(url_for('add'))
        mon = UserPokemon()
        mon.user_id = current_user.id
        mon.pokemon_name = form.name.data
        with app.app_context():
            db.session.add(mon)
            db.session.commit()
        flash(f'{form.name.data.capitalize()} added to your collection!')
        return redirect(url_for('add'))
    return render_template('add.html', title="Add Pokemon", form=form)

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
    return render_template('pokemon.html', title='Pokémon', form=form, pokemon=pokemon, error=error, owned=owned)

@app.route('/collection')
def collection():
    owned = [x.pokemon_name for x in UserPokemon.query.filter_by(user_id = current_user.id)]
    owned_objects = [addPokemon(x) for x in owned]
    return render_template('collection.html', title='Collection', owned=owned_objects)