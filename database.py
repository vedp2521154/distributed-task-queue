import sqlite3


class Database:
    def __init__(self, db_name="task_queue.db"):
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)
        self.create_tasks_table()

    def create_tasks_table(self):
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                task_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                status TEXT NOT NULL,
                retry_count INTEGER NOT NULL,
                max_retries INTEGER NOT NULL
            )
            """
        )

        self.connection.commit()

    def save_task(self, task):
        self.connection.execute(
            """
            INSERT INTO tasks (
                task_id,
                name,
                status,
                retry_count,
                max_retries
            )
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(task_id) DO UPDATE SET
                name = excluded.name,
                status = excluded.status,
                retry_count = excluded.retry_count,
                max_retries = excluded.max_retries
            """,
            (
                task.task_id,
                task.name,
                task.status,
                task.retry_count,
                task.max_retries,
            ),
        )

        self.connection.commit()

    def update_task(self, task):
     connection = sqlite3.connect(self.db_name)

     connection.execute(
        """
        UPDATE tasks
        SET status = ?,
            retry_count = ?
        WHERE task_id = ?
        """,
        (
            task.status,
            task.retry_count,
            task.task_id,
        ),
    )

     connection.commit()
     connection.close()

    def load_task(self, task_id):
        cursor = self.connection.execute(
            """
            SELECT task_id,
                   name,
                   status,
                   retry_count,
                   max_retries
            FROM tasks
            WHERE task_id = ?
            """,
            (task_id,),
        )

        return cursor.fetchone()

    def load_pending_tasks(self):
        cursor = self.connection.execute(
            """
            SELECT task_id,
                   name,
                   status,
                   retry_count,
                   max_retries
            FROM tasks
            WHERE status = ?
            """,
            ("PENDING",),
        )

        return cursor.fetchall()

    def load_all_task_ids(self):
        cursor = self.connection.execute(
            """
            SELECT task_id
            FROM tasks
            """
        )

        return {row[0] for row in cursor.fetchall()}
