# https://tinypng.com/developers/reference/python

import tinify
import os, time
from pathlib import Path
from progressbar import ProgressBar as pb

PATH_KEY = Path('src/config/key.txt')
PATH_DEBUG = Path('src/logs/debug.txt')
PATH_INPUT = Path('src/input')
PATH_OUTPUT = Path('src/output')

if not PATH_INPUT.exists():
    PATH_INPUT.mkdir(parents=True)

if not PATH_INPUT.exists():
    PATH_INPUT.mkdir(parents=True)

with open(Path(PATH_KEY), 'r') as f:
    tinify.key = f.read().strip()

names = list(path.name for path in Path('src/input').glob('*.*'))
if not names:
    print('No files found in input folder')
    exit()

n_success = 0
n_failure = 0

for name in pb()(names):

    try:
        source = tinify.from_file(PATH_INPUT / name)
        source.to_file(PATH_OUTPUT / name)

        n_success += 1

    except Exception as e:
        n_failure += 1

        with open(PATH_DEBUG, 'a') as f:
            f.write(str(e))
            f.write('\n')

print(f'Converted {n_success} / {len(names)} ({n_success / len(names) * 100:.2f})%')
if n_failure:
    print(f'Consult {PATH_DEBUG} for error log')
