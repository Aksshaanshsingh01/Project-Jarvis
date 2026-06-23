import sqlite3


class MemoryManager:

    def __init__(self):
        self.conn = sqlite3.connect("database/jarvis_memory.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fact TEXT
            )
        """)

        self.conn.commit()

    def save_memory(self, fact):
        self.cursor.execute(
            "INSERT INTO memories (fact) VALUES (?)",
            (fact,)
        )

        self.conn.commit()

    def get_memories(self):

        self.cursor.execute(
            "SELECT fact FROM memories"
        )

        memories = self.cursor.fetchall()

        return [memory[0] for memory in memories]