import typer
from .logging_config import logging
from src.database.helpers import create_tables, insert_data


run_db = typer.Typer()


@run_db.command("create_tables_in_db")
def _create_tables_in_db() -> None:
    logging.info("Starting file execution...")
    create_tables()


@run_db.command("insert_data_in_db")
def _insert_data_in_db() -> None:
    insert_data()
    logging.info("File execution is finished.")
