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

from flask import Flask, flash, redirect, render_template, request, session
from flask import send_from_directory

from . import dbays

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
# FIXME: Decorator not working, gah, see:
# https://flask.palletsprojects.com/en/3.0.x/patterns/viewdecorators/
def incr_page(f):
    print('hi')
    def check_f(*args, **kwargs):
        print('f:', f)
        print('f args:\t', *args)
        print('f kwargs:\t', **kwargs)
        return f(*args, **kwargs)

    check_f.__name__ = f.__name__
    return f

@app.route('/')
def index():
    if 'username' in session:
        print('User:', session['username'])

    else:
        print('User: NOT LOGGED IN')

    return render_template('index.html')


@app.route('/analysis/', methods=['GET', 'POST', 'PUT', 'DELETE'])
@incr_page
def analysis():
    print(dbays.cache.get('analysis'))
    return render_template('analysis.html')


@app.route('/api/')
def api_root():
    return 'api v0'


@app.route('/about/')
def about():
    return render_template('about.html')
