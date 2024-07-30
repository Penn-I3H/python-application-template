#!/usr/bin/env python3.9

import sys
import shutil
import os

print("start of processing")
src = os.environ['INPUT_DIR']
dest = os.environ['OUTPUT_DIR']

print("Command line arguments ...")
print(sys.argv)
print("ENV variables ...")
print(os.environment)

shutil.copytree(src, dest, dirs_exist_ok=True)
print("end of processing")
