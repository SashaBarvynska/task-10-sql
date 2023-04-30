import typer

from logging_config import logging
from src.database import create_tables, insert_data

run_db = typer.Typer()


@run_db.command()
def create_tables_in_db() -> None:
    logging.info('starting file execution...')
    create_tables()


@run_db.command()
def insert_data_in_db() -> None:
    insert_data()
    logging.info('file execution is finished.')


if __name__ == '__main__':
    run_db()
