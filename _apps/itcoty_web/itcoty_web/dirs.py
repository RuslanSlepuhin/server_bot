import platform
from pathlib import Path
from itcoty_web.envs import load_config

env = load_config()

BASE_DIR = Path(__file__).resolve().parents[1]
DOCKER_CACHE_DIR = Path("/var/cache/app")
LOCAL_DIR = BASE_DIR / ".local"

STATIC_DIR = (
                 DOCKER_CACHE_DIR if DOCKER_CACHE_DIR.is_dir() else LOCAL_DIR
             ) / "static"

STATIC_DIR.mkdir(exist_ok=True, mode=0o777)
LOCAL_DIR.mkdir(exist_ok=True, mode=0o777)

if platform.system() == "Windows":
    BASE_DB_DIR = Path(f"{env.database.winpath}").resolve()
    DB_DIR = BASE_DB_DIR / f"{env.database.version}"
    DB_DATA = DB_DIR / "data"
    DB_CTL = DB_DIR / "bin" / "pg_ctl"
