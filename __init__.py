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
import time
import random

from flask import Flask, flash, redirect, render_template, request, session, g
from flask import send_from_directory, url_for
from functools import wraps

import bcrypt

def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('config.py')

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory('static', 'favicon.ico')
    
    from . import db
    db.init_app(app)
    return app

app = create_app()
app.config['DEBUG'] = True

logger = app.logger

# https://flask.palletsprojects.com/en/3.0.x/patterns/viewdecorators/
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(request.base_url)
        if 'user' in g:
            if g.user is None:
                return redirect(url_for('login', next=request.base_url))
        else:
            return redirect(url_for('login', next=request.base_url))

        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def load_logged_in_user():
    username = session.get('username')
    if username is None:
        g.user = None

    else:
        uk = f'user:{username}'
        # NOTE: Every user should have a 'created' field now.
        uc = db.get_db().hget(uk, 'created')
        if uc is None:
            print(f'Error, {uk} lacks a "created" key')

        else:
            session['username'] = username
            _t = time.time()
            # Load the user
            db.get_db().hset(uk, 'accessed', _t)
            d = {
                    'created': uc,
                    'name': username,
                    'accessed': _t,
                    }
            g.user = d.copy()

@app.route('/')
def index():
    print(request.headers)
    if 'username' in session:
        username = session['username']
    else:
        print('CubeRubrics User: NOT LOGGED IN')

    return render_template('index.html')


def check_login(username: str, pw_plain: str):
    uk = f'user:{username}'
    pw_b = str(pw_plain).encode('utf-8')

    pw_stored = db.get_db().hget(uk, 'pw')
    if pw_stored is None:
        logger.warning(f'No password found for username "{username}"')
        time.sleep(0.01)
        return False

    else:
        s = db.get_db().hget(uk, 's')
        pw = bcrypt.hashpw(pw_b, s)
        return pw == pw_stored

@app.route('/login/', methods=['GET', 'POST', 'PUT'])
def login():
    vali = None
    if request.method == 'POST':
        # TODO: move all of this to WTForms
        username = str(request.form.get('username')).strip()
        pw_raw = request.form.get('password')

        vali = {'username': username, 'password': pw_raw}

        # FIXME: Not a longterm solution to getting DOS'd 
        time.sleep(0.1)

        # FIXME: Filter out any non-standard characters
        if len(username) < 3:
            flash(f'Usernames must be at least 3 (valid) characters long', 'warning')

        else:
            if check_login(username, pw_raw):
                print('Valid credentials for', username)
                flash(f'Now logged in as {username}. Hello!', 'success')
                session['username'] = username
                db.get_db().hset(f'user:{username}', 'lastlogin', time.time())
                if request.args:
                    next_url = request.args.get('next')
                    if next_url:
                        print('Continuing to next link:', next_url)
                        return redirect(request.args.get('next'))
                    else:
                        print('No next link, sending to /')
                        return redirect(url_for('index'))
                else:
                    return redirect(url_for('index'))
            else:
                print('invalid credentials for', username)

    return render_template('login.html', r=vali)

@app.route('/logout/')
def logout():
    username = session.get('username')
    if username is None:
        flash('You were not logged in', 'info')
        return redirect(url_for('index'))

    uk = f'user:{username}'
    db.get_db().hset(uk, 'lastlogout', time.time())
    session.clear()
    flash(f'Logged out from {username}. Bye!', 'success')

    return redirect(url_for('index'))

@app.route('/analysis/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def analysis():
    return render_template('analysis.html')


# TODO: make this a Blueprint
@app.route('/api/')
@login_required
def api():
    return 'api v0'


@app.route('/about/')
def about():
    return render_template('about.html')

