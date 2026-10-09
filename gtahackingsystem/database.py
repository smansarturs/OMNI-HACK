"""SQLite storage for OMNI-HACK progress."""

import os
import sqlite3

SAVE_DIR = os.path.join(os.path.expanduser("~"), ".omnihack")
DB_FILE = os.path.join(SAVE_DIR, "progress.db")


def _con():
    os.makedirs(SAVE_DIR, exist_ok=True)
    return sqlite3.connect(DB_FILE)


def init_db():
    con = _con()
    try:
        con.execute(
            """CREATE TABLE IF NOT EXISTS progress (
                   id INTEGER PRIMARY KEY CHECK (id = 1),
                   security_level INTEGER NOT NULL,
                   integrity INTEGER NOT NULL,
                   credits INTEGER NOT NULL,
                   completed_games INTEGER NOT NULL
               )"""
        )
        con.commit()
    finally:
        con.close()


def save_state(state):
    con = _con()
    try:
        con.execute(
            "INSERT OR REPLACE INTO progress "
            "(id, security_level, integrity, credits, completed_games) "
            "VALUES (1, ?, ?, ?, ?)",
            (state.security_level, state.integrity,
             state.credits, state.completed_games),
        )
        con.commit()
    finally:
        con.close()


def load_state(state):
    con = _con()
    try:
        row = con.execute(
            "SELECT security_level, integrity, credits, completed_games "
            "FROM progress WHERE id = 1"
        ).fetchone()
    finally:
        con.close()
    if row:
        (state.security_level, state.integrity,
         state.credits, state.completed_games) = row


def reset_progress(state):
    state.security_level = 1
    state.integrity = 3
    state.credits = 0
    state.completed_games = 0
    save_state(state)