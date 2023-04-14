from logging_config import logging
from src.database import create_tables, insert_data_in_db

if __name__ == '__main__':

    logging.info('starting file execution...')
    create_tables()

    insert_data_in_db()

    logging.info('file execution is finished.')
