from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS studies (
  study_id VARCHAR PRIMARY KEY,
  title VARCHAR,
  phase VARCHAR,
  status VARCHAR,
  condition VARCHAR,
  planned_enrollment INTEGER,
  start_date DATE
);

CREATE TABLE IF NOT EXISTS sites (
  site_id VARCHAR PRIMARY KEY,
  study_id VARCHAR,
  country VARCHAR,
  investigator VARCHAR,
  planned_activation_date DATE,
  actual_activation_date DATE,
  FOREIGN KEY (study_id) REFERENCES studies(study_id)
);

CREATE TABLE IF NOT EXISTS weekly_metrics (
  study_id VARCHAR,
  site_id VARCHAR,
  week_start DATE,
  planned_enrolled_cum INTEGER,
  actual_enrolled_cum INTEGER,
  screened_cum INTEGER,
  screen_fail_cum INTEGER,
  open_queries INTEGER,
  protocol_deviations INTEGER,
  vendor_tickets INTEGER
);

CREATE TABLE IF NOT EXISTS milestones (
  study_id VARCHAR,
  name VARCHAR,
  planned_date DATE,
  actual_date DATE
);

CREATE TABLE IF NOT EXISTS risks (
  risk_id VARCHAR PRIMARY KEY,
  study_id VARCHAR,
  rule_id VARCHAR,
  title VARCHAR,
  severity VARCHAR,
  score DOUBLE,
  drivers VARCHAR,
  recommendation VARCHAR,
  evidence JSON,
  created_at VARCHAR
);

CREATE TABLE IF NOT EXISTS actions (
  action_id VARCHAR PRIMARY KEY,
  study_id VARCHAR,
  linked_risk_id VARCHAR,
  title VARCHAR,
  owner VARCHAR,
  due_date DATE,
  status VARCHAR,
  created_by VARCHAR,
  created_at VARCHAR
);
"""


def connect(db_path: Path) -> duckdb.DuckDBPyConnection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(db_path))
    con.execute(SCHEMA_SQL)
    return con


def write_df(con: duckdb.DuckDBPyConnection, table: str, df: pd.DataFrame) -> None:
    con.register("_df", df)
    con.execute(f"DELETE FROM {table}")
    con.execute(f"INSERT INTO {table} SELECT * FROM _df")
    con.unregister("_df")


def read_df(con: duckdb.DuckDBPyConnection, sql: str, params: tuple | None = None) -> pd.DataFrame:
    if params is None:
        return con.execute(sql).fetchdf()
    return con.execute(sql, params).fetchdf()
