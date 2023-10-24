#!/usr/bin/env python3
"""
Copyright 2023 Patrick Ingham, Crystal Calvert

This file is part of the Cube Rubrics project: https://github.com/CubeRubrics

Cube Rubrics is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Cube Rubrics is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with Cube Rubrics. If not, see <https://www.gnu.org/licenses/>.
"""
import os
import sys
import yaml
import logging
import datetime
import random

from flask import Flask, flash, redirect, render_template, request, session, g
from flask import send_from_directory, url_for
from functools import wraps

def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('config.py')

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory('static', 'favicon.ico')

    return app

app = create_app()
app.config['DEBUG'] = True

logger = app.logger

from . import dbays

# https://flask.palletsprojects.com/en/3.0.x/patterns/viewdecorators/
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' in g:
            if g.user is None:
                return redirect(url_for('login', next=request.url))
        else:
            return redirect(url_for('login', next=request.url))

        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    if 'username' in session:
        print('User:', session['username'])

    else:
        print('User: NOT LOGGED IN')

    return render_template('index.html')


@app.route('/login/', methods=['GET', 'POST', 'PUT'])
def login():
    vali = None
    if request.method == 'POST':
        username = request.form.get('username')
        pw_raw = request.form.get('password')
        print(f'Logging in {username} with plaintext password {pw_raw}')
        vali = {'username': username, 'password': pw_raw}

    return render_template('login.html', r=vali)

@app.route('/logout/')
@login_required
def logout():
    return render_template('login.html', u=g.user)

@app.route('/analysis/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def analysis():
    return render_template('analysis.html')


@app.route('/api/')
@login_required
def api_root():
    return 'api v0'


@app.route('/about/')
def about():
    return render_template('about.html')
