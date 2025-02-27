import sqlite3
import asyncio

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("economy.db")
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                balance INTEGER DEFAULT 0
            )
        """)
        self.conn.commit()

    async def get_balance(self, user_id: str) -> int:
        self.cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()
        if result is None:
            self.cursor.execute("INSERT INTO users (user_id, balance) VALUES (?, 0)", (user_id,))
            self.conn.commit()
            return 0
        return result[0]

    async def update_balance(self, user_id: str, amount: int):
        current = await self.get_balance(user_id)
        new_balance = current + amount
        self.cursor.execute(
            "INSERT OR REPLACE INTO users (user_id, balance) VALUES (?, ?)",
            (user_id, new_balance)
        )
        self.conn.commit()

    def __del__(self):
        self.conn.close()
