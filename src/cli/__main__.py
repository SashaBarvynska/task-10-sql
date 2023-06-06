import sys
import os

# add current directory to path (so will be able to call)
sys.path.append(os.getcwd())

from src.cli.insert_data_to_db import run_db

run_db()
