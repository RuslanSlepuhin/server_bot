from typing import Any

from django.core.management.base import BaseCommand
from itcoty_web.dirs import BASE_DIR


class Command(BaseCommand):
    """
    Handle the dev setting file creating.
    """

    def handle(self, *args: Any, **options: Any) -> None:
        """
        Reads settings and creates the new file on its base
        that contains also the settings for development.
        """
        base_settings = BASE_DIR / "itcoty_web" / "settings.py"
        dev_settings = BASE_DIR / "itcoty_web" / "drfout.py"

        with open(dev_settings, "w", encoding="UTF-8") as out:
            with open(base_settings, "r", encoding="UTF-8") as lines:
                for line in lines:
                    if "rest_framework.renderers.JSONRenderer" in line:
                        continue
                    elif "TEST_REQUEST_DEFAULT_FORMAT" in line:
                        continue
                    out.write(line)


