#!/usr/bin/env python3.9

import sys
import shutil
import os

print("start of processing")
src = os.environ['INPUT_DIR']
dest = os.environ['OUTPUT_DIR']
resources = os.environ['RESOURCES_DIR'] # static resources

print("Command line arguments ...")
print(sys.argv)
print("ENV variables ...")
print(os.environ)

files = os.listdir(resources)
print(files)

# create a file static-file.txt in the resources directory and read it here
if os.path.exists(f'{resources}/static-file.txt'):
    with open(f'{resources}/static-file.txt', "r") as file:
        content = file.read()

    print(content)

shutil.copytree(src, dest, dirs_exist_ok=True)
print("end of processing")