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

EMAIL_MAX_CHARS = 254

def process_subscriber(email: str, name=None, notes=None):
    ts = time.time()
    dt = datetime.datetime.utcnow()
    if email is None:
        raise Exception('Email address is required')

    em = str(email).strip().lower()
    if len(em) > EMAIL_MAX_CHARS:
        raise Exception(f'Given email exceeds maximum allowed characters {EMAIL_MAX_CHARS}')

    elif len(em) <= 3:
        raise Exception(f'Given email address "{em}" too short')

    d = {
            'email': em,
            }

    if name is not None:
        d['name'] = str(name).strip()
        if len(name) > EMAIL_MAX_CHARS:
            raise Exception(f'Given name exceeds maximum allowed characters {EMAIL_MAX_CHARS}')

        elif len(name) < 1:
            # that's blank too
            pass

        else:
            d['name'] = name

    if notes is not None:
        d['notes'] = str(notes).strip()
        if len(notes) > EMAIL_MAX_CHARS * 10:
            raise Exception(f'Notes cannot exceed {EMAIL_MAX_CHARS * 10}')
        elif len(notes) < 1:
            # that's blank
            pass

        else:
            d['notes'] = notes

    d['t'] = ts
    d['dt'] = dt

    return d.copy()

