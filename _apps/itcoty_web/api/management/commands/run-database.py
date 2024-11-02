import platform
import psycopg2
import subprocess

from django.core.management.base import BaseCommand
from psycopg2 import sql
from typing import Any

from itcoty_web.envs import load_config
from itcoty_web.dirs import DB_DATA, DB_CTL


env = load_config()


def start_server() -> bool:
    """ Starts the database server if it's not running. """

    if (DB_DATA / "postmaster.pid").exists():
        return True

    try:
        this_platform = platform.system()

        if this_platform == "Windows":
            subprocess.run([DB_CTL, "start", "-D", DB_DATA])

        elif this_platform == "Linux":
            subprocess.run(["sudo", "systemctl", "start", "postgresql"])

    except psycopg2.OperationalError:
        return False

    else:
        return True


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

        cursor.execute(sql.SQL(
            "CREATE DATABASE {}").format(sql.Identifier(dbname)
                                         )
                       )
    except psycopg2.errors.DuplicateDatabase:
        cursor.close()
        conn.close()

    else:
        cursor.close()
        conn.close()


class Command(BaseCommand):
    """Handle a database creating."""

    def handle(self, *args: Any, **options: Any) -> None:
        """ Runs the database creating. """

        server_is_running = start_server()

        if server_is_running:
            create_database(env.database.name)
