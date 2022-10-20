from flask import render_template, redirect, url_for
from app import app
from app.forms import GetPoke
from app.getPokemon import *

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title = 'Home')

@app.route('/pokemon', methods = ['GET', 'POST'])
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