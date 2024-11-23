# https://tinypng.com/developers/reference/python

import tinify
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

paths = list(path for path in Path('src/input').glob('*.*'))
if not paths:
    print('No files found in input folder. Exiting')
    exit()

convert = input('Convert to webp? [Y/N; default N]: ').upper().strip()
convert = convert.startswith('Y')

n_success = 0
n_failure = 0

for path in pb()(paths):

    try:
        source = tinify.from_file(PATH_INPUT / path.name)
        
        if convert:
            source = source.convert(type='image/webp')
            source.to_file(PATH_OUTPUT / f'{path.stem}.webp')

        else:
            source.to_file(PATH_OUTPUT / path.name)

        n_success += 1

    except Exception as e:
        n_failure += 1

        with open(PATH_DEBUG, 'a') as f:
            f.write(f'{path}\n{e}\n\n')

word = 'Shrunk' if not convert else 'Converted'
print(f'{word} {n_success} / {len(paths)} ({n_success / len(paths) * 100:.2f})%')
if n_failure:
    print(f'Consult {PATH_DEBUG} for error log')
