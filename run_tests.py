#!/usr/bin/env python3
# based on https://anzui.de/en/blog/2015-05-21/

import os
import glob
import subprocess
import sys

blenderExecutable = 'blender'

# allow override of blender executable (important for CI!)
if len(sys.argv) > 1:
    blenderExecutable = sys.argv[1]

for file in glob.glob('./tests/*.py.blend'):
    print(file)
    subprocess.call([blenderExecutable, '--addons', 'hypermesh',
        '--factory-startup', '-noaudio',
        '-b', file,
        '--python', file[:-6]])
