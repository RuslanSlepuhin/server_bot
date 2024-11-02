import psycopg2
import platform
import subprocess

from django.core.management.base import BaseCommand

from psycopg2 import sql
from typing import Any

from itcoty_web.envs import load_config
from itcoty_web.dirs import DB_DATA, DB_CTL


env = load_config()

def start_server():
    """ Starts the database server if it's not running. """

    this_platform = platform.system()

    if this_platform == "Windows":
        subprocess.run([str(DB_CTL), "start", "-D", str(DB_DATA)])
    elif this_platform == "Linux":
        subprocess.run(["sudo", "systemctl", ]) #????????????


def create_database(dbname):
    """ Creates the database if not exists. """

    conn = None
    cursor = None

    try:
        conn = psycopg2.connect(
            dbname=env.database.default,
            user=env.database.user,
            password=env.database.password,
            host=env.database.host,
            port=env.database.port,
        )
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute(
            sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(dbname)
            )
        )
        print(f"The database {dbname} has been created.")

    except psycopg2.errors.DuplicateDatabase:
        print(f"The database {dbname} already exists.")

    except psycopg2.OperationalError:
        start_server()

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


class Command(BaseCommand):
    """Handle a database creating."""

    def handle(self, *args: Any, **options: Any) -> None:
        """ Runs the database creating. """
        create_database(env.database.name)


def start_postgres():
    """ Starts the database server if it's not running. """
    conn = None

    try:
        conn = psycopg2.connect(
            dbname=env.database.default,
            user=env.database.user,
            password=env.database.password,
            host=env.database.host,
            port=env.database.port,
        )

    except psycopg2.errors.OperationalError:
        ...

    finally:
        if conn:
            conn.close()

