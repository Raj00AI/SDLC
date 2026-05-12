from __future__ import annotations

from catalyst_ai.config import get_paths
from catalyst_ai.data.store import connect


def get_con():
    paths = get_paths()
    con = connect(paths.db_path)
    try:
        yield con
    finally:
        con.close()
