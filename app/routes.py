from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.forms import GetPoke, LoginForm, RegistrationForm
from app.getPokemon import *
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
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

@app.route('/pokemon', methods = ['GET', 'POST'])
@login_required
def pokemon():
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
    return render_template('pokemon.html', title = 'Pokémon', form = form, pokemon = pokemon, error = error)