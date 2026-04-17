from __future__ import annotations

from . import db
from .config import DB_BACKEND

POSTGRES_COMPATIBILITY_SQL = """
CREATE OR REPLACE FUNCTION public.round(double precision, integer)
RETURNS numeric
LANGUAGE sql
IMMUTABLE
AS $$
    SELECT round($1::numeric, $2)
$$
"""


def initialize_runtime_database(*, reset: bool = False) -> None:
    db.initialize_database(reset=reset)
    if DB_BACKEND != "postgres":
        return

    with db.connect() as connection:
        connection.execute(POSTGRES_COMPATIBILITY_SQL)
        connection.commit()
