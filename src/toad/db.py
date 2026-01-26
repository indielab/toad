from datetime import datetime
from pathlib import Path
from typing import TypedDict
from toad import paths

import aiosqlite


class Session(TypedDict):
    id: int
    title: str
    agent: str
    session_id: str
    protocol: str
    created_at: datetime
    last_used: datetime


class DB:
    def __init__(self):
        self.path = paths.get_state() / "toad.db"

    def open(self) -> aiosqlite.Connection:
        return aiosqlite.connect(self.path)

    async def create(self) -> bool:
        try:
            async with self.open() as db:
                await db.execute(
                    """
                    CREATE TABLE IF NOT EXISTS sessions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        agent TEXT NOT NULL,
                        session_id TEXT NOT NULL,                                
                        title TEXT NOT NULL,      
                        protocol TEXT NOT NULL,                  
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        meta TEXT DEFAULT '{}'
                    )
                    """
                )
        except aiosqlite.Error:
            raise
            return False
        return True

    async def new_session(
        self,
        title: str,
        agent: str,
        session_id: str,
        protocol: str = "acp",
    ) -> bool:
        try:
            async with self.open() as db:
                await db.execute(
                    """
                    INSERT INTO sessions (title, agent, session_id, protocol) VALUES (?, ?, ?, ?)    
                    """,
                    (
                        title,
                        agent,
                        session_id,
                        protocol,
                    ),
                )
                await db.commit()
        except aiosqlite.Error:
            raise
            return False
        return True
