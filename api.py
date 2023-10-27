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

    em = str(email).strip().lower()
    if len(em) > EMAIL_MAX_CHARS:
        raise Exception(f'Given email exceeds maximum allowed characters {EMAIL_MAX_CHARS}')

    d = {
            'email': em,
            }

    if name is not None:
        d['name'] = str(name).strip()
        if len(name) > EMAIL_MAX_CHARS:
            raise Exception(f'Given name exceeds maximum allowed characters {EMAIL_MAX_CHARS}')

        else:
            d['name'] = name

    if notes is not None:
        d['notes'] = str(notes).strip()
        if len(notes) > EMAIL_MAX_CHARS * 10:
            raise Exception(f'Notes cannot exceed {EMAIL_MAX_CHARS * 10}')

        else:
            d['notes'] = notes

    d['t'] = ts
    d['dt'] = dt

    return d.copy()

