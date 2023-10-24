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

host = 'localhost'
port = 6379
print('Initializing cache')
cache = redis.Redis(host=host, port=port, db=0, decode_responses=True)

_initial_runs = cache.get('runs')
print(f'\t- app has run {_initial_runs} times')
cache.incr('runs')

print('Initializing security')
sec = redis.Redis(host=host, port=port, db=1,  decode_responses=True)
