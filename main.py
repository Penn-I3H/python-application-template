#!/usr/bin/env python3.9

import sys
import shutil
import os



try:
    print("start of processing")
    src = os.environ['INPUT_DIR']
    dest = os.environ['OUTPUT_DIR']

    print("Command line arguments ...")
    print(sys.argv)
    print("ENV variables ...")
    print(os.environ)
    shutil.copytre(src, dest, dirs_exist_ok=True)
    print("end of processing")
except Exception as e:
    sys.exit(e)



