from pathlib import Path

MAIN_DIR = Path(__file__).resolve().parents[3]
BASE_DIR = Path(__file__).resolve().parents[1]
DOCKER_CACHE_DIR = Path("/var/cache/app")
LOCAL_DIR = BASE_DIR / ".local"

STATIC_DIR = (
                 DOCKER_CACHE_DIR if DOCKER_CACHE_DIR.is_dir() else LOCAL_DIR
             ) / "django-static"

STATIC_DIR.mkdir(exist_ok=True, mode=0o777)