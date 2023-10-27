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
import redis
import random, string
import bcrypt

import click

from flask import current_app, g
import time

host = 'localhost'
port = 6379

def generate_plaintext_password(length=11):
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))


def get_db():
    if 'db' not in g:
        g.db = redis.Redis(host=host, port=port, db=0)

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

def init_db():
    db = get_db()
    db.flushdb()
    db.set('runs', 0)
    print('\t* Set run count to zero')

    uk = 'user:admin'
    db.hset(uk, 'logins', 0)
    db.hset(uk, 'created', time.time())
    pw_plain = generate_plaintext_password()
    pw_b = pw_plain.encode('utf-8')
    salt = bcrypt.gensalt()

    pw_h = bcrypt.hashpw(pw_b, salt)
    db.hset(uk, 's', salt)
    db.hset(uk, 'pw', pw_h)
    print('\t* Created new admin account with password:', pw_plain)


def store_subscriber(subscriber: dict):
    """
    Temporary measure to handle the subscriber page only
    """
    em = subscriber['email']
    store_db = get_db()
    bprev_emails = store_db.lrange('subscribers', 0, -1)
    prev_emails = [ x.decode() for x in bprev_emails ]
    print(prev_emails)
    if em in prev_emails:
        # Already subscribed, but we don't need to inform the user of
        # that, no reason to disclose subscribers
        return 0

    else:
        store_db.lpush('subscribers', em)

    skey = f'subscriber:{em}'
    subscriber['id'] = store_db.llen('subscribers')
    results = {}
    for k, v in subscriber.items():
        # store hash unless already exists. No overwriting!
        rk = store_db.hsetnx(skey, k, v)
        print(rk)

    return 1


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    click.echo('Initializing the database:')
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
