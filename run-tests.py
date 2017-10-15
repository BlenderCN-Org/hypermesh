#!/usr/bin/env python3
# based on https://anzui.de/en/blog/2015-05-21/

import glob
import subprocess
import sys
import os

blenderExecutable = 'blender'

# allow override of blender executable (important for CI!)
if len(sys.argv) > 1:
    blenderExecutable = sys.argv[1]

for file in glob.glob('./tests/*.py'):
    print(file)
    command = [
        blenderExecutable,
        '--addons', 'hypermesh',
        '--factory-startup',
        '-noaudio',
        '--python-exit-code', '1',
        '-b']
    if os.path.isfile(file + '.blend'):
        command.append(file + '.blend')
    command.extend(['--python', file])
    exitcode = subprocess.call(command)
    if exitcode != 0:
        sys.exit(exitcode)
