from typing import Generator
from os import listdir
from os.path import isfile, join
import re
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import sqlite3


def process_files_in_dir(dir_path: str) -> Counter:
    """
    Method count words from the whole files in directory in multithreading way.
    :param dir_path: string directory path
    :return: Counter object
    """
    main_result = Counter()
    with ThreadPoolExecutor(5) as executor:
        files_gen = get_files(dir_path)
        result_counters = executor.map(process_file, files_gen)
    for counter in result_counters:
        main_result.update(counter)
    return main_result


def get_files(dir_path: str) -> Generator[str, None, None]:
    """
    Method process all objects inside directory and find only files.
    :param dir_path: string path of the dir.
    :return: Generator for iterate over the strings
    """
    for file_name in listdir(dir_path):
        full_file_path = join(dir_path, file_name)
        if isfile(full_file_path):
            yield full_file_path


def process_file(file_path: str) -> Counter:
    """
    Method splits string into words by regular expression.
    :param file_path: string value
    :return:
    """
    words = Counter()
    try:
        with open(file_path, "rt") as file_descriptor:
            for line in file_descriptor:
                for word in re.split(r",|\.|\s", line):
                    word = word.strip()
                    if word:
                        words[word] += 1
    except UnicodeDecodeError:
        # It happens if it is binary file
        return Counter()
    return words


def work_with_db(bag_of_words: Counter, dir_path: str, db_name="bag_of_words.db"):
    """
    Method for writing bag of words to database in the same directory.
    :param bag_of_words: Counter object where keys - words, values - word`s counts
    :param dir_path: string value of the directory path
    :param db_name: name of the database
    :return: None
    """
    full_db_path = join(dir_path, db_name)
    try:
        conn = create_connection(full_db_path)
        cursor = conn.cursor()
        create_table(cursor)
        write_to_db(cursor, bag_of_words)
        conn.commit()
        conn.close()
    except :
        print("Internal error")


def create_connection(full_db_path: str) -> sqlite3.Connection:
    """
    Method for creating connection to database.
    :param full_db_path: string value path of database file.
    :return: connection object
    """
    return sqlite3.connect(full_db_path)


def create_table(cursor: sqlite3.Cursor):
    """
    Method for creating table.
    :param cursor: sqlite Cursor object.
    :return: None
    """
    sql_query = "CREATE TABLE IF NOT EXISTS BAG_OF_WORDS(" \
                "ID INTEGER PRIMARY KEY AUTOINCREMENT," \
                "WORD STRING," \
                "COUNTER INTEGER)"
    cursor.execute(sql_query)


def write_to_db(cursor: sqlite3.Cursor, bag_of_words: Counter):
    """
    Method for inserting words with counts to database.
    :param cursor: sqlite Cursor object
    :param bag_of_words: Counter object where words - keys, values - counts of the words.
    :return: None
    """
    sql_query = "INSERT INTO BAG_OF_WORDS(WORD, COUNTER)" \
                "VALUES\n"
    values_to_insert = ",\n".join((f"('{word}', {count})" for word, count in bag_of_words.items()))
    full_query = f"{sql_query}{values_to_insert}"
    cursor.execute(full_query)
