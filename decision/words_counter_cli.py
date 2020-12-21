from argparse import ArgumentParser
from os.path import abspath

from .helpers import process_files_in_dir, work_with_db

# init parser for CLI
parser = ArgumentParser(description="Count words in txt files in directory and write to SQLite database")

# add arguments for CLI
parser.add_argument("-d", action="store", dest="directory", type=str, help="get directory path")


# parse got arguments
args = parser.parse_args()

if args.directory:
    try:
        dir_path = abspath(args.directory)
        bag_of_words = process_files_in_dir(dir_path)
        work_with_db(bag_of_words, dir_path)
        result = "Words are counted"
    except FileNotFoundError:
        result = "Wrong directory! Please, try another one."
else:
    result = "No arguments in CLI"
print(result)
