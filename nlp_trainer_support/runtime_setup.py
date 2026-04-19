from __future__ import annotations

import re

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

_POSTGRES_PATCHED = False


def apply_postgres_compatibility_patches() -> None:
    global _POSTGRES_PATCHED
    if _POSTGRES_PATCHED or DB_BACKEND != "postgres":
        return

    original_translate_sql = db.PostgresConnectionWrapper._translate_sql

    def patched_translate_sql(self, sql: str) -> str:
        translated = original_translate_sql(self, sql)
        if re.match(r"^\s*INSERT\s+OR\s+IGNORE\s+INTO\s+", translated, flags=re.IGNORECASE):
            translated = re.sub(
                r"^\s*INSERT\s+OR\s+IGNORE\s+INTO\s+",
                "INSERT INTO ",
                translated,
                count=1,
                flags=re.IGNORECASE,
            )
            stripped = translated.rstrip()
            has_semicolon = stripped.endswith(";")
            if has_semicolon:
                stripped = stripped[:-1].rstrip()
            translated = stripped + " ON CONFLICT DO NOTHING"
            if has_semicolon:
                translated += ";"
        return translated

    db.PostgresConnectionWrapper._translate_sql = patched_translate_sql
    _POSTGRES_PATCHED = True


def initialize_runtime_database(*, reset: bool = False) -> None:
    apply_postgres_compatibility_patches()
    db.initialize_database(reset=reset)
    if DB_BACKEND != "postgres":
        return

    with db.connect() as connection:
        connection.execute(POSTGRES_COMPATIBILITY_SQL)
        connection.commit()
